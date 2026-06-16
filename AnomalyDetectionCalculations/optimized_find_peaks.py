"""Optuna-based hyperparameter optimization for ``scipy.signal.find_peaks``.

This module provides :class:`OptimizedFindPeaks`, a thin wrapper around
``scipy.signal.find_peaks`` that uses `Optuna <https://optuna.org/>`_ to search
for the parameter set (``height``, ``prominence``, ``distance``, ...) that best
recovers a set of known/ground-truth peak locations from a signal.

The typical use case is anomaly detection, where the ground-truth anomalies are
known on a training signal and we want to pick ``find_peaks`` parameters that
maximize a classification metric (F1 by default) between the detected peaks and
the true anomaly positions.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

import numpy as np
import optuna
from scipy.signal import find_peaks

# All keyword arguments accepted by ``scipy.signal.find_peaks`` that this
# wrapper knows how to optimize, together with their type ("float" or "int").
_OPTIMIZABLE_PARAMS: dict[str, str] = {
    "height": "float",
    "threshold": "float",
    "distance": "int",
    "prominence": "float",
    "width": "float",
    "wlen": "int",
    "rel_height": "float",
    "plateau_size": "int",
}

# A search space entry is either a ``(low, high)`` pair or a
# ``(low, high, options)`` triple where ``options`` is a mapping forwarded to
# the Optuna ``suggest_*`` call (e.g. ``{"log": True}``).
SearchBound = Sequence[Any]
Scorer = Callable[[np.ndarray, np.ndarray, int], float]


def _as_index_mask(true_peaks: np.ndarray, n_samples: int) -> np.ndarray:
    """Convert ground-truth peaks to a boolean mask of length ``n_samples``.

    Parameters
    ----------
    true_peaks : numpy.ndarray
        Either a boolean mask of length ``n_samples`` or an array of integer
        indices marking the true peak positions.
    n_samples : int
        Length of the signal the peaks refer to.

    Returns
    -------
    numpy.ndarray
        Boolean mask of length ``n_samples`` that is ``True`` at every true
        peak position.

    Examples
    --------
    >>> _as_index_mask(np.array([1, 3]), 5)
    array([False,  True, False,  True, False])
    >>> _as_index_mask(np.array([False, True, False, True, False]), 5)
    array([False,  True, False,  True, False])
    """
    true_peaks = np.asarray(true_peaks)
    if true_peaks.dtype == bool:
        if true_peaks.shape[0] != n_samples:
            raise ValueError(
                f"Boolean mask length {true_peaks.shape[0]} does not match "
                f"signal length {n_samples}."
            )
        return true_peaks
    mask = np.zeros(n_samples, dtype=bool)
    mask[true_peaks.astype(int)] = True
    return mask


def _f1_components(
    true_mask: np.ndarray, pred_peaks: np.ndarray, tolerance: int
) -> tuple[int, int, int]:
    """Greedily match predicted peaks to true peaks within ``tolerance``.

    Parameters
    ----------
    true_mask : numpy.ndarray
        Boolean mask marking true peak positions.
    pred_peaks : numpy.ndarray
        Integer indices of the predicted peaks.
    tolerance : int
        Maximum absolute index distance for a predicted peak to count as a
        match for a true peak. ``0`` requires an exact index match.

    Returns
    -------
    tp, fp, fn : int
        Number of true positives, false positives and false negatives.
    """
    true_idx = np.flatnonzero(true_mask)
    pred = np.sort(np.asarray(pred_peaks, dtype=int))
    matched_true = np.zeros(true_idx.shape[0], dtype=bool)
    tp = 0
    for p in pred:
        if true_idx.shape[0] == 0:
            break
        dist = np.abs(true_idx - p)
        # Only consider true peaks that are still unmatched and close enough.
        dist[matched_true] = tolerance + 1
        nearest = int(np.argmin(dist))
        if dist[nearest] <= tolerance:
            matched_true[nearest] = True
            tp += 1
    fp = pred.shape[0] - tp
    fn = int((~matched_true).sum())
    return tp, fp, fn


def _make_metric_scorer(metric: str, tolerance: int) -> Scorer:
    """Build a scorer callable for one of the supported metric names.

    Parameters
    ----------
    metric : {'f1', 'precision', 'recall', 'accuracy'}
        Name of the classification metric to optimize.
    tolerance : int
        Index tolerance used when matching predicted to true peaks.

    Returns
    -------
    callable
        A function ``scorer(true_mask, pred_peaks, n_samples) -> float``.
    """
    metric = metric.lower()
    valid = {"f1", "precision", "recall", "accuracy"}
    if metric not in valid:
        raise ValueError(f"Unknown metric {metric!r}; choose one of {sorted(valid)}.")

    def scorer(true_mask: np.ndarray, pred_peaks: np.ndarray, n_samples: int) -> float:
        tp, fp, fn = _f1_components(true_mask, pred_peaks, tolerance)
        if metric == "precision":
            return tp / (tp + fp) if (tp + fp) else 0.0
        if metric == "recall":
            return tp / (tp + fn) if (tp + fn) else 0.0
        if metric == "accuracy":
            tn = n_samples - tp - fp - fn
            return (tp + tn) / n_samples if n_samples else 0.0
        # f1
        denom = 2 * tp + fp + fn
        return (2 * tp) / denom if denom else 0.0

    return scorer


class OptimizedFindPeaks:
    """Optimize ``scipy.signal.find_peaks`` parameters with Optuna.

    The optimizer searches over the ``find_peaks`` keyword arguments listed in
    ``search_space`` to maximize (or minimize) a score computed by comparing the
    detected peaks against a set of ground-truth peak positions. Any parameter
    can be pinned to a constant value through ``fixed_params`` so that it is
    passed verbatim to ``find_peaks`` and excluded from the search.

    Parameters
    ----------
    scorer : {'f1', 'precision', 'recall', 'accuracy'} or callable, optional
        How to score a candidate parameter set. If a string, the corresponding
        classification metric is computed between the detected peaks and the
        ground-truth peaks. If a callable, it must have the signature
        ``scorer(true_mask, pred_peaks, n_samples) -> float`` where
        ``true_mask`` is a boolean array of true peak positions, ``pred_peaks``
        is the integer index array returned by ``find_peaks`` and ``n_samples``
        is the signal length. Default is ``'f1'``.
    search_space : dict, optional
        Mapping from a ``find_peaks`` parameter name to its search bounds. Each
        value is either a ``(low, high)`` pair or a ``(low, high, options)``
        triple, where ``options`` is a dict forwarded to the Optuna
        ``suggest_float``/``suggest_int`` call (e.g. ``{"log": True}``). Only
        the keys in :data:`_OPTIMIZABLE_PARAMS` may be optimized. If ``None``, a
        default search space is derived from the signal passed to :meth:`fit`.
    fixed_params : dict, optional
        Parameters passed unchanged to ``find_peaks`` on every trial. Keys here
        take precedence over and are removed from ``search_space``.
    n_trials : int, optional
        Number of Optuna trials to run. Default is ``100``.
    direction : {'maximize', 'minimize'}, optional
        Optimization direction. Default is ``'maximize'`` (suitable for the
        built-in metrics).
    tolerance : int, optional
        Index tolerance for matching predicted peaks to true peaks when using a
        built-in string ``scorer``. ``0`` (default) requires exact matches.
    seed : int, optional
        Seed for Optuna's ``TPESampler`` for reproducible studies. Default is 0.
    verbose : bool, optional
        If ``False`` (default), Optuna's logging is silenced.

    Attributes
    ----------
    study_ : optuna.study.Study
        The Optuna study created by :meth:`fit`.
    best_params_ : dict
        Best parameters found, including the fixed parameters. Ready to splat
        into ``find_peaks``.
    best_score_ : float
        Score of the best trial.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.signal import find_peaks
    >>> rng = np.random.default_rng(0)
    >>> t = np.linspace(0, 20 * np.pi, 1000)
    >>> signal = np.sin(t) + 0.1 * rng.standard_normal(t.size)
    >>> true_peaks, _ = find_peaks(np.sin(t))      # noise-free reference peaks
    >>> opt = OptimizedFindPeaks(
    ...     scorer="f1",
    ...     fixed_params={"distance": 20},
    ...     n_trials=40,
    ...     tolerance=3,
    ...     seed=0,
    ... )
    >>> opt.fit(signal, true_peaks)                       # doctest: +ELLIPSIS
    <...OptimizedFindPeaks object at 0x...>
    >>> 0.0 <= opt.best_score_ <= 1.0
    True
    >>> peaks, props = opt.predict(signal)
    >>> # The tuned kwargs can be reused directly on a new signal:
    >>> kwargs = opt.find_peaks_kwargs()
    >>> peaks2, props2 = find_peaks(signal, **kwargs)
    >>> np.array_equal(peaks, peaks2)
    True
    """

    def __init__(
        self,
        scorer: str | Scorer = "f1",
        search_space: dict[str, SearchBound] | None = None,
        fixed_params: dict[str, Any] | None = None,
        n_trials: int = 100,
        direction: str = "maximize",
        tolerance: int = 0,
        seed: int | None = 0,
        verbose: bool = False,
    ) -> None:
        self.scorer = scorer
        self.search_space = search_space
        self.fixed_params = dict(fixed_params) if fixed_params else {}
        self.n_trials = n_trials
        self.direction = direction
        self.tolerance = tolerance
        self.seed = seed
        self.verbose = verbose

        self.study_: optuna.study.Study | None = None
        self.best_params_: dict[str, Any] | None = None
        self.best_score_: float | None = None

        # Guard against obvious typos in fixed parameter names.
        allowed = {
            "height",
            "threshold",
            "distance",
            "prominence",
            "width",
            "wlen",
            "rel_height",
            "plateau_size",
        }
        unknown = set(self.fixed_params) - allowed
        if unknown:
            raise ValueError(
                f"fixed_params contains unknown find_peaks arguments: {sorted(unknown)}."
            )

    def _resolve_scorer(self) -> Scorer:
        """Return the scorer callable, building it from a name if needed."""
        if callable(self.scorer):
            return self.scorer
        return _make_metric_scorer(self.scorer, self.tolerance)

    def _default_search_space(self, x: np.ndarray) -> dict[str, SearchBound]:
        """Derive a sensible default search space from the signal ``x``.

        Parameters
        ----------
        x : numpy.ndarray
            The signal whose peaks are being detected.

        Returns
        -------
        dict
            Default ``(low, high[, options])`` bounds for the optimizable
            parameters, scaled to the amplitude and length of ``x``.
        """
        span = float(np.ptp(x)) or 1.0
        n = int(x.shape[0])
        # Tune the three most generally useful, well-behaved knobs. ``width``,
        # ``wlen``, ``plateau_size`` etc. are specialized filters that easily
        # suppress valid peaks, so they are left for the user to add explicitly
        # through ``search_space`` when the application calls for them.
        return {
            "height": (float(np.min(x)), float(np.max(x))),
            "prominence": (1e-3 * span, span, {"log": True}),
            "distance": (1, max(2, n // 2)),
        }

    def _build_kwargs(self, trial: optuna.Trial, space: dict[str, SearchBound]) -> dict[str, Any]:
        """Sample one ``find_peaks`` kwargs dict from a trial.

        Parameters
        ----------
        trial : optuna.Trial
            The trial used to suggest values.
        space : dict
            The effective search space (defaults already filled in, fixed
            parameters removed).

        Returns
        -------
        dict
            Keyword arguments for ``find_peaks`` combining the suggested values
            with the fixed parameters.
        """
        kwargs: dict[str, Any] = dict(self.fixed_params)
        for name, bound in space.items():
            ptype = _OPTIMIZABLE_PARAMS[name]
            low, high = bound[0], bound[1]
            options = bound[2] if len(bound) > 2 else {}
            if ptype == "int":
                kwargs[name] = trial.suggest_int(name, int(low), int(high), **options)
            else:
                kwargs[name] = trial.suggest_float(name, float(low), float(high), **options)
        return kwargs

    def fit(self, x: np.ndarray, true_peaks: np.ndarray) -> "OptimizedFindPeaks":
        """Run the Optuna search to find the best ``find_peaks`` parameters.

        Parameters
        ----------
        x : array_like
            One-dimensional signal in which to detect peaks.
        true_peaks : array_like
            Ground-truth peak positions, given either as an integer index array
            or as a boolean mask of the same length as ``x``.

        Returns
        -------
        OptimizedFindPeaks
            The fitted estimator (``self``), enabling method chaining.

        Raises
        ------
        ValueError
            If ``search_space`` references parameters that cannot be optimized.

        Examples
        --------
        >>> import numpy as np
        >>> x = np.array([0, 1, 0, 5, 1, 4, 0], dtype=float)
        >>> opt = OptimizedFindPeaks(n_trials=10, seed=0).fit(x, np.array([3, 5]))
        >>> sorted(opt.best_params_)  # doctest: +ELLIPSIS
        [...]
        """
        x = np.asarray(x, dtype=float).ravel()
        true_mask = _as_index_mask(np.asarray(true_peaks), x.shape[0])
        n_samples = x.shape[0]
        scorer = self._resolve_scorer()

        space = dict(self.search_space) if self.search_space is not None else self._default_search_space(x)
        unknown = set(space) - set(_OPTIMIZABLE_PARAMS)
        if unknown:
            raise ValueError(
                f"search_space contains non-optimizable parameters: {sorted(unknown)}. "
                f"Optimizable parameters are {sorted(_OPTIMIZABLE_PARAMS)}."
            )
        # Fixed parameters win over the search space.
        for name in self.fixed_params:
            space.pop(name, None)

        def objective(trial: optuna.Trial) -> float:
            kwargs = self._build_kwargs(trial, space)
            peaks, _ = find_peaks(x, **kwargs)
            return scorer(true_mask, peaks, n_samples)

        if not self.verbose:
            optuna.logging.set_verbosity(optuna.logging.WARNING)
        sampler = optuna.samplers.TPESampler(seed=self.seed)
        self.study_ = optuna.create_study(direction=self.direction, sampler=sampler)
        self.study_.optimize(objective, n_trials=self.n_trials)

        self.best_params_ = {**self.fixed_params, **self.study_.best_params}
        self.best_score_ = float(self.study_.best_value)
        return self

    def find_peaks_kwargs(self) -> dict[str, Any]:
        """Return the optimized keyword arguments for ``find_peaks``.

        Returns
        -------
        dict
            Mapping ready to be splatted into ``scipy.signal.find_peaks``, e.g.
            ``find_peaks(signal, **opt.find_peaks_kwargs())``. Includes any
            fixed parameters.

        Raises
        ------
        RuntimeError
            If called before :meth:`fit`.

        Examples
        --------
        >>> import numpy as np
        >>> from scipy.signal import find_peaks
        >>> x = np.array([0, 1, 0, 5, 1, 4, 0], dtype=float)
        >>> opt = OptimizedFindPeaks(n_trials=10, seed=0).fit(x, np.array([3, 5]))
        >>> kwargs = opt.find_peaks_kwargs()
        >>> peaks, _ = find_peaks(x, **kwargs)
        >>> isinstance(peaks, np.ndarray)
        True
        """
        if self.best_params_ is None:
            raise RuntimeError("Call fit() before requesting the optimized kwargs.")
        return dict(self.best_params_)

    def predict(self, x: np.ndarray) -> tuple[np.ndarray, dict[str, np.ndarray]]:
        """Run ``find_peaks`` on ``x`` using the optimized parameters.

        Parameters
        ----------
        x : array_like
            One-dimensional signal in which to detect peaks.

        Returns
        -------
        peaks : numpy.ndarray
            Indices of the detected peaks.
        properties : dict
            The properties dictionary returned by ``scipy.signal.find_peaks``.

        Raises
        ------
        RuntimeError
            If called before :meth:`fit`.

        Examples
        --------
        >>> import numpy as np
        >>> x = np.array([0, 1, 0, 5, 1, 4, 0], dtype=float)
        >>> opt = OptimizedFindPeaks(n_trials=10, seed=0).fit(x, np.array([3, 5]))
        >>> peaks, props = opt.predict(x)
        >>> peaks.dtype.kind
        'i'
        """
        x = np.asarray(x, dtype=float).ravel()
        return find_peaks(x, **self.find_peaks_kwargs())


if __name__ == "__main__":
    # Small demonstration: recover the peaks of a clean sine from a noisy copy.
    rng = np.random.default_rng(0)
    t = np.linspace(0, 20 * np.pi, 1000)
    clean = np.sin(t)
    noisy = clean + 0.3 * rng.standard_normal(t.size)

    reference_peaks, _ = find_peaks(clean)

    optimizer = OptimizedFindPeaks(
        scorer="f1",
        #fixed_params={"distance": 20},
        n_trials=300,
        tolerance=4,
        seed=0
    )
    optimizer.fit(noisy, reference_peaks)

    print(f"Best F1 score : {optimizer.best_score_:.3f}")
    print(f"Best params   : {optimizer.best_params_}")
    print(f"find_peaks kwargs: {optimizer.find_peaks_kwargs()}")

    detected, _ = optimizer.predict(noisy)
    print(f"True peaks     : {reference_peaks.size}")
    print(f"Detected peaks : {detected.size}")

"""Generate the OptimizedFindPeaks tutorial and solution notebooks.

Run once with the WignerCampEnv conda environment:

    python _make_notebooks.py

This produces:
    optimized_find_peaks_tutorial.ipynb
    optimized_find_peaks_solution.ipynb

The script is kept in the repo so the notebooks can be regenerated/edited from
plain text rather than hand-editing JSON.
"""

import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

# --------------------------------------------------------------------------- #
# Reusable cell contents
# --------------------------------------------------------------------------- #

# Raw URL of the class on the public GitHub repo (always the latest `main`).
RAW_CLASS_URL = (
    "https://raw.githubusercontent.com/intensivedatacomp/WignerCamp2026/"
    "main/AnomalyDetectionCalculations/optimized_find_peaks.py"
)

COLAB_SETUP = f"""\
try:
    from google.colab import drive
    IN_COLAB = True
    drive.mount('/content/drive/')
    # Your working copy on Google Drive.
    !mkdir -p "/content/drive/My Drive/WignerCamp2026/AnomalyDetection"
    %cd /content/drive/My\\ Drive/WignerCamp2026/AnomalyDetection
    !pip install optuna --quiet
    # Make the OptimizedFindPeaks class importable: grab the latest version
    # straight from GitHub into the working directory.
    !wget -q -O optimized_find_peaks.py {RAW_CLASS_URL}
except:
    IN_COLAB = False
    %load_ext autoreload
    %autoreload 2
print(f'Running on {{"Google colab" if IN_COLAB else "Local computer"}}')"""

IMPORTS = """\
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# The class we are learning about lives next to this notebook.
from optimized_find_peaks import OptimizedFindPeaks

# Optuna is chatty by default; silence everything below a warning.
import optuna
optuna.logging.set_verbosity(optuna.logging.WARNING)"""

MAKE_SIGNAL = """\
def make_anomaly_signal(seed=0):
    \"\"\"A slow baseline with a handful of sharp 'anomaly' spikes plus noise.

    Returns the signal and the indices of the true spikes (our ground truth).
    \"\"\"
    rng = np.random.default_rng(seed)
    n = 1000
    baseline = 0.6 * np.sin(np.linspace(0, 6 * np.pi, n))   # gentle background
    true_peaks = np.sort(rng.choice(np.arange(20, n - 20), size=8, replace=False))
    signal = baseline.copy()
    for p in true_peaks:
        amp = rng.uniform(4, 7)          # spikes are much taller than baseline
        w = 4
        idx = np.arange(p - w, p + w + 1)
        signal[idx] += amp * (1 - np.abs(idx - p) / (w + 1))
    signal += 0.4 * rng.standard_normal(n)  # measurement noise
    return signal, true_peaks

signal, true_peaks = make_anomaly_signal()
print(f"Signal length     : {signal.size}")
print(f"True anomalies (8): {true_peaks}")

fig, ax = plt.subplots(figsize=(11, 4))
ax.plot(signal, lw=0.8, color="steelblue", label="signal")
ax.plot(true_peaks, signal[true_peaks], "v", color="green", ms=11,
        label="true anomalies")
ax.set_xlabel("sample index")
ax.set_ylabel("amplitude")
ax.legend(loc="upper right")
ax.set_title("Anomaly signal: 8 sharp spikes hidden in a noisy baseline")
plt.tight_layout()
plt.show()"""

PLOT_HELPER = """\
def plot_result(signal, true_peaks, found_peaks, title=""):
    \"\"\"Plot a signal with its true peaks and the peaks we detected.\"\"\"
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(signal, lw=0.8, color="steelblue", alpha=0.8, label="signal")
    ax.plot(true_peaks, signal[true_peaks], "v", color="green", ms=11,
            label=f"true peaks ({np.size(true_peaks)})")
    ax.plot(found_peaks, signal[found_peaks], "x", color="red", ms=9, mew=2,
            label=f"found peaks ({np.size(found_peaks)})")
    ax.set_xlabel("sample index")
    ax.set_ylabel("amplitude")
    ax.legend(loc="upper right")
    ax.set_title(title)
    plt.tight_layout()
    plt.show()"""


def build(solution: bool) -> nbf.NotebookNode:
    """Build the tutorial (solution=False) or solution (solution=True) notebook."""
    cells = []
    md = lambda s: cells.append(new_markdown_cell(s))
    code = lambda s: cells.append(new_code_cell(s))

    kind = "Solutions" if solution else "Tutorial"
    nb_name = (
        "optimized_find_peaks_solution.ipynb"
        if solution
        else "optimized_find_peaks_tutorial.ipynb"
    )
    colab_url = (
        "https://colab.research.google.com/github/intensivedatacomp/"
        f"WignerCamp2026/blob/main/AnomalyDetectionCalculations/{nb_name}"
    )

    # ---------------------------------------------------------------- Title
    md(
        f"[![Open In Colab](https://colab.research.google.com/assets/"
        f"colab-badge.svg)]({colab_url})"
    )
    md(f"""\
# `OptimizedFindPeaks` — {kind}

`scipy.signal.find_peaks` is powerful but has many parameters (`height`,
`prominence`, `distance`, `width`, ...). Choosing them by hand is tedious.

`OptimizedFindPeaks` (in `optimized_find_peaks.py`) wraps `find_peaks` and uses
**Optuna** to search for the parameter set that best recovers a set of
*known / ground-truth* peak positions.

This is exactly the situation in **anomaly detection**: on a training signal we
know where the anomalies are, and we want `find_peaks` parameters that turn the
signal into the correct set of anomaly flags. We can then reuse those parameters
on new, unlabelled signals.

In this notebook each topic is introduced with a worked **example**, followed by
a short **exercise**.{" The exercise cells contain the reference solutions." if solution else " Fill in the cells marked `# TODO`."}""")

    code(COLAB_SETUP)
    code(IMPORTS)

    # ---------------------------------------------------------------- Data
    md("""\
## 1. The data

We need a signal **and** the *true* peak positions to score against. Our signal
is a gentle baseline with 8 sharp **anomaly spikes** at known locations, buried
in noise. The noise creates many small bumps, so a naive `find_peaks` will report
hundreds of "peaks" — there is plenty to optimize.""")
    code(MAKE_SIGNAL)
    code(PLOT_HELPER)

    # ---------------------------------------------------------------- Sec 2
    md("""\
## 2. Basic usage

The workflow mirrors scikit-learn:

1. **Create** an `OptimizedFindPeaks` with how many Optuna trials to run and a
   `seed` for reproducibility.
2. **`fit(signal, true_peaks)`** runs the Optuna search. `true_peaks` may be an
   array of integer indices *or* a boolean mask the length of the signal.
3. Read **`best_params_`** (the winning parameters) and **`best_score_`** (the
   best metric value, F1 by default).
4. **`predict(signal)`** runs `find_peaks` with those parameters and returns
   `(peaks, properties)` — just like `find_peaks` itself.
5. **`find_peaks_kwargs()`** returns the parameter dict so you can reuse it on a
   *new* signal: `find_peaks(other_signal, **kwargs)`.

First, the baseline — `find_peaks` with no tuning at all:""")
    code("""\
baseline_peaks, _ = find_peaks(signal)
print(f"Untuned find_peaks finds {baseline_peaks.size} peaks "
      f"(there are only {true_peaks.size} true anomalies).")""")

    md("""\
Now let `OptimizedFindPeaks` tune the parameters. We pass `tolerance=2`; Section
4 explains exactly what it does. For now: it lets a detected peak count as
correct if it lands within 2 samples of a true peak (a small safety margin).""")
    code("""\
opt = OptimizedFindPeaks(scorer="f1", n_trials=100, tolerance=2, seed=0)
opt.fit(signal, true_peaks)

print(f"Best F1 score : {opt.best_score_:.3f}")
print(f"Best params   : {opt.best_params_}")

found_peaks, props = opt.predict(signal)
plot_result(signal, true_peaks, found_peaks, f"Tuned find_peaks (F1 = {opt.best_score_:.3f})")""")

    md("""\
The tuned parameters are reusable on any signal of the same kind:""")
    code("""\
from optimized_find_peaks import _f1_components

kwargs = opt.find_peaks_kwargs()
print("Reusable kwargs:", kwargs)

# Apply them directly with plain scipy on a freshly generated signal.
new_signal, new_true = make_anomaly_signal(seed=99)
peaks_new, _ = find_peaks(new_signal, **kwargs)
print(f"On a new signal the same kwargs find {peaks_new.size} peaks "
      f"(true anomalies: {new_true.size}).")

new_mask = np.zeros(new_signal.size, dtype=bool)
new_mask[new_true] = True
new_tp, new_fp, new_fn = _f1_components(new_mask, peaks_new, tolerance=2)

new_precision = new_tp / (new_tp + new_fp) if (new_tp + new_fp) else 0.0
new_recall    = new_tp / (new_tp + new_fn) if (new_tp + new_fn) else 0.0
new_f1        = 2 * new_tp / (2 * new_tp + new_fp + new_fn) if (2 * new_tp + new_fp + new_fn) else 0.0
         
plot_result(new_signal, new_true, peaks_new, f"Tuned find_peaks (F1 = {new_f1:.3f})")""")

    # --------- Exercise 1
    md("""\
### Exercise 1

Create your own `OptimizedFindPeaks`, fit it to `signal`/`true_peaks`, and plot
the result.

- Use `n_trials=150`, `tolerance=2`, `seed=1`.
- Print `best_score_` and `best_params_`.
- Use `plot_result` to visualise the detected peaks.""")
    if solution:
        code("""\
opt1 = OptimizedFindPeaks(scorer="f1", n_trials=150, tolerance=2, seed=1)
opt1.fit(signal, true_peaks)
print(f"Best F1: {opt1.best_score_:.3f}")
print(f"Best params: {opt1.best_params_}")
peaks1, _ = opt1.predict(signal)
plot_result(signal, true_peaks, peaks1, f"Exercise 1 (F1 = {opt1.best_score_:.3f})")""")
    else:
        code("""\
# TODO: create the optimizer, fit it, print the results and plot.
opt1 = OptimizedFindPeaks(...)
# opt1.fit(...)
# ...
# plot_result(...)""")

    # ---------------------------------------------------------------- Sec 3
    md("""\
## 3. Fixing parameters and choosing the search space

By default the optimizer tunes three well-behaved, widely useful knobs —
`height`, `prominence` and `distance` — with bounds derived from the signal.
Two common ways to take more control:

- **Fix a parameter.** Maybe physics tells you anomalies are at least 20 samples
  apart. Pass `fixed_params={"distance": 20}`: that value is sent to
  `find_peaks` on every trial and is *not* optimized (it still appears in
  `best_params_` and `find_peaks_kwargs()`).
- **Set the search space.** Override the defaults with `search_space`, a dict
  mapping a parameter name to its bounds:
    - `(low, high)` → a float searched linearly,
    - `(low, high, {"log": True})` → a float searched on a log scale (great for
      `prominence`, which spans orders of magnitude),
    - `(low, high)` on an integer parameter (`distance`, `wlen`, `plateau_size`)
      → searched as an integer.

  Only these keys may be optimized: `height`, `threshold`, `distance`,
  `prominence`, `width`, `wlen`, `rel_height`, `plateau_size`.""")
    code("""\
opt_fixed = OptimizedFindPeaks(
    scorer="f1",
    fixed_params={"distance": 20},                 # pinned, not optimized
    search_space={
        "prominence": (1e-3, 8.0, {"log": True}),  # log-scale float
        "height": (-1.0, 8.0),                     # linear float
    },
    n_trials=100,
    tolerance=2,
    seed=0,
)
opt_fixed.fit(signal, true_peaks)
print(f"Best F1     : {opt_fixed.best_score_:.3f}")
print(f"Best params : {opt_fixed.best_params_}")   # note distance == 20 always""")

    # --------- Exercise 2
    md("""\
### Exercise 2

Build an optimizer that:

- **fixes** `width` to `1.0` (a minimal width filter),
- searches `prominence` on a **log scale** between `1e-3` and `8.0`,
- searches the integer `distance` between `5` and `40`,
- runs `n_trials=150`, `tolerance=2`, `seed=2`.

Fit it, print the best score and params, and confirm `width` is `1.0` in
`best_params_`.""")
    if solution:
        code("""\
opt2 = OptimizedFindPeaks(
    scorer="f1",
    fixed_params={"width": 1.0},
    search_space={
        "prominence": (1e-3, 8.0, {"log": True}),
        "distance": (5, 40),          # integer parameter -> searched as int
    },
    n_trials=150,
    tolerance=2,
    seed=2,
)
opt2.fit(signal, true_peaks)
print(f"Best F1     : {opt2.best_score_:.3f}")
print(f"Best params : {opt2.best_params_}")
assert opt2.best_params_["width"] == 1.0""")
    else:
        code("""\
# TODO: build the optimizer described above, fit it, and print the results.
opt2 = OptimizedFindPeaks(...)
# opt2.fit(signal, true_peaks)
# print(opt2.best_score_, opt2.best_params_)""")

    # ---------------------------------------------------------------- Sec 4
    md("""\
## 4. Understanding `tolerance` (read this carefully)

To turn detected peaks into a score, the class compares the **detected peak
indices** with the **true peak indices** and counts:

- **True positive (TP)** — a detected peak that matches a true peak,
- **False positive (FP)** — a detected peak that matches *no* true peak,
- **False negative (FN)** — a true peak that *no* detected peak matched.

From these it computes precision, recall and F1.

**The key question: when does a detected peak "match" a true peak?**

If we demanded the detected index equal the true index *exactly*, detection
would be unfairly punished. On a smooth or noisy peak the highest sample is
often shifted by a sample or two, so a peak detected at index 101 would not count
for a true peak at index 100.

`tolerance` is that allowed wiggle room, measured in **samples (indices)**:

> A detected peak at index `p` matches a true peak at index `q` if
> `abs(p - q) <= tolerance`.

- `tolerance=0` (default) → indices must match **exactly**.
- `tolerance=3` → a detected peak counts as correct if it is within 3 samples of
  a true peak.

Matching is **greedy and one-to-one**: each true peak is matched by at most one
detected peak and vice-versa, so you cannot inflate the score by stacking several
detections next to a single true peak.

Let's make it concrete. The helper `_f1_components` (used internally by the
class) returns the `(TP, FP, FN)` counts so we can watch them change.""")
    code("""\
from optimized_find_peaks import _f1_components

# True peaks at indices 10, 50, 90 (as a boolean mask over 100 samples).
true_mask = np.zeros(100, dtype=bool)
true_mask[[10, 50, 90]] = True

# Suppose find_peaks reported these indices:
#   11 is 1 away from 10, 52 is 2 away from 50, 70 is far from everything,
#   and nothing lands near 90.
predicted = np.array([11, 52, 70])

for tol in (0, 1, 2, 5):
    tp, fp, fn = _f1_components(true_mask, predicted, tolerance=tol)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) else 0.0
    print(f"tolerance={tol}: TP={tp} FP={fp} FN={fn}  "
          f"precision={precision:.2f} recall={recall:.2f} F1={f1:.2f}")""")

    md("""\
Walking through the output:

- **`tolerance=0`**: none of `11, 52, 70` equals a true index exactly →
  `TP=0`, `FP=3`, `FN=3`, `F1=0.00`.
- **`tolerance=1`**: only `11` is within 1 of `10` → `TP=1`. `52` is 2 away from
  `50` (too far), `70` matches nothing → `FP=2`, `FN=2`.
- **`tolerance=2`**: now `52` also matches `50` → `TP=2`, `FP=1` (the stray
  `70`), `FN=1` (true peak `90` was never detected).
- **`tolerance=5`**: still `TP=2` — a bigger tolerance does not rescue `70`
  (nearest true peak `50` is 20 away) nor the missed true peak `90`.

So `tolerance` controls **how forgiving the index-matching is**, not which peaks
`find_peaks` returns.

### The same effect on a real signal

Below is a signal of smooth Gaussian bumps. Because each bump is rounded, the
*noisiest sample* near the top is offset from the true centre by a few indices —
exactly the situation `tolerance` exists for.""")
    code("""\
def make_bump_signal(seed=0):
    \"\"\"Four smooth Gaussian bumps; their centres are the true peaks.\"\"\"
    rng = np.random.default_rng(seed)
    n = 400
    centers = np.array([50, 150, 250, 350])
    x = np.arange(n)
    sig = np.zeros(n)
    for c in centers:
        sig += 2.0 * np.exp(-0.5 * ((x - c) / 8.0) ** 2)
    sig += 0.4 * rng.standard_normal(n)
    return sig, centers

bump_signal, bump_true = make_bump_signal()

# The detected maxima are NEAR the true centres but not exactly on them:
detected = find_peaks(bump_signal, prominence=1.0)[0]
nearest = [int(detected[np.argmin(np.abs(detected - c))]) for c in bump_true]
print(f"true centres      : {bump_true.tolist()}")
print(f"nearest detections: {nearest}   <- shifted by a few samples")""")

    md("""\
Now optimize on this bump signal at several tolerances and watch the best F1
climb as the tolerance starts to accommodate that shift:""")
    code("""\
for tol in (0, 1, 2, 3):
    o = OptimizedFindPeaks(scorer="f1", n_trials=80, tolerance=tol, seed=0)
    o.fit(bump_signal, bump_true)
    print(f"tolerance={tol}: best F1 = {o.best_score_:.3f}")""")

    md("""\
With `tolerance=0` no detection lands exactly on a centre, so F1 is 0 even though
the bumps are obviously found. As the tolerance grows to cover the ~1–3 sample
shift, every bump is credited and F1 reaches 1.0.

**Rule of thumb:** set `tolerance` to how precisely you need a peak localised —
too small unfairly penalises correct-but-shifted detections; too large credits
unrelated detections. A few samples is typical.""")

    # --------- Exercise 3
    md("""\
### Exercise 3

**Part A — by hand.** With true peaks at indices `10, 50, 90` (the `true_mask`
above) and predicted indices `np.array([8, 12, 48, 95])`, work out `TP`, `FP`,
`FN` for `tolerance=0` and `tolerance=2`. Remember matching is one-to-one. Then
check your answers with `_f1_components`.

**Part B — on the bump signal.** Fit two optimizers on `bump_signal`/`bump_true`
that are identical except for `tolerance` (use `0` and `3`; `n_trials=80`,
`seed=0`). Print both `best_score_` values and explain in a comment why the
`tolerance=3` score is higher.""")
    if solution:
        code("""\
# Part A — by hand, true peaks at 10, 50, 90, predicted [8, 12, 48, 95]:
#
#   tolerance=0: no predicted index equals 10/50/90 exactly.
#                TP=0, FP=4, FN=3
#
#   tolerance=2: 8 is 2 from 10 (match). 12 is also 2 from 10, but 10 is already
#                taken (one-to-one) -> 12 is a FP. 48 is 2 from 50 (match).
#                95 is 5 from 90 -> too far, FP.
#                TP=2, FP=2 (12 and 95), FN=1 (true peak 90).
predicted_ex = np.array([8, 12, 48, 95])
print("tolerance=0:", _f1_components(true_mask, predicted_ex, tolerance=0))  # (0, 4, 3)
print("tolerance=2:", _f1_components(true_mask, predicted_ex, tolerance=2))  # (2, 2, 1)

# Part B — same search, different tolerance.
opt_tol0 = OptimizedFindPeaks(scorer="f1", n_trials=80, tolerance=0, seed=0)
opt_tol0.fit(bump_signal, bump_true)
opt_tol3 = OptimizedFindPeaks(scorer="f1", n_trials=80, tolerance=3, seed=0)
opt_tol3.fit(bump_signal, bump_true)
print(f"best F1 @ tolerance=0: {opt_tol0.best_score_:.3f}")
print(f"best F1 @ tolerance=3: {opt_tol3.best_score_:.3f}")

# Why higher with tolerance=3: the detected maximum of each smooth bump sits a
# couple of samples away from the true centre. With tolerance=0 those shifted-
# but-correct detections score as FP+FN; with tolerance=3 they are credited as
# TP, so precision and recall (hence F1) rise to 1.0.""")
    else:
        code("""\
# Part A — write your by-hand TP/FP/FN here as a comment, then check:
#   tolerance=0: TP=?, FP=?, FN=?
#   tolerance=2: TP=?, FP=?, FN=?
predicted_ex = np.array([8, 12, 48, 95])
# print("tolerance=0:", _f1_components(...))
# print("tolerance=2:", _f1_components(...))

# Part B — fit two optimizers on bump_signal differing only in tolerance (0, 3).
# opt_tol0 = OptimizedFindPeaks(...)
# opt_tol3 = OptimizedFindPeaks(...)
# print(opt_tol0.best_score_, opt_tol3.best_score_)""")

    # ---------------------------------------------------------------- Sec 5
    md("""\
## 5. Other metrics and custom scorers

We are back to the anomaly `signal`/`true_peaks` from Section 1.

The built-in `scorer` strings are `"f1"`, `"precision"`, `"recall"` and
`"accuracy"`. Choose the one that matches your goal:

- `"recall"` — catch as many true peaks as possible (misses are costly).
- `"precision"` — avoid false alarms (extra detections are costly).
- `"f1"` — balance the two (a good default).

Optimizing different metrics changes the *character* of the solution even when
each reaches a high score, so we report **both** precision and recall of every
result to see the trade-off.""")
    code("""\
def pr_re(true_peaks, pred_peaks, tolerance=2):
    \"\"\"Helper: precision and recall of a set of detected peaks.\"\"\"
    mask = np.zeros(signal.size, dtype=bool)
    mask[true_peaks] = True
    tp, fp, fn = _f1_components(mask, pred_peaks, tolerance)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    return precision, recall

for metric in ("f1", "recall", "precision"):
    o = OptimizedFindPeaks(scorer=metric, n_trials=100, tolerance=2, seed=0)
    o.fit(signal, true_peaks)
    pk, _ = o.predict(signal)
    p, r = pr_re(true_peaks, pk)
    print(f"scorer={metric:9s}: {pk.size:3d} peaks | precision={p:.2f} recall={r:.2f}")""")

    md("""\
Notice the trade-off:

- **`recall`** floods the signal with detections (catches every anomaly, but
  many false alarms → low precision).
- **`precision`** keeps only the few most certain peaks (no false alarms, but
  misses real anomalies → low recall).
- **`f1`** balances the two and recovers exactly the right peaks.

You can also pass your **own** scorer: any callable with the signature
`scorer(true_mask, pred_peaks, n_samples) -> float`, where `true_mask` is the
boolean array of true peaks, `pred_peaks` are the detected indices, and
`n_samples` is the signal length. A custom scorer does its **own** matching — the
class's `tolerance` argument only applies to the built-in string metrics.""")
    code("""\
# A custom scorer: F1, but with a gentle penalty for detecting too many peaks.
def penalised_f1(true_mask, pred_peaks, n_samples):
    tp, fp, fn = _f1_components(true_mask, pred_peaks, tolerance=2)
    f1 = 2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) else 0.0
    n_true = int(true_mask.sum())
    overshoot = max(0, pred_peaks.size - n_true) / max(1, n_true)
    return f1 - 0.05 * overshoot

opt_custom = OptimizedFindPeaks(scorer=penalised_f1, n_trials=100, seed=0)
opt_custom.fit(signal, true_peaks)
print(f"Custom scorer: best score = {opt_custom.best_score_:.3f}, "
      f"found {opt_custom.predict(signal)[0].size} peaks")""")

    # --------- Exercise 4
    md("""\
### Exercise 4

1. Fit one optimizer with `scorer="precision"` and one with `scorer="recall"`
   (both `n_trials=100`, `tolerance=2`, `seed=0`). Plot both results with
   `plot_result` and note how many peaks each returns.
2. Write a custom scorer `recall_min_precision(true_mask, pred_peaks, n_samples)`
   that returns the **recall**, but `0.0` whenever precision drops below `0.5`
   (i.e. "maximise recall, but never let more than half the detections be false
   alarms"). Optimize with it and report the resulting number of peaks.""")
    if solution:
        code("""\
# 1. Precision vs recall.
opt_p = OptimizedFindPeaks(scorer="precision", n_trials=100, tolerance=2, seed=0)
opt_p.fit(signal, true_peaks)
opt_r = OptimizedFindPeaks(scorer="recall", n_trials=100, tolerance=2, seed=0)
opt_r.fit(signal, true_peaks)

peaks_p, _ = opt_p.predict(signal)
peaks_r, _ = opt_r.predict(signal)
plot_result(signal, true_peaks, peaks_p, f"Precision-optimized ({peaks_p.size} peaks)")
plot_result(signal, true_peaks, peaks_r, f"Recall-optimized ({peaks_r.size} peaks)")
# Precision-optimized: very few, highly confident detections (may miss anomalies).
# Recall-optimized: many detections to catch every anomaly (many false alarms).


# 2. Custom scorer: recall, gated by a minimum precision of 0.5.
def recall_min_precision(true_mask, pred_peaks, n_samples):
    tp, fp, fn = _f1_components(true_mask, pred_peaks, tolerance=2)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    return recall if precision >= 0.5 else 0.0

opt_gated = OptimizedFindPeaks(scorer=recall_min_precision, n_trials=150, seed=0)
opt_gated.fit(signal, true_peaks)
peaks_g, _ = opt_gated.predict(signal)
print(f"Gated scorer: best score = {opt_gated.best_score_:.3f}, found {peaks_g.size} peaks")
plot_result(signal, true_peaks, peaks_g, "Recall, constrained to precision >= 0.5")""")
    else:
        code("""\
# 1. Fit precision- and recall-optimized optimizers, predict, and plot both.
# opt_p = OptimizedFindPeaks(scorer="precision", ...)
# opt_r = OptimizedFindPeaks(scorer="recall", ...)
# ...

# 2. Write recall_min_precision(true_mask, pred_peaks, n_samples):
#    return the recall, but 0.0 if precision < 0.5. Then optimize with it.
def recall_min_precision(true_mask, pred_peaks, n_samples):
    ...

# opt_gated = OptimizedFindPeaks(scorer=recall_min_precision, ...)
# opt_gated.fit(signal, true_peaks)""")

    # ---------------------------------------------------------------- Wrap up
    md("""\
## Summary

- `OptimizedFindPeaks(scorer, search_space, fixed_params, n_trials, tolerance,
  seed).fit(signal, true_peaks)` tunes `find_peaks` with Optuna.
- Read results from `best_params_` / `best_score_`; apply them with
  `predict(signal)` or reuse `find_peaks_kwargs()` on new data.
- `fixed_params` pins parameters; `search_space` controls what is searched and
  how (linear vs `{"log": True}`, float vs int). The default tunes `height`,
  `prominence` and `distance`.
- **`tolerance`** is the index wiggle-room for counting a detected peak as a
  match to a true peak (greedy, one-to-one). It shapes the *score*, not the
  detection.
- Pick `scorer` to match your priority (`precision` / `recall` / `f1`) or supply
  a custom callable.""")

    nb = new_notebook(cells=cells)
    nb.metadata["language_info"] = {"name": "python"}
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    return nb


for solution in (False, True):
    nb = build(solution)
    name = "optimized_find_peaks_solution" if solution else "optimized_find_peaks_tutorial"
    with open(f"{name}.ipynb", "w") as f:
        nbf.write(nb, f)
    print(f"wrote {name}.ipynb ({len(nb.cells)} cells)")

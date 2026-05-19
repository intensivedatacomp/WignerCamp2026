import pytest
import optuna

from optuna_task import (
    task_1_objective,
    task_2_objective,
    task_3_run_optimization,
    task_4_subset_objective,
)

optuna.logging.set_verbosity(optuna.logging.WARNING)


############################
# Task 1 — single-valued objective
############################
def _run_task1(n_trials: int = 100, seed: int = 42) -> optuna.Study:
    study = optuna.create_study(
        direction='minimize',
        sampler=optuna.samplers.TPESampler(seed=seed),
    )
    study.optimize(task_1_objective, n_trials=n_trials)
    return study


def test_task_1_returns_float():
    """Objective must return a single float, not a tuple."""
    study = optuna.create_study(direction='minimize')
    study.optimize(task_1_objective, n_trials=1)
    assert isinstance(study.best_value, float)


def test_task_1_best_value_close_to_zero():
    """With 100 trials the best value must be well below 0.01."""
    study = _run_task1()
    assert study.best_value < 0.01


def test_task_1_best_x_close_to_two():
    """Best x must be within 0.2 of the true optimum 2."""
    study = _run_task1()
    assert abs(study.best_params['x'] - 2.0) < 0.2


def test_task_1_best_y_close_to_minus_three():
    """Best y must be within 0.2 of the true optimum -3."""
    study = _run_task1()
    assert abs(study.best_params['y'] - (-3.0)) < 0.2


def test_task_1_params_named_x_and_y():
    """Objective must suggest parameters named 'x' and 'y'."""
    study = _run_task1(n_trials=5)
    assert 'x' in study.best_params
    assert 'y' in study.best_params


############################
# Task 2 — log-scale float and categorical objective
############################
_FUNC_CHOICES = ['square', 'sqrt', 'log10']


def _run_task2(n_trials: int = 100, seed: int = 42) -> optuna.Study:
    study = optuna.create_study(
        direction='minimize',
        sampler=optuna.samplers.TPESampler(seed=seed),
    )
    study.optimize(task_2_objective, n_trials=n_trials)
    return study


def test_task_2_returns_float():
    """Objective must return a single float."""
    study = optuna.create_study(direction='minimize')
    study.optimize(task_2_objective, n_trials=1)
    assert isinstance(study.best_value, float)


def test_task_2_best_value_close_to_zero():
    """With 100 trials the best value must be well below 0.001."""
    study = _run_task2()
    assert study.best_value < 0.001


def test_task_2_param_alpha_in_range():
    """Best alpha must lie within the declared log-scale range [1e-4, 1e2]."""
    study = _run_task2()
    alpha = study.best_params['alpha']
    assert 1e-4 <= alpha <= 1e2


def test_task_2_param_func_is_valid_choice():
    """Best func must be one of the three declared categorical choices."""
    study = _run_task2()
    assert study.best_params['func'] in _FUNC_CHOICES


def test_task_2_params_named_alpha_and_func():
    """Objective must suggest parameters named 'alpha' and 'func'."""
    study = _run_task2(n_trials=5)
    assert 'alpha' in study.best_params
    assert 'func' in study.best_params


############################
# Task 3 — full workflow
############################
def _simple_objective(trial: optuna.Trial) -> float:
    """Fixed test objective: minimizes (x - 5)^2, true minimum 0 at x=5."""
    x = trial.suggest_float('x', -10.0, 10.0)
    return (x - 5.0) ** 2


def test_task_3_returns_tuple():
    """Return value must be a tuple of length 2."""
    result = task_3_run_optimization(_simple_objective, n_trials=50, seed=42)
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_task_3_best_params_is_dict():
    """First element of return value must be a dict."""
    best_params, _ = task_3_run_optimization(_simple_objective, n_trials=50, seed=42)
    assert isinstance(best_params, dict)


def test_task_3_best_value_is_float():
    """Second element of return value must be a float."""
    _, best_value = task_3_run_optimization(_simple_objective, n_trials=50, seed=42)
    assert isinstance(best_value, float)


def test_task_3_best_value_close_to_zero():
    """With 50 trials the best value must be well below 0.01."""
    _, best_value = task_3_run_optimization(_simple_objective, n_trials=50, seed=42)
    assert best_value < 0.01


def test_task_3_best_x_close_to_five():
    """Best x must be within 0.5 of the true optimum 5."""
    best_params, _ = task_3_run_optimization(_simple_objective, n_trials=50, seed=42)
    assert abs(best_params['x'] - 5.0) < 0.5


def test_task_3_reproducible():
    """Two calls with the same seed must return identical results."""
    result1 = task_3_run_optimization(_simple_objective, n_trials=50, seed=42)
    result2 = task_3_run_optimization(_simple_objective, n_trials=50, seed=42)
    assert result1[1] == result2[1]
    assert result1[0] == result2[0]


def test_task_3_different_seeds_may_differ():
    """Different seeds should generally produce different best_params."""
    _, v1 = task_3_run_optimization(_simple_objective, n_trials=50, seed=0)
    _, v2 = task_3_run_optimization(_simple_objective, n_trials=50, seed=1)
    # Both should still find a near-zero value
    assert v1 < 0.01
    assert v2 < 0.01


############################
# Task 4 — subset selection with binary mask
############################
_LST_A = [-3, 1, 2, 5, 10]
_TARGET_A = 0

_LST_B = [-4, 1, 2, 3, 7]
_TARGET_B = 3


def _run_task4(lst, target, n_trials=200, seed=42) -> optuna.Study:
    study = optuna.create_study(
        direction='minimize',
        sampler=optuna.samplers.TPESampler(seed=seed),
    )
    study.optimize(
        lambda trial: task_4_subset_objective(trial, lst, target),
        n_trials=n_trials,
    )
    return study


def test_task_4_best_value_is_zero_case_a():
    """Exact subset [-3, 1, 2] sums to 0, so best_value must be 0."""
    study = _run_task4(_LST_A, _TARGET_A)
    assert study.best_value == 0.0


def test_task_4_selected_sum_equals_target_case_a():
    """The elements chosen by the best mask must sum to target=0."""
    study = _run_task4(_LST_A, _TARGET_A)
    mask = [study.best_params[f'include_{i}'] for i in range(len(_LST_A))]
    selected = [v for v, keep in zip(_LST_A, mask) if keep]
    assert sum(selected) == _TARGET_A


def test_task_4_best_value_is_zero_case_b():
    """A sublist of [-4, 1, 2, 3, 7] summing to 3 must be found."""
    study = _run_task4(_LST_B, _TARGET_B, seed=0)
    assert study.best_value == 0.0


def test_task_4_selected_sum_equals_target_case_b():
    """The elements chosen by the best mask must sum to target=3."""
    study = _run_task4(_LST_B, _TARGET_B, seed=0)
    mask = [study.best_params[f'include_{i}'] for i in range(len(_LST_B))]
    selected = [v for v, keep in zip(_LST_B, mask) if keep]
    assert sum(selected) == _TARGET_B


def test_task_4_params_named_with_include_prefix():
    """Each element must produce a parameter named 'include_<i>'."""
    study = _run_task4(_LST_A, _TARGET_A, n_trials=10)
    for i in range(len(_LST_A)):
        assert f'include_{i}' in study.trials[0].params


def test_task_4_empty_subset_returns_inf():
    """When all mask entries are False the function must return float('inf')."""
    class _AllFalseTrial:
        def suggest_categorical(self, name, choices):
            return False

    result = task_4_subset_objective(_AllFalseTrial(), _LST_A, _TARGET_A)
    assert result == float('inf')

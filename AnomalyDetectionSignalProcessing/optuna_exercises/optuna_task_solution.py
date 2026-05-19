import math
import optuna


###################
#     Task 1      #
###################
def task_1_objective(trial: optuna.Trial) -> float:
    """
    Define a single-valued objective function to minimize.

    The objective is:

        f(x, y) = (x - 2)**2 + (y + 3)**2

    for x in [-5, 5] and y in [-5, 5]. The true minimum is
    f = 0 at (x, y) = (2, -3).

    Parameters
    ----------
    trial : optuna.Trial
        The Optuna trial object used to suggest parameter values.

    Returns
    -------
    float
        The objective value f(x, y).

    Notes
    -----
    Use trial.suggest_float to sample x and y.
    """
    x = trial.suggest_float('x', -5.0, 5.0)
    y = trial.suggest_float('y', -5.0, 5.0)
    return (x - 2.0) ** 2 + (y + 3.0) ** 2


###################
#     Task 2      #
###################
def task_2_objective(trial: optuna.Trial) -> float:
    """
    Define a single-valued objective using a log-scale float and a categorical.

    The objective is:

        f(alpha, func) = (g_func(alpha) - 1.5)**2

    where alpha is sampled on a log scale from [1e-4, 1e2] and g_func is
    selected from three choices:

        'square' : g(alpha) = alpha**2       optimal alpha = sqrt(1.5)  ~ 1.225
        'sqrt'   : g(alpha) = alpha**0.5     optimal alpha = 1.5**2     = 2.25
        'log10'  : g(alpha) = log10(alpha)   optimal alpha = 10**1.5    ~ 31.62

    All three choices can reach f = 0, but each requires a very different
    optimal alpha. The log scale for alpha is important because these optimal
    values span more than an order of magnitude.

    Parameters
    ----------
    trial : optuna.Trial
        The Optuna trial object used to suggest parameter values.

    Returns
    -------
    float
        The objective value f(alpha, func).

    Notes
    -----
    Use trial.suggest_float('alpha', 1e-4, 1e2, log=True) to sample alpha
    and trial.suggest_categorical to choose func from
    ['square', 'sqrt', 'log10'].
    """
    alpha = trial.suggest_float('alpha', 1e-4, 1e2, log=True)
    func = trial.suggest_categorical('func', ['square', 'sqrt', 'log10'])
    if func == 'square':
        value = alpha ** 2
    elif func == 'sqrt':
        value = alpha ** 0.5
    else:
        value = math.log10(alpha)
    return (value - 1.5) ** 2


###################
#     Task 3      #
###################
def task_3_run_optimization(
    objective,
    n_trials: int,
    seed: int,
) -> tuple[dict, float]:
    """
    Run a full single-objective minimization with a fixed random seed.

    Parameters
    ----------
    objective : callable
        An Optuna objective function that takes a trial and returns a float.
    n_trials : int
        Number of trials to run.
    seed : int
        Random seed passed to TPESampler for reproducibility.

    Returns
    -------
    best_params : dict
        The parameter names and values of the best trial.
    best_value : float
        The best objective value found.

    Notes
    -----
    Steps to implement:

    1. Create a study with direction='minimize' using
       optuna.samplers.TPESampler(seed=seed).
    2. Call study.optimize(objective, n_trials=n_trials).
    3. Return (study.best_params, study.best_value).
    """
    sampler = optuna.samplers.TPESampler(seed=seed)
    study = optuna.create_study(direction='minimize', sampler=sampler)
    study.optimize(objective, n_trials=n_trials)
    return study.best_params, study.best_value


###################
#     Task 4      #
###################
def task_4_subset_objective(
    trial: optuna.Trial,
    lst: list[float],
    target: float,
) -> float:
    """
    Define a subset-selection objective using a binary mask.

    For each index i, suggest a boolean named 'include_i' using
    trial.suggest_categorical with choices [True, False]. Collect the
    elements of lst where the mask is True into selected:

        selected = [lst[i] for i if include_i is True]

    The objective measures how close the subset sum is to the target:

        f(mask) = abs(sum(selected) - target)

    Parameters
    ----------
    trial : optuna.Trial
        The Optuna trial object.
    lst : list of float
        The pool of candidate elements.
    target : float
        The desired sum.

    Returns
    -------
    float
        abs(sum(selected) - target), or float('inf') if nothing is selected.

    Notes
    -----
    Wrap this function in a lambda when passing to study.optimize:

        study.optimize(
            lambda trial: task_4_subset_objective(trial, lst, target), ...
        )
    """
    mask = [
        trial.suggest_categorical(f'include_{i}', [True, False])
        for i in range(len(lst))
    ]
    selected = [v for v, keep in zip(lst, mask) if keep]
    if not selected:
        return float('inf')
    return abs(sum(selected) - target)


def main():
    optuna.logging.set_verbosity(optuna.logging.WARNING)

    # Task 1
    study1 = optuna.create_study(
        direction='minimize',
        sampler=optuna.samplers.TPESampler(seed=42),
    )
    study1.optimize(task_1_objective, n_trials=100)
    print(
        f"Task 1 | best x={study1.best_params['x']:.4f}, "
        f"y={study1.best_params['y']:.4f}, "
        f"value={study1.best_value:.6f}  (true minimum: 0 at x=2, y=-3)"
    )

    # Task 2
    study2 = optuna.create_study(
        direction='minimize',
        sampler=optuna.samplers.TPESampler(seed=42),
    )
    study2.optimize(task_2_objective, n_trials=100)
    print(
        f"Task 2 | func={study2.best_params['func']!r}, "
        f"alpha={study2.best_params['alpha']:.6f}, "
        f"value={study2.best_value:.2e}  (true minimum: 0)"
    )

    # Task 3
    def simple_objective(trial):
        x = trial.suggest_float('x', -10.0, 10.0)
        return (x - 5.0) ** 2

    best_params, best_value = task_3_run_optimization(simple_objective, n_trials=50, seed=42)
    print(
        f"Task 3 | best_params={best_params}, "
        f"best_value={best_value:.6f}  (true minimum: 0 at x=5)"
    )

    # Task 4
    LST = [-3.0, 1.0, 2.0, 5.0, 10.0]
    TARGET = 0
    study4 = optuna.create_study(
        direction='minimize',
        sampler=optuna.samplers.TPESampler(seed=42),
    )
    study4.optimize(
        lambda trial: task_4_subset_objective(trial, LST, TARGET),
        n_trials=200,
    )
    mask = [study4.best_params[f'include_{i}'] for i in range(len(LST))]
    selected = [v for v, keep in zip(LST, mask) if keep]
    print(
        f"Task 4 | selected={selected}, "
        f"sum={sum(selected)}, target={TARGET}  (expected: [-3.0, 1.0, 2.0])"
    )


if __name__ == "__main__":
    main()

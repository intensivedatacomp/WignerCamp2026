# Optuna Exercises

## Goal

In this exercise you will practise the Optuna hyperparameter optimization workflow covered in the presentation using simple mathematical functions.

You will complete the missing implementations in [optuna_task.py](optuna_task.py).

## What you will learn

- How to define a single-valued objective function with `trial.suggest_float` and `trial.suggest_int`.
- How to define more complicated objectives.
- How to run the full Optuna workflow: creating a study, optimizing, and reading results.
- How to use a binary mask to select an unknown-length sublist from a fixed list.
- How to fix the random seed with `TPESampler` to make results reproducible.

## Tasks

### Task 1 — Single-valued objective function

Complete `task_1_objective(trial)` in [optuna_task.py](optuna_task.py).

Define an objective function that minimizes:

```
f(x, y) = (x - 2)^2 + (y + 3)^2
```

for `x` in `[-5, 5]` and `y` in `[-5, 5]`.

Use `trial.suggest_float` to sample both parameters.
Return the scalar value `f(x, y)`.

The true minimum is `f = 0` at `(x, y) = (2, -3)`.

### Task 2 — Objective with a log-scale float and a categorical

Complete `task_2_objective(trial)` in [optuna_task.py](optuna_task.py).

Define a single-valued objective:

```
f(alpha, func) = (g_func(alpha) - 1.5)**2
```

where `alpha` is sampled on a **log scale** from `[1e-4, 1e2]` and `func` is chosen
from `['square', 'sqrt', 'log10']`:

```
'square' : g(alpha) = alpha**2       optimal alpha = sqrt(1.5)  ~ 1.225
'sqrt'   : g(alpha) = alpha**0.5     optimal alpha = 1.5**2     = 2.25
'log10'  : g(alpha) = log10(alpha)   optimal alpha = 10**1.5    ~ 31.62
```

The true minimum is `f = 0` for all three function choices.
Use `trial.suggest_float('alpha', 1e-4, 1e2, log=True)` and
`trial.suggest_categorical` to implement the objective.

The log scale is important here: the optimal `alpha` values for the three functions
span more than an order of magnitude, so a linear scale would cluster most samples
far from the true optimum.

### Task 3 — Full optimization workflow

Complete `task_3_run_optimization(objective, n_trials, seed)` in [optuna_task.py](optuna_task.py).

Implement the full single-objective minimization workflow:

1. Create a study with `direction='minimize'` using `optuna.samplers.TPESampler(seed=seed)` for reproducibility.
2. Call `study.optimize(objective, n_trials=n_trials)`.
3. Return the tuple `(study.best_params, study.best_value)`.

### Task 4 — Subset selection with a binary mask

Complete `task_4_subset_objective(trial, lst, target)` in [optuna_task.py](optuna_task.py).

For each element `lst[i]`, suggest a boolean named `'include_i'` (e.g. `'include_0'`, `'include_1'`, …) using `trial.suggest_categorical`.
Collect the elements where the mask is `True` into `selected`.

- If `selected` is empty, return `float('inf')`.
- Otherwise return `abs(sum(selected) - target)`.

The optimization finds the sublist of `lst` whose sum is closest to `target`.

**Example**: with `lst = [-3, 1, 2, 5, 10]` and `target = 0`, the optimal sublist is `[-3, 1, 2]` (sum = 0).

## Running locally

You can run the task file directly to see the output of your implementations:

```bash
python optuna_task.py
```

## Testing

Run the test suite from inside this directory with:

```bash
pytest
```

All tasks must pass before you check the solutions.

## Check solutions

After all tests pass, compare your implementations with [optuna_task_solution.py](optuna_task_solution.py).

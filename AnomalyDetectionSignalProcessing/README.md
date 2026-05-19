# Anomaly Detection — Signal Processing

Materials for the signal processing part of the Anomaly Detection project track at the 2026 Wigner Summer Camp.

## Contents

### Presentations

#### `find_peaks` — Peak Detection with SciPy ([find_peaks.pdf](find_peaks.pdf))

A slide-based presentation introducing `scipy.signal.find_peaks` for detecting peaks in 1D signals.

Topics covered:

- What a peak is and how signals are represented as arrays.
- Filtering by **value**: the `height` parameter (minimum peak height, or a `(min, max)` interval).
- Filtering by **distance**: the `distance` parameter (minimum number of samples between peaks).
- **Prominence**: how far a peak stands out from its surroundings; the `prominence` parameter.
- **Width**: peak width at a given relative height; the `width` and `rel_height` parameters.
- **Plateau size**: detecting flat-topped peaks with the `plateau_size` parameter.
- Combining multiple parameters to isolate exactly the peaks of interest.

Code examples are in [find_peaks.py](find_peaks.py).

---

#### Bayesian Hyperparameter Optimization with Optuna (notebook: [optuna_presentation.ipynb](optuna_presentation.ipynb) and presentation: [optuna_presentation.slides.html](optuna_presentation.slides.html))

A Jupyter notebook presentation introducing the Optuna library for Bayesian hyperparameter optimization.
All examples use simple mathematical functions — no machine learning model is required.

Topics covered:

- What Optuna is and why Bayesian optimization outperforms grid and random search.
- The core workflow: `create_study`, `optimize`, `best_params`, `best_value`.
- Suggesting parameter types: `suggest_float`, `suggest_int`, `suggest_categorical`.
- Log-scale sampling with `suggest_float(..., log=True)`.
- Choosing elements from a predefined list using `suggest_categorical`.
- Selecting an unknown-length sublist with a binary mask.
- Fixing the random seed with `TPESampler(seed=...)` for reproducible results.
- Visualizing the optimization history.

Run the notebook locally with Jupyter Lab or VS Code, or open it in Google Colab.
To export as slides:

```bash
jupyter nbconvert --to slides optuna_presentation.ipynb
```

---

### Exercises

#### Optuna Exercises ([optuna_exercises/](optuna_exercises/))

Hands-on coding exercises to practise the Optuna workflow.
See [optuna_exercises/README.md](optuna_exercises/README.md) for detailed task descriptions.

| File | Purpose |
|---|---|
| `optuna_task.py` | Task stubs to complete |
| `optuna_task_solution.py` | Reference solutions |
| `test_optuna_task.py` | Pytest suite (23 tests) |

Tasks:

1. Define a single-valued objective function using `suggest_float`.
2. Define an objective with a log-scale float and a categorical parameter.
3. Implement the full optimization workflow and return `best_params` and `best_value`.
4. Select a sublist with an unknown length using a binary mask.

Run the exercises from inside the folder:

```bash
cd optuna_exercises
python optuna_task.py   # see output of your implementation
pytest                  # validate with the test suite
```

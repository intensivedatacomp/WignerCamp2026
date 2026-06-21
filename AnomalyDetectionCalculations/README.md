# Anomaly Detection — Calculations

Hands-on materials that tie the Anomaly Detection track together: using **Optuna** to automatically tune `scipy.signal.find_peaks` so that detected peaks match known anomaly locations.

## 📄 Contents

- [🧠 `optimized_find_peaks.py`](./optimized_find_peaks.py) — the `OptimizedFindPeaks` class, a thin wrapper around `scipy.signal.find_peaks` that uses Optuna to search for the parameter set (`height`, `prominence`, `distance`, ...) that best recovers a set of ground-truth peak locations. Optimizes a classification metric (F1 by default) between detected peaks and the true anomaly positions.
- [📓 `optimized_find_peaks_tutorial.ipynb`](./optimized_find_peaks_tutorial.ipynb) — student tutorial notebook with tasks to complete.
- [📓 `optimized_find_peaks_solution.ipynb`](./optimized_find_peaks_solution.ipynb) — reference solution to the tutorial.
- [📓 `generate_data_peaks_baseline.ipynb`](./generate_data_peaks_baseline.ipynb) — generates the baseline signal/peak data used by the tutorial.
- [`_make_notebooks.py`](./_make_notebooks.py) — regenerates the tutorial and solution notebooks from plain text, so they can be edited without hand-editing notebook JSON. Run once inside the `WignerCampEnv` environment:

  ```bash
  python _make_notebooks.py
  ```

The notebooks pull the latest `optimized_find_peaks.py` from the public GitHub repo, so they also run on Google Colab.

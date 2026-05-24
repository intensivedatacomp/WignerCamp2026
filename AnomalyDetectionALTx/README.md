# `ALTx` introduction

This folder contains self-contained examples that illustrate how the **Adaptive Law-based Transformation (ALT)** method works using toy datasets. The examples are presented in both **notebook** and **presentation** formats and cover the full ALT pipeline for both **time series classification** and **anomaly detection**.

## 📄 Contents

- [📓 `presentation_calculation.ipynb`](./presentation_calculation.ipynb)  
  A Jupyter notebook that demonstrates the steps of ALT for **classification** with executable code and explanations:
  - Sequence generation using linear recursion
  - Shapelet (law) extraction via eigenvector decomposition
  - Embedding and transformation of the test instance
  - Feature computation and classification  
  → Perfect for interactive exploration or educational use.

- [📓 `altx_intro.ipynb`](./altx_intro.ipynb)  
  A companion notebook used alongside the presentation for hands-on exercises.

- [📓 `altx_anomaly.ipynb`](./altx_anomaly.ipynb)  
  A Jupyter notebook demonstrating ALT for **anomaly detection**:
  - Generating a normal time series and injecting anomalies
  - Extracting laws from normal data only
  - Computing a per-window anomaly score vector
  - Localising anomalies via threshold comparison

- [🧠 `functions.py`](./functions.py)  
  Python helper functions used by the notebooks. Includes:
  - `generate_recursive_array`: create synthetic time series from recurrence rules
  - `extract_symmetric_laws`: extract shapelet vectors (laws)
  - `embed_as_pairs`: perform 2D time-delay embedding

- [🎤 `altx.tex`](./altx.tex)  
  The LaTeX Beamer source file of the presentation. Covers classification, the parameters \(r, l, k\), and a dedicated **anomaly detection** section with numerical examples and exercises.

- [📑 `altx.pdf`](./altx.pdf)  
  The compiled version of the LaTeX presentation. Useful for quick reviews or showing slides.

## 🧠 About ALT

ALT (Adaptive Law-based Transformation) is a lightweight and interpretable feature extraction technique for time series. It:
- Learns governing *linear laws* from the data via time-delay embedding and eigenvalue decomposition.
- Transforms time series into a feature space using projections to these laws.
- Applies simple statistical indicators to perform **classification** or **anomaly detection**.

For anomaly detection, laws are extracted from normal data only, and a per-window score vector is computed. Peaks in this vector — values exceeding a chosen threshold — mark the anomaly locations.

The method requires only a few hyperparameters:  
- **`r`**: length of the time window,  
- **`l`**: embedding size (number of delay coordinates),  
- **`k`**: shift step between windows.

## 📚 References

- **ALT Preprint**  
Kurbucz, M.T., Hajós, B., Halmos, B.P., Molnár, V.Á., Jakovác A. Adaptive law-based feature representation for time series classification. *Sci Rep* **15** 41775 (2025). [https://doi.org/10.1038/s41598-025-25667-0](https://doi.org/10.1038/s41598-025-25667-0)

- **ALT Software Package**  
Balázs Paszkál Halmos, Balázs Hajós, Vince Áron Molnár, Marcell Tamás Kurbucz, Antal Jakovác, `altx`: a python package for adaptive law-based transformation in time series classification, *Mach. Learn.: Sci. Technol.* **7** 015034 (2026) [https://doi.org/10.1088/2632-2153/ae3e4f](https://doi.org/10.1088/2632-2153/ae3e4f)

- **ALT Source Code**  
  GitHub repository: [github.com/dcintlab/altx](https://github.com/dcintlab/altx)
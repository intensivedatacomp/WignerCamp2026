# `ALTx` introduction

This folder contains a simple, self-contained example that illustrates how the **Adaptive Law-based Transformation (ALT)** method works using a toy dataset. The example is presented in both **notebook** and **presentation** formats and walks through the full ALT pipeline: from generating synthetic time series to classifying an unknown test instance using extracted linear laws.

## 📄 Contents

- [📓 `presentation_calculation.ipynb`](./presentation_calculation.ipynb)  
  A Jupyter notebook that demonstrates the steps of ALT with executable code and explanations:
  - Sequence generation using linear recursion
  - Shapelet (law) extraction via eigenvector decomposition
  - Embedding and transformation of the test instance
  - Feature computation and classification  
  → Perfect for interactive exploration or educational use.

- [🧠 `functions.py`](./functions.py)  
  Python helper functions used by the notebook. Includes:
  - `generate_recursive_array`: create synthetic time series from recurrence rules
  - `extract_symmetric_laws`: extract shapelet vectors (laws)
  - `embed_as_pairs`: perform 2D time-delay embedding

- [🎤 `altx.tex`](./altx.tex)  
  The LaTeX Beamer source file of the presentation that mirrors the notebook content in slide format.

- [📑 `altx.pdf`](./altx.pdf)  
  The compiled version of the LaTeX presentation. Useful for quick reviews or showing slides.

## 🧠 About ALT

ALT (Adaptive Law-based Transformation) is a lightweight and interpretable feature extraction technique for time series classification. It:
- Learns governing *linear laws* from the data via time-delay embedding and eigenvalue decomposition.
- Transforms time series into a feature space using projections to these laws.
- Applies simple statistical indicators to perform classification.

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

## 🚀 Try it Online

Click to open the notebook in Google Colab:  
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Datacompintensive/WignerCamp2025/blob/master/ALT/presentation_calculation.ipynb)

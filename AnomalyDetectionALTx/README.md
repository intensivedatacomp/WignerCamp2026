# ALT Presentation Example

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

- [🎤 `ALT.tex`](./ALT.tex)  
  The LaTeX Beamer source file of the presentation that mirrors the notebook content in slide format.

- [📑 `ALT.pdf`](./ALT.pdf)  
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
  *Marcell T. Kurbucz, Balázs Hajós, Balázs P. Halmos, Vince Á. Molnár, Antal Jakovác*.  
  *Adaptive Law-Based Transformation (ALT): A Lightweight Feature Representation for Time Series Classification.*  
  arXiv preprint: [arXiv:2501.09217](https://arxiv.org/abs/2501.09217) (2025).

- **ALT Software Package**  
  *Balázs P. Halmos, Balázs Hajós, Vince Á. Molnár, Marcell T. Kurbucz, Antal Jakovác*.  
  *ALT: A Python Package for Lightweight Feature Representation in Time Series Classification.*  
  arXiv preprint: [arXiv:2504.12841](https://arxiv.org/abs/2504.12841) (2025).

- **ALT Source Code**  
  GitHub repository: [github.com/Datacompintensive/ALT](https://github.com/Datacompintensive/ALT)

## 🚀 Try it Online

Click to open the notebook in Google Colab:  
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Datacompintensive/WignerCamp2025/blob/master/ALT/presentation_calculation.ipynb)

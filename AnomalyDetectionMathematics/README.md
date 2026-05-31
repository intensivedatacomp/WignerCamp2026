# Mathematics for Anomaly Detection

This folder contains a linear algebra introduction lecture and a hands-on PyTorch exercise used in the Wigner Summer Camp.

## Contents

```
AnomalyDetectionMathematics/
├── linear_algebra.tex          # LaTeX source of the presentation
├── linear_algebra.pdf          # Compiled presentation (PDF)
├── CMakeLists.txt              # Build file for compiling the PDF
└── mathematics_exercise/       # PyTorch coding exercise
    ├── README.md
    ├── linalg_task.py          # Exercise template (functions to complete)
    ├── linalg_task_solution.py # Reference solutions
    └── test_linalg_task.py     # pytest test suite
```

## Presentations

**Source:** [linear_algebra.tex](linear_algebra.tex) | **Compiled PDF:** [linear_algebra.pdf](linear_algebra.pdf)

The presentation introduces the linear algebra concepts needed for anomaly detection. It covers the following topics:

- **Vectors** — notation, standard basis vectors, the zero vector.
- **Dot product** — definition, geometric interpretation, practice exercises with solutions.
- **Matrices** — definition, types (square and non-square), vector-matrix multiplication.
- **Transformations** — stretching, rotation, reflection, and projection as matrix operations; exercises with solutions.
- **Matrix-matrix multiplication** — general formula and worked examples.
- **Eigenvalues and eigenvectors** — definition, key properties, and the eigenvalue equation.
- **Eigendecomposition with PyTorch** — using `torch.linalg.eigh` for real symmetric matrices, scaling unit eigenvectors to integer form, exercise with solution.

**Source:** [accuracy.tex](accuracy.tex) | **Compiled PDF:** [accuracy.pdf](accuracy.pdf)

Presentation which describes the evaluation of accuracy of classification and anomaly detection. It covers the following topics:

- **Confusion matrix** — matrix of the result of a classification.
- **Accuracy** — Proportion of all correct predictions.
- **Precision** — TP/(TP + FP): Fraction of predicted positives that are true positives.
- **Recall** — TP/(TP + FN): Fraction of actual positives that are correctly identified.
- **F1-score** — Harmonic mean of precision and recall.

### Compiling the PDF

Using CMake (recommended):

```bash
cd ..
rm -rf build
mkdir -p build
cd build
cmake -DBUILD_DOCS=ON -DBUILD_NOTEBOOKS=ON ..
cmake --build . -j4
```

Or directly with pdflatex:

```bash
pdflatex linear_algebra.tex
rm *.aux *.log *.nav *.out *.snm *.toc *.vrb
```

## Exercise

**Folder:** [mathematics_exercise/](mathematics_exercise/) | **Exercise README:** [mathematics_exercise/README.md](mathematics_exercise/README.md)

A self-contained coding exercise that reinforces the presentation material using PyTorch tensors. Complete the five functions in [mathematics_exercise/linalg_task.py](mathematics_exercise/linalg_task.py):

| Task | Description | PyTorch API |
|------|-------------|-------------|
| 1 | Multiply a vector by a scalar | `s * v` |
| 2 | Dot product of two vectors | `torch.dot(a, b)` |
| 3 | Vector–matrix multiplication | `v @ M` |
| 4 | Matrix–matrix multiplication | `A @ B` |
| 5 | Eigenvalues and eigenvectors of a real symmetric matrix | `torch.linalg.eigh(A)` |

### Running the exercise

```bash
cd mathematics_exercise
python linalg_task.py
```

### Testing

```bash
cd mathematics_exercise
pytest
```

### Solutions

Reference implementations are in [mathematics_exercise/linalg_task_solution.py](mathematics_exercise/linalg_task_solution.py).

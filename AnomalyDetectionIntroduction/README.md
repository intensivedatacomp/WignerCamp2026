# Anomaly Detection — Introduction

Opening presentation for the **Anomaly Detection** project track at the 2026 Wigner Summer Camp. It motivates the project and gives a high-level overview before students dive into the mathematics, the `altx` method, and signal processing.

## 📄 Contents

- [📑 `AnomalyDetectionIntroduction.pdf`](./AnomalyDetectionIntroduction.pdf) — the compiled slides.
- [🎤 `AnomalyDetectionIntroduction.tex`](./AnomalyDetectionIntroduction.tex) — the LaTeX Beamer source. Sections:
  - *Why Anomaly Detection?*
  - *From Data to Anomalies*
  - *Detecting Anomalies*
- [📓 `generate_introduction_figures.ipynb`](./generate_introduction_figures.ipynb) — Jupyter notebook that generates the figures used in the slides (saved into the shared [`img/`](../img) folder).
- [`CMakeLists.txt`](./CMakeLists.txt) — build rules so the slides are compiled by the top-level CMake build.

## 🔧 Building the slides

From the repository root:

```bash
rm -rf build && mkdir -p build && cd build
cmake -DBUILD_DOCS=ON ..
cmake --build . -j4
cd -
```

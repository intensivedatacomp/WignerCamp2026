# Introduction to Image Processing

Opening presentation for the **Edge Detection** project track at the 2026 Wigner Summer Camp. It introduces the research group's robust edge detection method for robot vision and frames the summer camp project.

## 📄 Contents

- [📑 `IntroductionToImageProcessing.pdf.pdf`](./IntroductionToImageProcessing.pdf.pdf) — the compiled slides.
- [🎤 `IntroductionToImageProcessing.tex`](./IntroductionToImageProcessing.tex) — the LaTeX Beamer source (*Robust Edge Detection for Robot Vision*). Sections:
  - *Motivation*
  - *The Problem*
  - *Our Method*
  - *Results*
  - *Summer Camp Project*

## 🔧 Building the slides

From the repository root:

```bash
rm -rf build && mkdir -p build && cd build
cmake -DBUILD_DOCS=ON ..
cmake --build . -j4
cd -
```

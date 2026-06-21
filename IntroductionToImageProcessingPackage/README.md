# Introduction to the Image Processing Package

Presentation introducing the [`image-processing`](https://github.com/intensivedatacomp/image-processing) package that implements the edge detection method used in the **Edge Detection** project track.

## 📄 Contents

- [📑 `IntroductionToImageProcessingPackage.pdf`](./IntroductionToImageProcessingPackage.pdf) — the compiled slides.
- [🎤 `IntroductionToImageProcessingPackage.tex`](./IntroductionToImageProcessingPackage.tex) — the LaTeX Beamer source. Sections:
  - *Introduction*
  - *Pipeline*
  - *Methods*
  - *Applications*

## 🔧 Building the slides

From the repository root:

```bash
rm -rf build && mkdir -p build && cd build
cmake -DBUILD_DOCS=ON ..
cmake --build . -j4
cd -
```

# WignerCamp2026

This repository contains the educational materials for the **2026 Wigner Summer Camp** organized by the **Data and Compute Intensive Sciences Research Group** at the Wigner Research Centre for Physics.

This year 2 different projects are offered to students:
- Edge detection:
    - Using a special convolution the relevant edges can be found on an image.
    - At the camp there will be several opportunities: applying the method to a video, investigating scale dependence of the method, or applying it to live video from a robot.
- Anomaly detection:
    - The research groups's novel method [altx](https://github.com/dcintlab/altx) has been demonstrated as effective in time-series data classification, now we would like to apply ot to anomaly detection.
    - The special focus will be on classical signal processing methods which are able to find peaks in the data.
    - Also classical hyperparameter optimizations such as bayesian hyperparameter optimization will be used to optimize the hyperparameters of the method.

---

## 📦 Cloning repository

You can clone this repository using:

```bash
git clone git@github.com:dcintlab/WignerCamp2026.git
cd WignerCamp2026
```

### Contents

You should get familiar with the folders in this repository in the following order:

#### General introduction
- [DevelopmentTools](DevelopmentTools): Basic introduction to linux terminal, vim, and git.
- Basic programming (numpy, pandas, matplotlib, torch)

#### Edge detection materials
- Convolution
- Introduction to the method

---

## ⏰ Recommended timeline

TODO: Update table

---

## 🐍 Creating the Conda Environment

To run the Python scripts, create a new Conda environment named `ALTenv`:

```bash
conda create -n ALTenv python=3.11 -y
conda activate ALTenv
```

Then install the required packages:

```bash
pip install numpy matplotlib pandas scipy
pip install torch torchvision torchaudio
pip install pytest
```

---

## 📄 Building LaTeX Documents

### 🔧 Installing Dependencies on Linux
To build the LaTeX documents with `CMake`, you need to have `cmake`, `pdflatex`, and `bibtex` installed. On most Linux distributions you can install them with your package manager.

For example, on Ubuntu/Debian:
```bash
sudo apt update
sudo apt install cmake texlive-latex-base texlive-latex-recommended
sudo apt install texlive-bibtex-extra texlive-fonts-recommended
```

- `cmake` — the build system.
- `pdflatex` — provided by texlive-latex-base (compiles .tex to .pdf).
- `bibtex` — provided by texlive-bibtex-extra (manages references).
- `texlive-latex-recommended` and `texlive-fonts-recommended` — recommended LaTeX packages and fonts used by many templates.

### 🔧 Compiling LaTeX Documents

Some folders contain `.tex` slides or documents. To compile all LaTeX files using `CMake`:

```bash
mkdir build
cd build
cmake ..
cmake --build . -j4
cd -
```

This will:

- Compile all `.tex` files found in the subdirectories,
- Automatically handle references (BibTeX if needed),
- Clean up all temporary files including: `.aux`, `.log`, `.toc`, `.out`, `.bbl`, `.blg`, `.lof`, `.lot`, `.snm`, `.nav`, `.vrb`.

---

## 👥 Authors

Developed by members of the **Wigner Data and Compute Intensive Sciences Group**.

---

## 📜 License

Materials in this repository are provided for **educational purposes**.

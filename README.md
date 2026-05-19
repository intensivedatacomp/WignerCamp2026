# WignerCamp2026

This repository contains the educational materials for the **2026 Wigner Summer Camp** organized by the **Data and Compute Intensive Sciences Research Group** at the Wigner Research Centre for Physics.

This year 2 different projects are offered to students:
- Edge detection:
    - Using a special convolution the relevant edges can be found on an image.
    - At the camp there will be several opportunities: applying the method to a video, investigating scale dependence of the method, or applying it to live video from a robot.
- Anomaly detection:
    - The research groups's novel method [altx](https://github.com/dcintlab/altx) has been demonstrated as effective in time-series data classification, now we would like to apply it to anomaly detection.
    - The special focus will be on classical signal processing methods which are able to find peaks in the data.
    - Also classical hyperparameter optimizations such as bayesian hyperparameter optimization will be used to optimize the hyperparameters of the method.

---

## 📦 Setup + cloning repository

First the development environment has to be set up for the Summer School, you can find instructions to do that at [EnvironmentSetup.md](DevelopmentTools/EnvironmentSetup.md).

You can clone this repository using:

```bash
git clone git@github.com:dcintlab/WignerCamp2026.git
cd WignerCamp2026
```

### Contents

You should get familiar with the folders in this repository in the following order:

#### General introduction
- [DevelopmentTools](DevelopmentTools): Basic introduction to linux terminal, vim, and git.
- [BasicProgramming](BasicProgramming): python, numpy, pandas, matplotlib, torch.

#### Edge detection materials
- Introduction to the project for the summer school.
- [EdgeDetectionConvolution](EdgeDetectionConvolution): introduction to convolution.
- Introduction to the method.

#### Anomaly detection
- Introduction to the project for the summer school.
- [AnomalyDetectionMathematics](AnomalyDetectionMathematics): matrix multiplication, eigendecomposition.
- Introduction to `altx`.
- [AnomalyDetectionSignalProcessing](AnomalyDetectionSignalProcessing): finding peaks and bayesian hyperparameter optimization.

---

## ⏰ Recommended timeline

TODO: Update table

---

## 🐍 Creating the Conda Environment

To run the Python scripts, create a new Conda environment named `WignerCampEnv`:

```bash
conda create -n WignerCampEnv python=3.14 -y
conda activate WignerCampEnv
```

Then install the required packages:

```bash
pip install -r requirements.txt
```

---

## 📄 Building LaTeX Documents

### 🔧 Installing Dependencies on Linux
To build the LaTeX documents with `CMake`, you need to have `cmake`, `pdflatex`, and `bibtex` installed. On most Linux distributions you can install them with your package manager. For a complete installation guide for the Summer School see: [EnvironmentSetup.md](DevelopmentTools/EnvironmentSetup.md).

### 🔧 Using Docker image to compile latex

You can get a prepared docker image by, see [github/halmosb/docker-builder](https://github.com/halmosb/docker-builder):
```bash
cd ..
git clone git@github.com:halmosb/docker-builder.git
cd docker-builder
git checkout v0.3.3
pip install -e .
docker-builder --no-root --latex
sudo docker build -f generated/Dockerfile.3.14.cpu -t python:3.14-cpu-no-root-latex .
cd ../WignerCamp2026
```

You can run the docker image with:
```bash
sudo docker run -it --rm \
  -v $(pwd):/workspace \
  --user root \
  -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix \
  python:3.14-cpu-no-root-latex
```


### 🔧 Compiling LaTeX Documents and jupyter notebook presentations

Some folders contain `.tex` slides or documents. To compile all LaTeX files using `CMake`:

```bash
rm -rf build
mkdir -p build
cd build
cmake -DBUILD_DOCS=ON -DBUILD_NOTEBOOKS=ON ..
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

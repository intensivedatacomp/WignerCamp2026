# Wigner Camp 2026

This repository contains the educational materials for the **2026 Wigner Summer Camp** organized by the **Data and Compute Intensive Sciences Research Group** at the Wigner Research Centre for Physics.

This year 2 different projects are offered to students:
- Edge detection:
    - Using a special convolution the relevant edges can be found on an image.
    - At the camp there will be several opportunities: applying the method to a video, investigating scale dependence of the method, or applying it to live video from a robot.
- Anomaly detection:
    - The research groups's novel method [altx](https://github.com/halmosb/altx) has been demonstrated as effective in time-series data classification, now we would like to apply it to anomaly detection.
    - The special focus will be on classical signal processing methods which are able to find peaks in the data.
    - Also classical hyperparameter optimizations such as bayesian hyperparameter optimization will be used to optimize the hyperparameters of the method.

---

## 🐍 Creating the Conda Environment

To run the Python scripts, create a new Conda environment named `WignerCampEnv`:

```bash
conda create -n WignerCampEnv python=3.14 -y
conda activate WignerCampEnv
```

---

## 📦 Setup + cloning repositories

First the development environment has to be set up for the Summer School, you can find instructions to do that at [EnvironmentSetup.md](GeneralDevelopmentTools/EnvironmentSetup.md).

You can clone this repository using:

```bash
git clone git@github.com:intensivedatacomp/WignerCamp2026.git
cd WignerCamp2026
pip install -r requirements.txt
cd ..
```

### Edge detection additional repos
For the edge detection project, some additional repositories are also needed.
```bash
git clone git@github.com:intensivedatacomp/image-processing.git
```

For both projects, the change directory to this repository:
```bash
cd WignerCamp2026
```

### Anomaly detection
For the anomaly detection project, some additional repositories are also needed.

For generating the artificial dataset:
```bash
git clone git@github.com:intensivedatacomp/artificial-dataset.git
cd artificial-dataset
pip install -e .[dev,docs]
cd ..
```

For using `altx`:
```bash
git clone git@github.com:halmosb/altx.git altx-fork
cd altx-fork
pip install -e .[examples,docs]
cd ..
```

For both projects, the change directory to this repository:
```bash
cd WignerCamp2026
```

---

## 📋 Contents

You should get familiar with the folders in this repository in the following order:

### General introduction
- [GeneralDevelopmentTools](GeneralDevelopmentTools): Basic introduction to linux terminal, vim, and git.
- [GeneralBasicProgramming](GeneralBasicProgramming): python, numpy, pandas, matplotlib, torch.
- [GeneralTestsAndDocumentation](GeneralTestsAndDocumentation): pytest and documenting code.

### Edge detection materials
- [IntroductionToImageProcessing](IntroductionToImageProcessing) for the summer school.
- [EdgeDetectionConvolution](EdgeDetectionConvolution): introduction to convolution.
- Introduction to the method.
- [GoodFeaturesToTrack](GoodFeaturesToTrack): `cv2.GoodFeaturesToTrack` method for finding corners.
- External repositories:
    - [github/intensivedatacomp/image-processing](https://github.com/intensivedatacomp/image-processing): Implementation of the edge detection method. TODO: finish repo!!!
    - [github/halmosb/Wigner-Robot](https://github.com/halmosb/Wigner-Robot): Code for controlling the robot.

### Anomaly detection
- Introduction to the project for the summer school.
- [AnomalyDetectionMathematics](AnomalyDetectionMathematics): matrix multiplication, eigendecomposition, accuracy.
- [AnomalyDetectionALTx](AnomalyDetectionALTx): Introduction to `altx`.
- [AnomalyDetectionSignalProcessing](AnomalyDetectionSignalProcessing): finding peaks and bayesian hyperparameter optimization.
- External repositories:
    - [github/intensivedatacomp/artificial-dataset](https://github.com/intensivedatacomp/artificial-dataset): Artificial dataset generation.
    - [github/halmosb/altx](https://github.com/halmosb/altx): `altx`: Adaptive Law-Based Transformation.

---

## ⏰ Recommended timeline

TODO: Update table


---

## 📄 Building LaTeX Documents

### 🔧 Installing Dependencies on Linux
To build the LaTeX documents with `CMake`, you need to have `cmake`, `pdflatex`, and `bibtex` installed. On most Linux distributions you can install them with your package manager. For a complete installation guide for the Summer School see: [EnvironmentSetup.md](DevelopmentTools/EnvironmentSetup.md).

### 🔧 Using Docker image to compile latex


You can run the docker image with:
```bash
sudo docker run -it --rm \
  -v $(pwd):/workspace \
  --user root \
  -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix \
  python:3.14-v0.3.4-cpu-no-root-latex
```
> [!NOTE]
> In order to display matplotlib plots executing `xhost +local:docker` on the host is also needed.

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

- Compile all `.tex` files found in the subdirectories.
- Automatically handle references (BibTeX if needed).
- Clean up all temporary files including: `.aux`, `.log`, `.toc`, `.out`, `.bbl`, `.blg`, `.lof`, `.lot`, `.snm`, `.nav`, `.vrb`, `.fls`, `.aux`, `.fdb_latexmk`.
- Compile the jupyter notebooks (whose name ends with `_presentation.ipynb`) to HTML presentations.

---

## 👥 Authors

Developed by members of the **Wigner Data and Compute Intensive Sciences Group**.

---

## 📜 License

Materials in this repository are provided for **educational purposes** and it is licensed under [GPLv3 license](LICENSE).

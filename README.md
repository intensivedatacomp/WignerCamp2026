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
For the edge detection project, the [github/intensivedatacomp/image-processing/](https://github.com/intensivedatacomp/image-processing/).
```bash
git clone git@github.com:intensivedatacomp/image-processing.git
cd image-processing
pip install -e .[dev,docs]
cd ..
```

For controlling the robot [github/halmosb/Wigner-Robot](https://github.com/halmosb/Wigner-Robot):
```bash
git clone git@github.com:halmosb/Wigner-Robot.git
```

For both projects, the change directory to this repository:
```bash
cd WignerCamp2026
```

### Anomaly detection materials
For the anomaly detection project, some additional repositories are also needed.

For generating the artificial dataset, [github/intensivedatacomp/artificial-dataset](https://github.com/intensivedatacomp/artificial-dataset):
```bash
git clone git@github.com:intensivedatacomp/artificial-dataset.git
cd artificial-dataset
pip install -e .[dev,docs]
cd ..
```

For using `altx`, [github/halmosb/altx](https://github.com/halmosb/altx):
```bash
git clone git@github.com:halmosb/altx.git altx-fork
cd altx-fork
pip install -e .[docs]
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
- [IntroductionToImageProcessing](IntroductionToImageProcessing): introduction to the edge detection method for the summer school.
- [EdgeDetectionConvolution](EdgeDetectionConvolution): introduction to convolution.
- [IntroductionToImageProcessingPackage](IntroductionToImageProcessingPackage): overview of the `image-processing` package implementing the method.
- [GoodFeaturesToTrack](GoodFeaturesToTrack): `cv2.GoodFeaturesToTrack` method for finding corners.
- [RobotSoftware](RobotSoftware): client/server control software for running the method on the robot's live video.
- External repositories:
    - [github/intensivedatacomp/image-processing](https://github.com/intensivedatacomp/image-processing): Implementation of the edge detection method.
    - [github/halmosb/Wigner-Robot](https://github.com/halmosb/Wigner-Robot): Code for controlling the robot.

### Anomaly detection
- [AnomalyDetectionIntroduction](AnomalyDetectionIntroduction): introduction to the project for the summer school.
- [AnomalyDetectionMathematics](AnomalyDetectionMathematics): matrix multiplication, eigendecomposition, accuracy.
- [AnomalyDetectionALTx](AnomalyDetectionALTx): Introduction to `altx`.
- [AnomalyDetectionSignalProcessing](AnomalyDetectionSignalProcessing): finding peaks and bayesian hyperparameter optimization.
- [AnomalyDetectionCalculations](AnomalyDetectionCalculations): tuning `find_peaks` with Optuna to detect anomalies.
- External repositories:
    - [github/intensivedatacomp/artificial-dataset](https://github.com/intensivedatacomp/artificial-dataset): Artificial dataset generation.
    - [github/halmosb/altx](https://github.com/halmosb/altx): `altx`: Adaptive Law-Based Transformation.

---

## ⏰ Recommended timeline

The camp runs **6–10 July 2026**. Each half-hour slot is one row. The two project tracks — **Edge Detection** and **Anomaly Detection** — share the morning of Day 1 (opening, project introductions and the general programming introduction), then split into separate groups from after the first lunch. The recommended scheduling below covers all track-specific materials by the **end of Day 2**; Days 3–4 are dedicated to project work, and Day 5 to preparing and giving the closing presentations. Lunch is **12:30–13:30** every day.

<table>
  <tr>
    <th rowspan="2">Time</th>
    <th colspan="2">Day 1<br>Mon 6 Jul</th>
    <th colspan="2">Day 2<br>Tue 7 Jul</th>
    <th colspan="2">Day 3<br>Wed 8 Jul</th>
    <th colspan="2">Day 4<br>Thu 9 Jul</th>
    <th colspan="2">Day 5<br>Fri 10 Jul</th>
  </tr>
  <tr>
    <th>Edge Detection</th><th>Anomaly Detection</th>
    <th>Edge Detection</th><th>Anomaly Detection</th>
    <th>Edge Detection</th><th>Anomaly Detection</th>
    <th>Edge Detection</th><th>Anomaly Detection</th>
    <th>Edge Detection</th><th>Anomaly Detection</th>
  </tr>

  <tr>
    <td>9:00–9:30</td>
    <td colspan="2">Opening Ceremony</td>
    <td colspan="2">Revision Exercises</td>
    <td colspan="2" rowspan="7">Working on the chosen topic</td>
    <td colspan="2" rowspan="7">Working on the chosen topic</td>
    <td colspan="2" rowspan="4">Creating Presentation</td>
  </tr>
  <tr>
    <td>9:30–10:00</td>
    <td colspan="2">Introduction to the projects<br><a href="IntroductionToImageProcessing">Edge Detection intro</a> · <a href="AnomalyDetectionIntroduction">Anomaly Detection intro</a></td>
    <td rowspan="6"><a href="IntroductionToImageProcessingPackage">Image Processing package</a><br><i>(<a href="https://github.com/intensivedatacomp/image-processing">image-processing</a> repo)</i></td>
    <td rowspan="6"><a href="AnomalyDetectionALTx">ALTx introduction</a><br><i>(<a href="https://github.com/intensivedatacomp/artificial-dataset">artificial-dataset</a> &amp; <a href="https://github.com/halmosb/altx">altx</a> repos)</i></td>
  </tr>
  <tr>
    <td>10:00–10:30</td>
    <td colspan="2" rowspan="5">General introduction<br><a href="GeneralDevelopmentTools/EnvironmentSetup.md">EnvironmentSetup.md</a> · <a href="GeneralDevelopmentTools">DevelopmentTools</a> · <a href="GeneralBasicProgramming">BasicProgramming</a><br><i>(optional: <a href="GeneralTestsAndDocumentation">TestsAndDocumentation</a>)</i></td>
  </tr>
  <tr>
    <td>10:30–11:00</td>
  </tr>
  <tr>
    <td>11:00–11:30</td>
    <td colspan="2" rowspan="2">Finalizing Presentation</td>
  </tr>
  <tr>
    <td>11:30–12:00</td>
  </tr>
  <tr>
    <td>12:00–12:30</td>
    <td colspan="2">Practice Presentation</td>
  </tr>

  <tr>
    <td>12:30–13:00</td>
    <td colspan="10" rowspan="2">Lunch</td>
  </tr>
  <tr>
    <td>13:00–13:30</td>
  </tr>

  <tr>
    <td>13:30–14:00</td>
    <td rowspan="3"><a href="EdgeDetectionConvolution">Convolution</a><br><i>(presentation)</i></td>
    <td rowspan="3"><a href="AnomalyDetectionMathematics">Linear Algebra</a><br><i>(presentations)</i></td>
    <td rowspan="3"><a href="GoodFeaturesToTrack">Good Features To Track</a></td>
    <td rowspan="3"><a href="AnomalyDetectionSignalProcessing">Signal Processing</a><br><i>(find_peaks &amp; Optuna)</i></td>
    <td colspan="2" rowspan="7">Working on the chosen topic</td>
    <td colspan="2" rowspan="7">Working on the chosen topic</td>
    <td colspan="2" rowspan="7">Closing &amp; presentation</td>
  </tr>
  <tr>
    <td>14:00–14:30</td>
  </tr>
  <tr>
    <td>14:30–15:00</td>
  </tr>
  <tr>
    <td>15:00–15:30</td>
    <td rowspan="4"><a href="EdgeDetectionConvolution/conv2d_exercise">conv2d exercise</a></td>
    <td rowspan="4"><a href="AnomalyDetectionMathematics/mathematics_exercise">mathematics exercise</a></td>
    <td rowspan="4"><a href="RobotSoftware">Robot Software</a></td>
    <td rowspan="4"><a href="AnomalyDetectionCalculations">Calculations</a><br><i>(tuning find_peaks with Optuna)</i></td>
  </tr>
  <tr>
    <td>15:30–16:00</td>
  </tr>
  <tr>
    <td>16:00–16:30</td>
  </tr>
  <tr>
    <td>16:30–17:00</td>
  </tr>
</table>

> [!NOTE]
> The exact times for the non-project activities on Days 3–4 (e.g. visiting particle accelerators) are not fixed yet; those slots are shown as project work for now.

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

# 🛠️ Environment Setup Guide for Summer School

This guide provides step-by-step instructions for installing and configuring the required tools:

* Conda (free distribution)
* Git + GitHub
* Vim
* Docker (optional)
* LaTeX (optional)

We cover both **Ubuntu (Linux)** and **Windows** systems, including **WSL (Windows Subsystem for Linux)**.

---

# 1. Conda (Python Environment Manager)

We recommend **Miniforge** (fully free, community-driven, no licensing restrictions).

## 🔹 Ubuntu

### Install

```bash
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-Linux-x86_64.sh
```

Restart shell or:

```bash
source ~/.bashrc
```

### Test

```bash
conda --version
```

### Common Issues

* **`conda: command not found`**
  → Run `source ~/.bashrc`
* **Permission issues**
  → Avoid installing with `sudo`

---

## 🔹 Windows (Native)

### Install

1. Download Miniforge installer from:
   [https://github.com/conda-forge/miniforge](https://github.com/conda-forge/miniforge)
2. Run `.exe` installer
3. Select:

   * “Add to PATH” (optional but convenient)

### Test (Command Prompt / PowerShell)

```powershell
conda --version
```

### Common Issues

* PATH not updated → restart terminal
* Antivirus blocking installer → temporarily disable

---

# 2. Git

## 🔹 Ubuntu

```bash
sudo apt update
sudo apt install git
```

### Configure

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### Test

```bash
git --version
```

---

## 🔹 Windows

Download from:
[https://git-scm.com/download/win](https://git-scm.com/download/win)

### Recommended installer options

* ✔ Use Git from command line
* ✔ Use bundled OpenSSH

### Test

```powershell
git --version
```

---

# 3. GitHub Registration

1. Go to: [https://github.com](https://github.com)
2. Click **Sign up**
3. Provide:

   * Email
   * Username
   * Password
4. Verify email

### Optional: SSH Setup

```bash
ssh-keygen -t ed25519 -C "your@email.com"
cat ~/.ssh/id_ed25519.pub
```

Add key to:
**GitHub → Settings → SSH and GPG keys**

---

# 4. Vim (Text Editor)

## 🔹 Ubuntu

```bash
sudo apt install vim
```

## 🔹 Windows

Options:

* Install via Git Bash (comes bundled)
* Or download from:
  [https://www.vim.org/download.php](https://www.vim.org/download.php)

### Test

```bash
vim
```

### Basic Usage

* Insert mode: `i`
* Save & quit: `:wq`
* Quit without saving: `:q!`

---

# 5. Docker

## 🔹 Ubuntu

### Install

```bash
sudo apt update
sudo apt install docker.io
```

### Enable

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

### Run without sudo

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Test

```bash
docker run hello-world
```

### Common Issues

* **Permission denied**
  → Ensure user is in `docker` group
* **Daemon not running**
  → `sudo systemctl start docker`

---

## 🔹 Windows

Install **Docker Desktop**:
[https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

### Requirements

* WSL2 enabled (recommended)
* Virtualization enabled in BIOS

### Test

```powershell
docker run hello-world
```

---

# 6. LaTeX

We recommend **TeX Live**.

## 🔹 Ubuntu

```bash
sudo apt install texlive-full
sudo apt install
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-bibtex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    dvipng \
    cm-super
```

### Test

```bash
pdflatex --version
```

---

## 🔹 Windows

Install **MiKTeX**:
[https://miktex.org/download](https://miktex.org/download)

### Notes

* Enable “install missing packages on-the-fly”

### Test

```powershell
pdflatex --version
```

---

# 7. Windows Subsystem for Linux (WSL)

WSL allows running a Linux environment inside Windows.

## 🔹 Install WSL

Open PowerShell as Administrator:

```powershell
wsl --install
```

Reboot when prompted.

---

## 🔹 Install Ubuntu in WSL

```powershell
wsl --install -d Ubuntu
```

Launch Ubuntu and create a user.

---

## 🔹 Use WSL

You can now use Linux commands:

```bash
sudo apt update
sudo apt install git vim
```

### Access Windows Files

```bash
cd /mnt/c/Users/YourName
```

---

## 🔹 When to Use WSL vs Native Windows

| Task        | Recommended |
| ----------- | ----------- |
| Development | WSL         |
| GUI tools   | Windows     |
| Docker      | WSL backend |

---

# 8. General Troubleshooting

### PATH Issues

* Restart terminal
* Check:

```bash
echo $PATH
```

### Permissions

* Avoid `sudo` unless necessary
* Use proper user groups (e.g., docker)

### Network Issues

* Try:

```bash
ping github.com
```

---

# 9. Final Verification Checklist

Run these commands:

```bash
conda --version
git --version
vim --version
docker --version
pdflatex --version
```

---

# 🎯 Recommendation

For consistency during the summer school:

* Prefer **Ubuntu or WSL**
* Use **Miniforge + conda environments**
* Use **Docker for reproducibility**

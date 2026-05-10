# 🖥️ Linux Terminal Basics, Vim, Git

This directory contains beginner-friendly guides designed to help new users become comfortable with the Linux terminal, the Vim text editor, and git. Both guides are written in Markdown and can be viewed in any Markdown viewer or directly on GitHub.

---

## 📁 Contents

### 🛠️ [EnvironmentSetup.md](EnvironmentSetup.md)

Instructions on how to set up your local environment for the Summer School:

- Conda (free distribution)
- Git + GitHub
- Vim
- WSL
- LaTeX (optional)
- Docker (optional)
- cmake (optional)

### 📘 [TerminalBasics.md](TerminalBasics.md)

A practical introduction to using the **Linux terminal**. Topics include:

- Navigating directories with `cd`, `ls`, `pwd`
- Creating, copying, moving, and deleting files and folders
- Viewing file contents with `cat`, `head`, `tail`, `less`
- Editing with `vim`
- Writing multiple lines to files using `for` loops
- Using tools like `htop` and `time`
- Final challenge task to reinforce learning

Ideal for users who are new to command-line environments.

---

### 📝 [Vim.md](Vim.md)

A short guide to **using the Vim editor**, including:

- Creating and saving files
- Vim modes (normal, insert, visual, etc.)
- Copying, pasting, deleting text (in Vim and with system clipboard)
- Moving the cursor efficiently
- Showing line numbers
- Undo/redo, search and replace
- Opening a terminal inside Vim with `:vert term`
- Practical examples showing why Vim is efficient

Useful for users who want to learn efficient text editing in the terminal.

---

### 📝 [Git.md](Git.md)

A basic introduction of using **git** and **Github**.

- Creating and adding SSH keys to Github
- Cloning and creating a repository
- Committing changes
- Compering file versions
- Pushing and git conflicts
- Branches

### 📝 [Git_intermediate.md](Git_intermediate.md)

Description of more advanced concepts of **git**. This can be skipped for beginner users.

- Trees
- Branches
- Merging
- Rebasing
- Reachability
- Tags

### 📝 [setup_git_exercises.py](setup_git_exercises.py)

Python script to generate git repositories for the examples in [Git_intermediate.md](Git_intermediate.md).

Can be run with:
```bash
python setup_git_exercises.py
```


## ✅ Extra

You can also open these files with:

```bash
less TerminalBasics.md
vim Vim.md
```
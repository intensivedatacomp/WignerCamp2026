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

A beginner's introduction to **the Vim editor**, covering the most important concepts with many examples:

- Why Vim and how to think about it
- The modal system: Normal, Insert, and Command-Line modes
- Opening, saving, and quitting
- Moving around efficiently
- Editing: deleting, changing, copy and paste
- Undo and redo
- Search and basic search/replace
- Visual mode for selecting text
- Common beginner mistakes and how to avoid them

Start here if you have never used Vim before.

---

### 📝 [Vim_intermediate.md](Vim_intermediate.md)

A deeper guide to **Vim's more powerful features**, for users who are already comfortable with the basics:

- Text objects (`ciw`, `da"`, `yi(`, …)
- The dot command — repeat last change
- Operators and motions as a composable language
- Macros — recording and replaying command sequences
- Basic regular expressions in Vim
- The global command `:g`
- Advanced search and replace with back-references
- Registers (named clipboards)
- Working with splits, tabs, and multiple buffers
- A useful `~/.vimrc` starter configuration

Can be skipped for beginner users.

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

## ✅ Extra

You can also open these files with:

```bash
less TerminalBasics.md
vim Vim.md
vim Vim_intermediate.md
```
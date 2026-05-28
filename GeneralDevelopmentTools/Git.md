# Introduction to Git and GitHub

**Git** is a version control system that helps you track changes in your code, collaborate with others, and manage different versions of your project. **GitHub** is an online platform that hosts Git repositories and provides tools for collaboration, issue tracking, and more.

---
## Downloading git
Git can be downloaded with:
```
sudo apt install git
```
For other operating systems see: [Install git](https://git-scm.com/install/).

---

## Setting up SSH Keys

To securely communicate with GitHub without typing your password every time, you can use SSH keys. You can find the up-to-date information at [Generating a new SSH key and adding it to the ssh-agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent?platform=windows).

### Generate an SSH key:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

Press Enter to accept the default file location and optionally set a passphrase.

### Add your key to the SSH agent:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### Add the key to your GitHub account:

* Copy your public key:

```bash
cat ~/.ssh/id_ed25519.pub
```

* Go to your [GitHub account](https://github.com/settings/profile) → Settings → [SSH and GPG keys](https://github.com/settings/keys) → New SSH key → paste the key and save.

---

## Clone or Create a Repository

To **clone** an existing repository:

```bash
git clone git@github.com:dcintlab/WignerCamp2026.git
```

To **create** a new repository locally:

```bash
mkdir MyRepo
cd MyRepo
git init
```

Then create a repository on GitHub and push your local repo there (see below).

---
## Initial setup

Before you can use git in its full glory you have to set up a things. First, you have to tell who you are and which editor you would like to use:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@something.com"
git config --global core.editor "vim"
```

Additionally, you can set up these additional aliases to make reviewing history easier:
```bash
git config --global alias.lga "log --all --graph --decorate --oneline"
git config --global alias.lg "log --graph --decorate --oneline"
git config --global alias.lgac "log --all --graph --decorate --pretty=format:'%C(yellow)%h%Creset %C(green)%cn%Creset %C(auto)%d%Creset %C(white)%s%Creset'"
git config --global alias.lgc "log --graph --decorate --pretty=format:'%C(yellow)%h%Creset %C(green)%cn%Creset %C(auto)%d%Creset %C(white)%s%Creset'"
```

## Adding and Committing Changes

### Add:

Stages changes to be included in the next commit.

```bash
git add filename      # stage a single file
git add .             # stage all changes
```

### Commit:

Records the staged changes with a message.

```bash
git commit -m "your message"
```

**Use case:**

* `add` is useful to select exactly which changes you want to include.
* `commit` actually saves those staged changes into the repository's history.

---

## Comparing Changes

To compare your working directory with the latest commit:

```bash
git diff
```

To compare with the previous commit:

```bash
git diff HEAD~1 HEAD
```

To see what files changed:

```bash
git status
```

---

## Pushing Changes

To upload your commits to the remote repository:

```bash
git push
```

For the first time you might have to use:
```bash
git push origin master
```
(or `git push origin main`) depending on the repository.

If you encounter **git conflicts**, don’t worry! This happens when you and someone else changed the same part of a file. Git will mark the conflicting areas in the file:

```bash
<<<<<<< HEAD
Your changes
=======
Other's changes
>>>>>>> branch-name
```

You just need to edit the file, decide which version (or combination) to keep, then:

```bash
git add filename
git commit -m "Conflict solved"
```

---

## Branches

Branches let you work on different versions of your project without interfering with the main codebase.

### Create and switch to a branch:

```bash
git checkout -b feature-branch
```

### Switch between branches:

```bash
git checkout main
```

### Merge a branch back into main:

```bash
git checkout main
git merge feature-branch
```

---

### Summary

Git and GitHub are powerful tools for managing your code. Don’t be afraid of conflicts — they are just opportunities to choose the right changes. Use branches to develop features or experiments independently. Happy coding!

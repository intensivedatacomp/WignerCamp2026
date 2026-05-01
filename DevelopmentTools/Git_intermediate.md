# Git Intermediate Tutorial (Practical & Conceptual)

This tutorial focuses on *how Git actually works under the hood* and the commands you will use in real workflows. It avoids basic setup (you can find instructions about it [here](Git.md)) and instead emphasizes mental models, history manipulation, and collaboration patterns.

> [!NOTE]
> You should try the commands from this tutorial outside any git repository, including this one. For example go `cd ..; mkdir -p not_repo; cd not_repo`.

---

# 1. The Three Trees: HEAD, Index (Staging Area), Working Directory

Understanding Git starts with its **three-tree architecture**.

## 1.1 Working Directory
- This is your actual filesystem.
- Files here can be:
  - **untracked**
  - **modified**
  - **clean (matching Git state)**

👉 Think: *what you are editing right now*

---

## 1.2 Staging Area (Index)
- A snapshot of what will go into the next commit.
- You explicitly control it using `git add`.

👉 Think: *what you intend to commit*

---

## 1.3 HEAD
- Points to the **current commit** (usually the tip of a branch).
- Represents the last committed snapshot.

👉 Think: *what is already committed*

---

## 1.4 Visual Model

```

Working Directory   -->  Staging Area  ----->  HEAD
edit                add                commit

````

---

## 1.5 Key Commands

### Check state
```bash
git status
````

### Stage changes

```bash
git add file.txt
git add .
```
The "." represents the current directory, using it stages all changes.

### Unstage changes

```bash
git restore --staged file.txt
```

### Discard working directory changes

```bash
git restore file.txt
```

### Reset staging + working directory

```bash
git reset --hard
```

⚠️ `--hard` deletes local changes permanently.

---

# 2. Branches

## 2.1 What is a Branch?

A branch is just a **pointer to a commit**.

```
A -- B -- C (main)
          ^
        HEAD
```

Creating a new branch:

```bash
git branch feature
```

Now:

```
A -- B -- C (main, feature)
```

---

## 2.2 Checkout / Switch

Move HEAD to another branch:

```bash
git checkout feature
```

Create + switch:

```bash
git checkout -b feature
```

---

## 2.3 Reset (Moving Branch Pointers)

Reset moves the current branch:

### Soft reset

```bash
git reset --soft HEAD~1
```

* Keeps changes staged

### Mixed reset (default)

```bash
git reset HEAD~1
```

* Keeps changes in working directory

### Hard reset

```bash
git reset --hard HEAD~1
```

* Deletes everything after that commit

---

## 2.4 Detached HEAD

```bash
git checkout <commit-hash>
```

* HEAD points directly to a commit (not a branch)
* New commits are "dangling" unless you create a branch

Fix:

```bash
git switch -c new-branch
```

---

# 3. Merging

## 3.1 Standard Merge

```bash
git merge feature
```

Creates a new commit if histories diverged:

```
      D -- E (feature)
     /
A -- B -- C (main)
           \
            F (merge commit)
```

---

## 3.2 Fast-Forward Merge

If no divergence:

```bash
git merge feature
```

Result:

```
A -- B -- C -- D (main, feature)
```

No merge commit created.

---

## 3.3 No Fast-Forward Merge

Force a merge commit:

```bash
git merge --no-ff feature
```

Why?

* Keeps branch structure visible
* Useful for feature tracking

---

## 3.4 Merge Conflicts

Occurs when same lines are modified:

```
<<<<<<< HEAD
current branch code
=======
incoming branch code
>>>>>>> feature
```

### Resolve:

1. Edit file manually
2. Remove markers
3. Stage resolution:

```bash
git add file.txt
```

4. Complete merge:

```bash
git commit
```

---

# 4. Rebasing

Rebasing = **replaying commits on top of another base**

---

## 4.1 Non-Interactive Rebase

```bash
git rebase main
```

Before:

```
A -- B -- C (main)
      \
       D -- E (feature)
```

After:

```
A -- B -- C -- D' -- E' (feature)
```

---

## 4.2 Interactive Rebase

```bash
git rebase -i HEAD~3
```

Options:

```
pick   keep commit
reword edit message
edit   modify commit
squash merge commits
drop   delete commit
```

### Example: squash commits

```
pick 123 first commit
squash 456 second commit
```

---

## 4.3 Rebase vs Merge

| Merge                     | Rebase                 |
| ------------------------- | ---------------------- |
| preserves history         | rewrites history       |
| creates merge commits     | linear history         |
| safer for shared branches | cleaner for local work |

---

## 4.4 Abort Rebase

```bash
git rebase --abort
```

---

# 5. Reachability in Git

## 5.1 Definition

A commit is **reachable** if there is a path from a reference (branch/tag) to it.

---

## 5.2 Why It Matters

* Git garbage collects unreachable commits
* Lost commits can still exist temporarily

---

## 5.3 Inspect Reachability

```bash
git log --all
git fsck --lost-found
```

---

## 5.4 Reflog (Critical Tool)

Tracks where HEAD pointed:

```bash
git reflog
```

Recover lost commit:

```bash
git checkout <hash>
```

---

# 6. Tags

## 6.1 What is a Tag?

A tag is a **named reference to a specific commit**, typically for releases.

---

## 6.2 Types of Tags

### Lightweight

```bash
git tag v1.0
```

### Annotated (recommended)

```bash
git tag -a v1.0 -m "Release v1.0"
```

---

## 6.3 List Tags

```bash
git tag
```

---

## 6.4 Show Tag Details

```bash
git show v1.0
```

---

## 6.5 Checkout a Tag

```bash
git checkout v1.0
```

(Detached HEAD state)

---

## 6.6 Push Tags

```bash
git push origin v1.0
```

Push all:

```bash
git push --tags
```

---

# Final Practical Tips

* Use **rebase locally**, **merge for shared branches**
* Avoid `--hard` unless absolutely sure
* Use `reflog` to recover mistakes
* Prefer `--no-ff` for structured history
* Keep commits small and meaningful

---

# Summary

* Git is a **snapshot + pointer system**
* The **three trees** define state transitions
* Branches are just **movable pointers**
* Merging combines histories, rebasing rewrites them
* Reachability determines data persistence
* Tags provide stable reference points for releases

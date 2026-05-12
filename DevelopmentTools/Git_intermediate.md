# Git Intermediate Tutorial

This tutorial builds on the basics covered in [Git.md](Git.md) and explores *how Git actually works under the hood*. By the end you will understand why Git behaves the way it does, how to fix common mistakes, and how to use powerful features like branching strategies, rebasing, and tags.

> [!NOTE]
> Every section has a **hands-on exercise**. Each exercise begins with a description of the repository state you need to create, followed by a hidden **Setup** section containing the exact terminal commands to reach that state. First, create a working directory for all exercises:
> ```bash
> mkdir git_exercises
> cd git_exercises
> ```
> Set up each exercise repository just before starting that exercise by expanding its **Setup** section.

---

# 0. Setting Up the `git lga` Alias

Before starting any exercise, register this alias once:

```bash
git config --global alias.lga "log --all --graph --decorate --oneline"
```

From now on, `git lga` is a shorthand for `git log --all --graph --decorate --oneline`, which prints a compact, decorated graph of every branch at once. All exercises use this alias instead of plain `git log`.

---

# 1. The Three Trees — Where Do Your Files Actually Live?

Before touching any Git command, it helps to know that Git thinks about your project through **three separate "areas"**. Understanding these three areas explains why `git add` and `git commit` are two separate steps, and why `git status` shows what it shows.

## 1.1 The Analogy: Desk, Backpack, and Submitted Work

Imagine writing an essay at school:

| Where | School analogy | What it means in Git |
|---|---|---|
| **Working Directory** | Your desk — messy, in progress | The actual files on your disk that you can edit freely |
| **Staging Area (Index)** | Your backpack — you chose what to pack | A holding area: changes you have *selected* for the next commit |
| **HEAD (Repository)** | The version you already handed in | The most recent committed snapshot |

The key insight: **nothing goes from your desk into the submitted version automatically**. You must first *pack it* (stage it), then *hand it in* (commit it).

---

## 1.2 Visual Model

```
┌──────────────────┐   git add    ┌───────────────┐   git commit   ┌──────────┐
│ Working Directory│ ──────────►  │  Staging Area │ ─────────────► │   HEAD   │
│  (your desk)     │              │  (your bag)   │                │ (history)│
└──────────────────┘              └───────────────┘                └──────────┘

   git restore <file>             git restore --staged <file>
   ◄── undo edit ──               ◄──── move back to desk ────
```

---

## 1.3 What Each Command Does

| Command | What moves | Direction |
|---|---|---|
| `git add <file>` | Selected changes | Working Directory → Staging Area |
| `git commit` | Everything staged | Staging Area → HEAD |
| `git restore --staged <file>` | Unstage a file | Staging Area → Working Directory |
| `git restore <file>` | Discard edits | HEAD → Working Directory (⚠️ loses changes!) |
| `git reset --hard` | Discard everything | HEAD → both Staging Area and Working Directory |

---

## 1.4 Key Commands

```bash
# See which tree each file is in right now
git status

# Stage a specific file
git add notes.txt

# Stage everything in the current folder
git add .

# See what is in the working directory but NOT yet staged
git diff

# See what IS staged and will go into the next commit
git diff --staged

# Move a staged file back to "just modified" (keeps your edits)
git restore --staged notes.txt

# Throw away edits to a file entirely (⚠️ cannot be undone)
git restore notes.txt

# Throw away ALL uncommitted changes everywhere (⚠️ very dangerous)
git reset --hard
```

> [!WARNING]
> `git restore <file>` and `git reset --hard` **permanently delete your uncommitted work**. There is no recycle bin. Only use them when you are sure.

---

## Exercise 1 — Exploring the Three Trees

Create a directory `ex1_three_trees` with a repository in the following state:

- **Commit 1** — `readme.txt` containing `"Welcome to my project."`
- **Commit 2** — `notes.txt` containing `"Remember to study Git!"`
- **Working directory** — `readme.txt` has a second line `"This line was added but NOT staged yet."` added but *not* staged
- **Untracked file** — `scratch.txt` containing `"I am an untracked file."`

<details>
<summary>Setup: terminal commands</summary>

Run these commands from your `git_exercises/` directory:

```bash
mkdir ex1_three_trees
cd ex1_three_trees
git init -b main
echo "Welcome to my project." > readme.txt
git add readme.txt
git commit -m "Initial commit: add readme"
echo "Remember to study Git!" > notes.txt
git add notes.txt
git commit -m "Add notes file"
printf "Welcome to my project.\nThis line was added but NOT staged yet.\n" > readme.txt
echo "I am an untracked file." > scratch.txt
```

</details>

```bash
cd ex1_three_trees
```

**Step 1 — See the current state of all three trees:**
```bash
git status
```
You should see `readme.txt` listed under *"Changes not staged for commit"* and `scratch.txt` under *"Untracked files"*. These are both in your **Working Directory** only.

**Step 2 — Look at what changed in readme.txt:**
```bash
git diff readme.txt
```
Lines starting with `+` were added, lines with `-` were removed.

**Step 3 — Stage only readme.txt:**
```bash
git add readme.txt
git status
```
Notice that `readme.txt` moved to *"Changes to be committed"* — it is now in the **Staging Area**. `scratch.txt` is still untracked.

**Step 4 — Look at what is staged:**
```bash
git diff --staged
```
This only shows what is *inside your backpack* — the staged changes.

**Step 5 — Commit what you staged:**
```bash
git commit -m "Update readme with new line"
git status
```
Now `readme.txt` has moved into **HEAD**. `scratch.txt` is still untracked because you never staged it.

**Step 6 — Unstage something (time-travel back to the desk):**
```bash
git add scratch.txt      # first put it in the staging area
git status               # confirm it is staged
git restore --staged scratch.txt
git status               # it moved back to untracked
```

**Step 7 — Check the full commit history:**
```bash
git lga
```

---

# 2. Branches — Sticky Notes, Not Folders

A common misconception is that branches are separate copies of your project. They are not. A branch is just a **tiny sticky note that points to a commit**. When you make a new commit, Git moves that sticky note forward automatically.

## 2.1 What Is a Branch, Really?

Every commit stores a snapshot of your files *plus* a pointer to its parent commit. This creates a chain:

```
A ──► B ──► C
            ▲
            (main)   ← this sticky note is all a branch is
```

When you create a new branch, Git just writes a second sticky note pointing to the same commit:

```
A ──► B ──► C
            ▲
            (main)
            (feature)   ← same commit, second sticky note
```

As you commit on `feature`, the `feature` sticky note moves, but `main` stays put:

```
A ──► B ──► C ──► D ──► E
            ▲           ▲
            (main)      (feature)
```

This is why branches are **free** to create — they cost almost no disk space.

---

## 2.2 HEAD: The "You Are Here" Pointer

`HEAD` is a special pointer that tells Git which branch you are currently on. When you switch branches, HEAD just moves to point to a different sticky note.

```
A ──► B ──► C ──► D ──► E
            ▲           ▲
            (main)      (feature)
                           ▲
                           HEAD   ← "you are here"
```

---

## 2.3 Creating and Switching Branches

```bash
# Create a new branch (does NOT switch to it)
git branch my-feature

# Switch to an existing branch
git switch my-feature          # modern syntax (Git 2.23+)
git checkout my-feature        # older syntax, also works

# Create AND switch in one step
git switch -c my-feature       # modern
git checkout -b my-feature     # older, also works

# See all branches (* marks the current one)
git branch

# Delete a merged branch (safe)
git branch -d my-feature

# Delete a branch even if it has unmerged commits (dangerous)
git branch -D my-feature
```

---

## 2.4 Detached HEAD — Don't Panic!

You enter *detached HEAD* state when you check out a specific commit hash instead of a branch name:

```bash
git checkout a1b2c3d    # checkout a commit, not a branch
```

Now HEAD points directly to a commit, not to any branch:

```
A ──► B ──► C ──► D
            ▲
            HEAD   ← pointing at a commit, not at a branch
```

This is fine for *looking around*, but if you **make new commits** in this state, they will not be attached to any branch. Once you switch away, those commits become invisible and Git may eventually delete them.

**If you accidentally committed in detached HEAD:**
```bash
# Create a new branch right here to save your work
git switch -c my-rescue-branch
```

---

## 2.5 Reset — Moving the Branch Pointer Backward

`git reset` moves the current branch's pointer backward in history. The three variants differ in what happens to your changes:

```
Before:    A ──► B ──► C ──► D
                             ▲
                             (main, HEAD)

After reset HEAD~2:
           A ──► B ──► C ──► D
                 ▲           (D and C are now "unreachable")
                 (main, HEAD)
```

The `~n` refers to `n` commits behind. For example `HEAD~3` means 3 commits behind where `HEAD` is. 

| Mode | Command | Your changes from C and D |
|---|---|---|
| **Soft** | `git reset --soft HEAD~2` | Still staged (in your backpack) |
| **Mixed** (default) | `git reset HEAD~2` | Still in working directory (on your desk, but unstaged) |
| **Hard** | `git reset --hard HEAD~2` | **Deleted permanently** |

> [!WARNING]
> `git reset --hard` throws away uncommitted work and the unreachable commits. Use `git reflog` to recover from accidents (see Section 5).

---

## Exercise 2 — Exploring Branches and HEAD

Create a directory `ex2_branches` with a repository in the following state:

- **`main` branch** — three commits:
  1. `story.txt` with Chapter 1
  2. `story.txt` extended with Chapter 2
  3. `foreword.txt` added after branching (this creates the divergence)
- **`feature-ending` branch** — forked after commit 2, with two more commits:
  1. `story.txt` extended with Chapter 3
  2. `epilogue.txt` added
- You should be on `main` when you start the exercise

<details>
<summary>Setup: terminal commands</summary>

Run these commands from your `git_exercises/` directory:

```bash
mkdir ex2_branches
cd ex2_branches
git init -b main
echo "Chapter 1: The beginning." > story.txt
git add story.txt
git commit -m "Add chapter 1"
cat > story.txt << 'EOF'
Chapter 1: The beginning.
Chapter 2: Things get interesting.
EOF
git add story.txt
git commit -m "Add chapter 2"
git switch -c feature-ending
cat > story.txt << 'EOF'
Chapter 1: The beginning.
Chapter 2: Things get interesting.
Chapter 3: The epic ending.
EOF
git add story.txt
git commit -m "Add chapter 3 on feature branch"
echo "And they lived happily ever after." > epilogue.txt
git add epilogue.txt
git commit -m "Add epilogue on feature branch"
git switch main
echo "A note from the author." > foreword.txt
git add foreword.txt
git commit -m "Add foreword on main (diverges from feature)"
```

</details>

```bash
cd ex2_branches
```

**Step 1 — Visualize the branch structure:**
```bash
git lga
```
You should see two branches: `main` and `feature-ending`. They share a common root but diverge.

**Step 2 — See what branches exist:**
```bash
git branch
```
The `*` marks your current branch.

**Step 3 — Switch to the feature branch:**
```bash
git switch feature-ending
git lga
```
Notice that `foreword.txt` (added on `main`) is gone from your working directory — you are now looking at the feature branch's snapshot.

**Step 4 — Switch back and confirm the file returns:**
```bash
git switch main
ls
```
`foreword.txt` is back. Git swapped your entire working directory.

**Step 5 — Create a new branch from main:**
```bash
git switch -c experiment
git lga
```
`experiment` starts at the same commit as `main`.

**Step 6 — Make a commit on experiment:**
```bash
echo "An experimental idea." > idea.txt
git add idea.txt
git commit -m "Add experimental idea"
git lga
```
Now `experiment` is one commit ahead of `main`.

**Step 7 — Soft reset to undo the commit but keep the file:**
```bash
git reset --soft HEAD~1
git status
```
`idea.txt` is back in the staging area — the commit was undone but the file is safe.

**Step 8 — Delete the branch you made:**
```bash
git switch main
git branch -d experiment
```
The `experiment` branch still lacks a commit (you reset it), so `-d` will warn you. Use `-D` to force-delete it.

---

# 3. Merging — Combining Work from Two Branches

When you want to bring the changes from one branch into another, you *merge* them. Git has two main strategies for doing this.

## 3.1 Fast-Forward Merge

If the target branch has not received any new commits since the feature branch was created, Git can do a **fast-forward merge** — it simply slides the target branch pointer forward. No new commit is created.

**Before:**
```
A ──► B ──► C ──► D
      ▲           ▲
    (main)       (feature)
```

**After `git merge feature` (from main):**
```
A ──► B ──► C ──► D
                  ▲
              (main, feature)
```

This is like catching up to a friend who walked ahead of you — you just run to where they are.

---

## 3.2 Three-Way Merge (Standard Merge)

If both branches received new commits after their split, Git cannot simply slide a pointer. Instead, it finds the **common ancestor** and combines the two sets of changes into a brand-new **merge commit**:

**Before:**
```
        C ──► D
       /          (feature)
A ──► B
       \
        E ──► F   (main)
```

**After `git merge feature` (from main):**
```
        C ──► D
       /        \
A ──► B           M   (main) ← merge commit
       \        /
        E ──► F
```

The merge commit `M` has *two parents*, which is what makes it special.

---

## 3.3 No-Fast-Forward Merge

Sometimes you *want* a merge commit even when a fast-forward is possible, so that the branch history is visible in the log:

```bash
git merge --no-ff feature
```

This is useful in team projects where you want to see exactly which commits came from which feature branch.

---

## 3.4 Merge Conflicts — When Git Cannot Decide

A conflict happens when **both branches changed the same part of the same file**. Git does not know which version to keep, so it pauses and asks you to decide.

Git marks the conflicting section like this:

```
<<<<<<< HEAD
color: green
=======
color: red
>>>>>>> theme-red
```

- Everything between `<<<<<<< HEAD` and `=======` is **your current branch's version**.
- Everything between `=======` and `>>>>>>> theme-red` is the **incoming branch's version**.

**To resolve a conflict:**
1. Open the file in a text editor.
2. Delete the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
3. Edit the file to contain exactly what you want.
4. Save the file.
5. Mark it as resolved:
   ```bash
   git add config.txt
   ```
6. Complete the merge:
   ```bash
   git commit
   ```

---

## Exercise 3a — Fast-Forward Merge

Create a directory `ex3a_fast_forward` with a repository in the following state:

- **`main` branch** — two commits: initial `app.py` and a second commit adding a startup message
- **`add-greeting` branch** — forked from `main`'s second commit, with two more commits: adding `greet()` and then `farewell()` to `greet.py`
- `main` received **no new commits** after branching, so a fast-forward merge is possible
- You should be on `main` when you start the exercise

<details>
<summary>Setup: terminal commands</summary>

Run these commands from your `git_exercises/` directory:

```bash
mkdir ex3a_fast_forward
cd ex3a_fast_forward
git init -b main
cat > app.py << 'EOF'
print("Hello, world!")
EOF
git add app.py
git commit -m "Initial app"
cat > app.py << 'EOF'
print("Hello, world!")
print("App has started.")
EOF
git add app.py
git commit -m "Add startup message"
git switch -c add-greeting
cat > greet.py << 'EOF'
def greet(name):
    print(f'Hello, {name}!')
EOF
git add greet.py
git commit -m "Add greet function"
cat > greet.py << 'EOF'
def greet(name):
    print(f'Hello, {name}!')

def farewell(name):
    print(f'Goodbye, {name}!')
EOF
git add greet.py
git commit -m "Add farewell function"
git switch main
```

</details>

```bash
cd ex3a_fast_forward
```

**Step 1 — See the current situation:**
```bash
git lga
```
`main` is two commits behind `add-greeting`. There is no divergence.

**Step 2 — Merge:**
```bash
git merge add-greeting
```
Notice the output says *"Fast-forward"*. No merge commit was created.

**Step 3 — Confirm the result:**
```bash
git lga
```
Both labels now point at the same commit. The history is a straight line.

---

## Exercise 3b — Handling a Merge Conflict

Create a directory `ex3b_conflict` with a repository in the following state:

- **Common ancestor commit** on `main` — `config.txt` with `color: blue`
- **`theme-red` branch** — one commit changing `color` to `red`
- **`main` branch** — one commit (after branching) changing `color` to `green`
- Both branches modified the **same line**, guaranteeing a conflict
- You should be on `main` when you start the exercise

<details>
<summary>Setup: terminal commands</summary>

Run these commands from your `git_exercises/` directory:

```bash
mkdir ex3b_conflict
cd ex3b_conflict
git init -b main
cat > config.txt << 'EOF'
color: blue
font: Arial
size: 12
EOF
git add config.txt
git commit -m "Add config file (common ancestor)"
git switch -c theme-red
cat > config.txt << 'EOF'
color: red
font: Arial
size: 12
EOF
git add config.txt
git commit -m "Change color to red"
git switch main
cat > config.txt << 'EOF'
color: green
font: Arial
size: 12
EOF
git add config.txt
git commit -m "Change color to green"
```

</details>

```bash
cd ex3b_conflict
```

**Step 1 — See what happened:**
```bash
git lga
cat config.txt
```
The file shows `color: green` on main. The other branch changed it to `color: red`.

**Step 2 — Attempt the merge:**
```bash
git merge theme-red
```
Git will stop with a conflict message. Check the status:
```bash
git status
```
`config.txt` is listed as *"both modified"*.

**Step 3 — Look at the conflict markers:**
```bash
cat config.txt
```
You will see the `<<<<<<<` / `=======` / `>>>>>>>` markers.

**Step 4 — Resolve it** by opening `config.txt` in any text editor and replacing the entire conflict section with your desired result.

In vim using the [fugitive](https://github.com/tpope/vim-fugitive) extension the merge can be resolved with the `:Gvdiffsplit!` command.

For example:
```
color: purple
font: Arial
size: 12
```

**Step 5 — Mark it resolved and commit:**
```bash
git add config.txt
git commit -m "Resolve color conflict: chose purple"
git lga
```

---

# 4. Rebasing — Replaying Your Work on a New Foundation

Rebasing is an alternative to merging. Instead of combining two diverged histories with a merge commit, rebasing **replays** your commits as if you had started from a different point.

## 4.1 What Does "Replay" Mean?

Think of your commits as a series of edits you made to a document. Rebasing says:

> "Pretend I had started editing from *this newer version* of the document instead of the old one. Apply all my edits in order on top of the newer version."

Git takes each of your commits, one by one, and re-applies them onto the new base.

**Before rebase:**
```
A ──► B ──► C              (main)
      ▲
      └──► D ──► E         (feature-logger)
```

**After `git rebase main` from feature-logger:**
```
A ──► B ──► C ──► D' ──► E'   (feature-logger)
             ▲
           (main)
```

Notice the prime marks (D', E'). These are *new* commits — they have different hashes even though they contain the same code changes as D and E. The old D and E still exist temporarily but become unreachable.

---

## 4.2 Basic Rebase

```bash
# While on the feature branch:
git rebase main
```

If there is a conflict during a rebase, Git stops and asks you to resolve it (same process as merge conflicts). After resolving:

```bash
git add <resolved-file>
git rebase --continue    # apply the next commit
```

To cancel and go back to how things were before you started:
```bash
git rebase --abort
```

---

## 4.3 Interactive Rebase — Rewriting Commit History

Interactive rebase lets you **edit, reorder, rename, combine, or delete** commits before they are replayed. It is extremely useful for cleaning up messy work-in-progress commits before sharing your branch.

```bash
git rebase -i HEAD~3    # interactively edit the last 3 commits
```

Git opens a text editor with a list like this:

```
pick a1b2c3d Add initial logger
pick b2c3d4e Fix typo in logger
pick c3d4e5f Add error-level logging
```

You can change the word at the start of each line:

| Word | What it does |
|---|---|
| `pick` | Keep the commit as-is |
| `reword` | Keep the commit but let you edit its message |
| `edit` | Pause the rebase so you can modify the commit's content |
| `squash` | Combine this commit into the previous one (merge their messages too) |
| `fixup` | Like squash but discard this commit's message |
| `drop` | Delete this commit entirely |

**Example: combine the first two commits into one:**

Change the editor contents to:
```
pick a1b2c3d Add initial logger
squash b2c3d4e Fix typo in logger
pick c3d4e5f Add error-level logging
```

Save and close the editor. Git will then ask you to write a combined commit message for the squashed pair.

---

## 4.4 Rebase vs Merge — When to Use Which

| | Merge | Rebase |
|---|---|---|
| **History** | Preserves full history with merge commits | Creates a clean, linear history |
| **Original commits** | Kept intact | Replaced with new commits (new hashes) |
| **Best for** | Shared/public branches, preserving context | Local feature branches before sharing |
| **Danger** | Creates "noisy" history with many merge commits | Rewriting shared history breaks teammates' repos |

> [!WARNING]
> **Golden Rule of Rebasing:** Never rebase commits that have already been pushed to a shared remote branch. When you rebase, commits get new hashes. If your teammate has the old hashes, their history diverges from yours and everyone ends up in a very confusing state.

**Simple rule of thumb:**
- Rebase your own feature branch onto main *before* opening a pull request.
- Once the branch is on the remote and others have cloned it, use merge instead.

---

## Exercise 4 — Rebasing a Feature Branch

Create a directory `ex4_rebase` with a repository in the following state:

- **`main` branch** — three commits in this order:
  1. `main.py` — `"# Main entry point"` (commit A)
  2. `utils.py` — `"# Shared utilities"` (commit B)
  3. `config.py` — `DEBUG = True` and `VERSION = '1.0'` (commit C, added *after* branching)
- **`feature-logger` branch** — forked after commit B, with two commits:
  1. `logger.py` with a `log()` function (commit D)
  2. `logger.py` extended with an `error()` function (commit E)
- You should be on `feature-logger` when you start the exercise

<details>
<summary>Setup: terminal commands</summary>

Run these commands from your `git_exercises/` directory:

```bash
mkdir ex4_rebase
cd ex4_rebase
git init -b main
echo "# Main entry point" > main.py
git add main.py
git commit -m "A: Add main module"
echo "# Shared utilities" > utils.py
git add utils.py
git commit -m "B: Add utils module"
git switch -c feature-logger
cat > logger.py << 'EOF'
def log(msg):
    print(f'[LOG] {msg}')
EOF
git add logger.py
git commit -m "D: Add basic logger"
cat > logger.py << 'EOF'
def log(msg):
    print(f'[LOG] {msg}')

def error(msg):
    print(f'[ERROR] {msg}')
EOF
git add logger.py
git commit -m "E: Add error-level logging"
git switch main
cat > config.py << 'EOF'
DEBUG = True
VERSION = '1.0'
EOF
git add config.py
git commit -m "C: Add config module"
git switch feature-logger
```

</details>

```bash
cd ex4_rebase
```

**Step 1 — Understand the starting situation:**
```bash
git lga
```
You are on `feature-logger`. It branched off after commit B. Main has since added commit C. The histories have diverged.

**Step 2 — Rebase onto main:**
```bash
git rebase main
```
Watch the output: Git replays each commit. No conflicts should occur here.

**Step 3 — Inspect the result:**
```bash
git lga
```
The history is now a straight line: A → B → C → D' → E'. The feature branch sits cleanly on top of main's latest commit.

**Step 4 — Check that the files are all present:**
```bash
ls
```
You should see `main.py`, `utils.py`, `config.py` (from main), and `logger.py` (from the feature branch).

**Bonus: Interactive Rebase to Combine Commits**

The feature branch has two commits ("Add basic logger" and "Add error-level logging"). Combine them into one:

```bash
git rebase -i HEAD~2
```

In the editor, change `pick` to `squash` on the second line:
```
pick    <hash>  D: Add basic logger
squash  <hash>  E: Add error-level logging
```

Save and close. Git will ask for a combined message — write something like `Add logger with basic and error levels`, then save.

```bash
git lga
```
The two commits became one.

---

# 5. Reachability and Reflog — Nothing Is Truly Lost (For a While)

## 5.1 What Does "Reachable" Mean?

Every commit lives in Git's database. But a commit is only **reachable** if you can get to it by following pointers: starting from a branch or tag, following parent links backward.

```
A ──► B ──► C ──► D
      |           ▲
      |           (main)
      |
      └──► X ──► Y    ← no branch or tag points here; X and Y are unreachable
```

Git has a garbage collector that periodically deletes unreachable commits. Until it runs (usually after 30–90 days), they are still in the database.

---

## 5.2 The Reflog — Git's Internal Diary

Even if a commit becomes unreachable, Git keeps a private log of everywhere `HEAD` has been. This is the **reflog**:

```bash
git reflog
```

Output looks something like:
```
a4f3c21 HEAD@{0}: commit: Add notes file
7b2e9a8 HEAD@{1}: commit: Add line 3 — critical!
3d1c5f0 HEAD@{2}: commit: Add line 2
1a0b4e7 HEAD@{3}: commit: Add data file
```

Every entry has a **hash** that you can use to recover the commit, even if no branch points to it anymore.

---

## 5.3 Recovering Lost Work After a Hard Reset

**Scenario:** You ran `git reset --hard HEAD~2` and realize you needed those commits.

```bash
# 1. See the reflog to find the lost commits
git reflog

# 2. Find the hash of the commit you want to recover
#    (it will be listed as HEAD@{1} or HEAD@{2}, etc.)

# 3. Create a new branch at that commit
git branch recovered-work <hash>

# OR: simply reset main back to that commit
git reset --hard <hash>
```

---

## Exercise 5 — Recovering from a Hard Reset

Create a directory `ex5_reflog` with a repository in the following state:

- **Four commits on `main`**, in order:
  1. `data.txt` with `"Line 1: Important data"`
  2. `data.txt` extended with `"Line 2: More important data"`
  3. `data.txt` extended with `"Line 3: Critical information!"`
  4. `notes.txt` with `"Remember to check the logs."`

<details>
<summary>Setup: terminal commands</summary>

Run these commands from your `git_exercises/` directory:

```bash
mkdir ex5_reflog
cd ex5_reflog
git init -b main
echo "Line 1: Important data" > data.txt
git add data.txt
git commit -m "Add data file"
printf "Line 1: Important data\nLine 2: More important data\n" > data.txt
git add data.txt
git commit -m "Add line 2"
printf "Line 1: Important data\nLine 2: More important data\nLine 3: Critical information!\n" > data.txt
git add data.txt
git commit -m "Add line 3 — critical!"
echo "Remember to check the logs." > notes.txt
git add notes.txt
git commit -m "Add notes file"
```

</details>

```bash
cd ex5_reflog
```

**Step 1 — See the full history:**
```bash
git lga
```
There are 4 commits. Note the hashes — especially the top one (most recent).

**Step 2 — Simulate accidentally losing 2 commits:**
```bash
git reset --hard HEAD~2
git lga
```
Only 2 commits remain. The last two are "gone".

**Step 3 — Use the reflog to find the lost commit:**
```bash
git reflog
```
Look for the entry that says `commit: Add notes file` — that is the most recent commit before the reset. Note its hash (first 7 characters on the left).

**Step 4 — Recover by resetting to the old commit:**
```bash
git reset --hard <hash-from-reflog>
git lga
```
All 4 commits are back!

**Step 5 — Alternative recovery: create a branch instead of resetting main:**
```bash
# First, lose the commits again
git reset --hard HEAD~2

# Recover into a new branch instead
git branch rescue HEAD@{1}
git lga
```
Now `main` is at 2 commits and `rescue` points at the 4-commit version. You can compare them or merge `rescue` into `main`.

---

# 6. Tags — Permanent Bookmarks

## 6.1 What Is a Tag?

A tag is like a **sticky bookmark in a physical book** — it marks one specific page (commit) and never moves, even as you keep adding new pages. Tags are typically used to mark release versions.

Unlike a branch, a tag does not move when you make new commits.

```
A ──► B ──► C ──► D ──► E
      ▲           ▲
      (v0.1)      (v1.0)   ← tags stay permanently fixed
```

---

## 6.2 Lightweight vs Annotated Tags

| | Lightweight | Annotated |
|---|---|---|
| **What it is** | Just a pointer to a commit | A full Git object with message, author, and date |
| **Command** | `git tag v1.0` | `git tag -a v1.0 -m "Release 1.0"` |
| **Recommended for** | Quick local bookmarks | Official releases (use this for releases) |

---

## 6.3 Tag Commands

```bash
# Create a lightweight tag at the current commit
git tag v0.1

# Create an annotated tag (recommended for releases)
git tag -a v1.0 -m "First stable release"

# Tag a specific past commit (use its hash)
git tag -a v0.9 abc1234 -m "Release candidate"

# List all tags
git tag

# See the full details of an annotated tag
git show v1.0

# Go back to look at the code at a tagged version (detached HEAD)
git checkout v1.0

# Delete a local tag
git tag -d v0.1

# Push a single tag to the remote
git push origin v1.0

# Push ALL local tags to the remote at once
git push --tags
```

---

## Exercise 6 — Creating and Using Tags

Create a directory `ex6_tags` with a repository in the following state:

- **Three commits on `main`**, each representing a release:
  1. `app.py` — version `0.1.0`, alpha release
  2. `app.py` — version `0.2.0`, beta release with a `new_feature()` stub
  3. `app.py` — version `1.0.0`, stable release adding a `stable_api()` stub

<details>
<summary>Setup: terminal commands</summary>

Run these commands from your `git_exercises/` directory:

```bash
mkdir ex6_tags
cd ex6_tags
git init -b main
cat > app.py << 'EOF'
VERSION = "0.1.0"
print("App v0.1.0 — alpha")
EOF
git add app.py
git commit -m "Alpha release 0.1.0"
cat > app.py << 'EOF'
VERSION = "0.2.0"
print("App v0.2.0")

def new_feature():
    pass
EOF
git add app.py
git commit -m "Beta release 0.2.0 — add new feature"
cat > app.py << 'EOF'
VERSION = "1.0.0"
print("App v1.0.0 — stable")

def new_feature():
    pass

def stable_api():
    pass
EOF
git add app.py
git commit -m "Stable release v1.0.0"
```

</details>

```bash
cd ex6_tags
```

**Step 1 — See the three commits:**
```bash
git lga
```
Three commits represent three releases: 0.1.0, 0.2.0, and 1.0.0.

**Step 2 — Tag the most recent commit (v1.0.0) with an annotated tag:**
```bash
git tag -a v1.0.0 -m "First stable release"
```

**Step 3 — Tag the two earlier commits with lightweight tags:**
```bash
# Find the hash of the first commit (it's listed last in git lga)
git lga

# Tag using the hash (replace <hash1> and <hash2> with actual values)
git tag v0.1.0 <hash-of-first-commit>
git tag v0.2.0 <hash-of-second-commit>
```

**Step 4 — List all tags:**
```bash
git tag
```

**Step 5 — Inspect the annotated tag:**
```bash
git show v1.0.0
```
Notice it shows the tagger name, date, and message — much more information than a lightweight tag.

**Step 6 — Travel back to the v0.1.0 state:**
```bash
git checkout v0.1.0
cat app.py
```
You are now in detached HEAD, looking at the old code.

**Step 7 — Come back to main:**
```bash
git switch main
```

---

# Summary

Here is the mental model that ties everything together:

```
Working Directory  ──add──►  Staging Area  ──commit──►  HEAD (branch)
                                                              │
                                                         (linked to all
                                                          past commits)
```

| Concept | What it really is |
|---|---|
| **Working Directory** | The files you can see and edit on your disk |
| **Staging Area** | A selection of changes waiting to be committed |
| **HEAD** | A pointer to the current branch (or commit in detached mode) |
| **Branch** | A movable pointer to a commit; costs almost no disk space |
| **Merge** | Combines two commit chains; preserves full history |
| **Fast-forward merge** | Slides a branch pointer forward; no new commit |
| **Three-way merge** | Creates a new merge commit with two parents |
| **Rebase** | Replays commits on top of a new base; creates linear history |
| **Tag** | A fixed pointer to a commit; does not move |
| **Reflog** | Git's internal diary of where HEAD has been — your safety net |
| **Reachability** | Whether you can get to a commit by following branch/tag pointers |

## Practical Rules of Thumb

- **Rebase locally, merge publicly.** Clean up your feature branch with rebase before sharing; use merge once the branch is on the remote.
- **Prefer `git restore --staged` over `git reset`.** It is safer — it only unstages, does not touch your files.
- **When in doubt, check `git reflog`.** Almost nothing is permanently lost for the first 30–90 days.
- **Use annotated tags for releases.** They carry metadata that lightweight tags do not.
- **Commit small and often.** It is easier to squash small commits together than to split a big one apart.
- **Read `git status` before and after every command.** It tells you exactly which tree each file is in.

#!/usr/bin/env python3
"""
Git Intermediate Tutorial — Exercise Setup Script

Creates practice git repositories so you can follow along with the
Git Intermediate Tutorial hands-on exercises.

Works on Linux, macOS, and Windows (Python 3.7+).

Usage:
    python setup_git_exercises.py            # set up ALL exercises
    python setup_git_exercises.py 1 2 3a     # set up specific exercises
    python setup_git_exercises.py --list     # show available exercises
    python setup_git_exercises.py --clean    # delete all exercise repos
"""

import argparse
import subprocess
import sys
import shutil
from pathlib import Path


BASE_DIR = Path.cwd() / "git_exercises"


# ── low-level helpers ─────────────────────────────────────────────────────────

def run_git(args, cwd, check=True):
    """
    Run a git command inside `cwd`.
    Prints the command for transparency, returns the CompletedProcess result.
    """
    str_args = [str(a) for a in args]
    print(f"    $ git {' '.join(str_args)}")
    result = subprocess.run(
        ["git"] + str_args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        print(f"\n  [ERROR] Command failed: git {' '.join(str_args)}")
        if result.stderr.strip():
            print(f"  {result.stderr.strip()}")
        sys.exit(1)
    return result


def write_file(path: Path, content: str):
    """Write a text file, creating any missing parent directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    # Use explicit '\n' to get consistent line endings everywhere.
    path.write_text(content, encoding="utf-8", newline="\n")


def new_repo(name: str) -> Path:
    """
    Create a fresh git repository at BASE_DIR/<name>.
    Deletes the directory first if it already exists so the script is
    safe to re-run.  Sets up a local identity so the script works even
    if the user has never run 'git config --global'.
    """
    repo = BASE_DIR / name
    if repo.exists():
        shutil.rmtree(repo)
    repo.mkdir(parents=True)

    run_git(["init"], repo)

    # Make sure the default branch is called 'main' regardless of the
    # user's global init.defaultBranch setting or the git version.
    run_git(["symbolic-ref", "HEAD", "refs/heads/main"], repo)

    # Local identity (does not affect the user's global config).
    run_git(["config", "user.name",  "Tutorial Student"], repo)
    run_git(["config", "user.email", "student@tutorial.local"], repo)
    return repo


def commit_all(repo: Path, message: str):
    """Stage every change in the repo and create a commit."""
    run_git(["add", "--all"], repo)
    run_git(["commit", "-m", message], repo)


# ── formatting helpers ────────────────────────────────────────────────────────

def section_header(title: str):
    bar = "─" * 64
    print(f"\n{bar}")
    print(f"  {title}")
    print(bar)


def done_message(repo: Path, hint: str):
    print(f"\n  ✓  Repository created : {repo}")
    print(f"     {hint}")


# ── exercise setup functions ──────────────────────────────────────────────────

def setup_exercise_1(base: Path):
    """Exercise 1 — The Three Trees"""
    section_header("Exercise 1 — The Three Trees")
    repo = new_repo("ex1_three_trees")

    # ── commit 1 ──
    write_file(repo / "readme.txt", "Welcome to my project.\n")
    commit_all(repo, "Initial commit: add readme")

    # ── commit 2 ──
    write_file(repo / "notes.txt", "Remember to study Git!\n")
    commit_all(repo, "Add notes file")

    # Leave readme.txt modified in the working directory (NOT staged).
    write_file(repo / "readme.txt", "Welcome to my project.\nThis line was added but NOT staged yet.\n")

    # Leave a brand-new untracked file.
    write_file(repo / "scratch.txt", "I am an untracked file.\n")

    done_message(
        repo,
        "readme.txt is modified (unstaged) | scratch.txt is untracked",
    )


def setup_exercise_2(base: Path):
    """Exercise 2 — Branches"""
    section_header("Exercise 2 — Branches")
    repo = new_repo("ex2_branches")

    # ── two commits on main ──
    write_file(repo / "story.txt", "Chapter 1: The beginning.\n")
    commit_all(repo, "Add chapter 1")

    write_file(
        repo / "story.txt",
        "Chapter 1: The beginning.\nChapter 2: Things get interesting.\n",
    )
    commit_all(repo, "Add chapter 2")

    # ── branch off, add two commits ──
    run_git(["checkout", "-b", "feature-ending"], repo)

    write_file(
        repo / "story.txt",
        "Chapter 1: The beginning.\n"
        "Chapter 2: Things get interesting.\n"
        "Chapter 3: The epic ending.\n",
    )
    commit_all(repo, "Add chapter 3 on feature branch")

    write_file(repo / "epilogue.txt", "And they lived happily ever after.\n")
    commit_all(repo, "Add epilogue on feature branch")

    # ── go back to main and add a commit (creates divergence) ──
    run_git(["checkout", "main"], repo)
    write_file(repo / "foreword.txt", "A note from the author.\n")
    commit_all(repo, "Add foreword on main (diverges from feature)")

    done_message(
        repo,
        "main and feature-ending have diverged — try: git log --all --graph --oneline",
    )


def setup_exercise_3a(base: Path):
    """Exercise 3a — Fast-Forward Merge"""
    section_header("Exercise 3a — Fast-Forward Merge")
    repo = new_repo("ex3a_fast_forward")

    # ── two commits on main ──
    write_file(repo / "app.py", 'print("Hello, world!")\n')
    commit_all(repo, "Initial app")

    write_file(
        repo / "app.py",
        'print("Hello, world!")\nprint("App has started.")\n',
    )
    commit_all(repo, "Add startup message")

    # ── branch off and add two commits; main is NOT touched after this ──
    run_git(["checkout", "-b", "add-greeting"], repo)

    write_file(repo / "greet.py", "def greet(name):\n    print(f'Hello, {name}!')\n")
    commit_all(repo, "Add greet function")

    write_file(
        repo / "greet.py",
        "def greet(name):\n    print(f'Hello, {name}!')\n\n"
        "def farewell(name):\n    print(f'Goodbye, {name}!')\n",
    )
    commit_all(repo, "Add farewell function")

    # ── return to main so the student can run 'git merge add-greeting' ──
    run_git(["checkout", "main"], repo)

    done_message(
        repo,
        "main is behind add-greeting — run: git merge add-greeting",
    )


def setup_exercise_3b(base: Path):
    """Exercise 3b — Merge Conflict"""
    section_header("Exercise 3b — Merge Conflict")
    repo = new_repo("ex3b_conflict")

    # ── common ancestor ──
    write_file(repo / "config.txt", "color: blue\nfont: Arial\nsize: 12\n")
    commit_all(repo, "Add config file (common ancestor)")

    # ── branch: change color to red ──
    run_git(["checkout", "-b", "theme-red"], repo)
    write_file(repo / "config.txt", "color: red\nfont: Arial\nsize: 12\n")
    commit_all(repo, "Change color to red")

    # ── main: change color to green (same line — will conflict!) ──
    run_git(["checkout", "main"], repo)
    write_file(repo / "config.txt", "color: green\nfont: Arial\nsize: 12\n")
    commit_all(repo, "Change color to green")

    done_message(
        repo,
        "both branches changed the same line — run: git merge theme-red",
    )


def setup_exercise_4(base: Path):
    """Exercise 4 — Rebasing"""
    section_header("Exercise 4 — Rebasing")
    repo = new_repo("ex4_rebase")

    # ── commits A and B on main ──
    write_file(repo / "main.py", "# Main entry point\n")
    commit_all(repo, "A: Add main module")

    write_file(repo / "utils.py", "# Shared utilities\n")
    commit_all(repo, "B: Add utils module")

    # ── branch off at B, add commits D and E ──
    run_git(["checkout", "-b", "feature-logger"], repo)

    write_file(repo / "logger.py", "def log(msg):\n    print(f'[LOG] {msg}')\n")
    commit_all(repo, "D: Add basic logger")

    write_file(
        repo / "logger.py",
        "def log(msg):\n    print(f'[LOG] {msg}')\n\n"
        "def error(msg):\n    print(f'[ERROR] {msg}')\n",
    )
    commit_all(repo, "E: Add error-level logging")

    # ── add commit C to main AFTER branching to create divergence ──
    run_git(["checkout", "main"], repo)
    write_file(repo / "config.py", "DEBUG = True\nVERSION = '1.0'\n")
    commit_all(repo, "C: Add config module")

    # ── student will rebase feature-logger from here ──
    run_git(["checkout", "feature-logger"], repo)

    done_message(
        repo,
        "feature-logger is based on B; main now has C too — run: git rebase main",
    )


def setup_exercise_5(base: Path):
    """Exercise 5 — Reflog Recovery"""
    section_header("Exercise 5 — Reflog Recovery")
    repo = new_repo("ex5_reflog")

    write_file(repo / "data.txt", "Line 1: Important data\n")
    commit_all(repo, "Add data file")

    write_file(repo / "data.txt", "Line 1: Important data\nLine 2: More important data\n")
    commit_all(repo, "Add line 2")

    write_file(
        repo / "data.txt",
        "Line 1: Important data\nLine 2: More important data\nLine 3: Critical information!\n",
    )
    commit_all(repo, "Add line 3 — critical!")

    write_file(repo / "notes.txt", "Remember to check the logs.\n")
    commit_all(repo, "Add notes file")

    done_message(
        repo,
        "4 commits — run: git reset --hard HEAD~2   then recover with: git reflog",
    )


def setup_exercise_6(base: Path):
    """Exercise 6 — Tags"""
    section_header("Exercise 6 — Tags")
    repo = new_repo("ex6_tags")

    write_file(repo / "app.py", 'VERSION = "0.1.0"\nprint("App v0.1.0 — alpha")\n')
    commit_all(repo, "Alpha release 0.1.0")

    write_file(
        repo / "app.py",
        'VERSION = "0.2.0"\nprint("App v0.2.0")\n\ndef new_feature():\n    pass\n',
    )
    commit_all(repo, "Beta release 0.2.0 — add new feature")

    write_file(
        repo / "app.py",
        'VERSION = "1.0.0"\nprint("App v1.0.0 — stable")\n\n'
        "def new_feature():\n    pass\n\ndef stable_api():\n    pass\n",
    )
    commit_all(repo, "Stable release v1.0.0")

    done_message(
        repo,
        "3 commits representing three releases — practice creating tags",
    )


# ── exercise registry ─────────────────────────────────────────────────────────

EXERCISES: dict = {
    "1":  ("The Three Trees",      setup_exercise_1),
    "2":  ("Branches",             setup_exercise_2),
    "3a": ("Fast-Forward Merge",   setup_exercise_3a),
    "3b": ("Merge Conflict",       setup_exercise_3b),
    "4":  ("Rebasing",             setup_exercise_4),
    "5":  ("Reflog Recovery",      setup_exercise_5),
    "6":  ("Tags",                 setup_exercise_6),
}


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Set up Git exercise repositories for the Git Intermediate Tutorial.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  python setup_git_exercises.py            set up ALL exercises
  python setup_git_exercises.py 1 2 3a     set up only exercises 1, 2, 3a
  python setup_git_exercises.py --list     list available exercises
  python setup_git_exercises.py --clean    delete the git_exercises directory
""",
    )
    parser.add_argument(
        "exercises",
        nargs="*",
        metavar="N",
        help="Exercise IDs to set up (e.g. 1 2 3a). Omit to set up all.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Print available exercise IDs and exit.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete the git_exercises directory and exit.",
    )
    args = parser.parse_args()

    # ── --list ──
    if args.list:
        print("\nAvailable exercises:\n")
        for key, (name, _) in EXERCISES.items():
            print(f"  {key:>3}  —  {name}")
        print()
        return

    # ── --clean ──
    if args.clean:
        if BASE_DIR.exists():
            shutil.rmtree(BASE_DIR)
            print(f"Removed {BASE_DIR}")
        else:
            print("Nothing to clean (directory does not exist).")
        return

    # ── verify git is available ──
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
    except FileNotFoundError:
        print("\nERROR: 'git' was not found on your PATH.")
        print("Install git from https://git-scm.com and try again.\n")
        sys.exit(1)

    # ── resolve which exercises to set up ──
    selected = args.exercises if args.exercises else list(EXERCISES.keys())
    unknown = [e for e in selected if e not in EXERCISES]
    if unknown:
        print(f"\nERROR: Unknown exercise ID(s): {', '.join(unknown)}")
        print("Run  python setup_git_exercises.py --list  to see valid IDs.\n")
        sys.exit(1)

    BASE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\nCreating repos inside: {BASE_DIR}\n")

    for key in selected:
        _, fn = EXERCISES[key]
        fn(BASE_DIR)

    bar = "─" * 64
    print(f"\n{bar}")
    print("  All done!  Open a terminal, cd into one of the repos below,")
    print("  and follow the exercises in Git_intermediate.md.")
    print(f"\n  Location: {BASE_DIR}")
    print(bar + "\n")


if __name__ == "__main__":
    main()

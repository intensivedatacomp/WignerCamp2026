# 📝 Introduction to Vim

Vim is a text editor that lives entirely inside the terminal. It is pre-installed on virtually every Linux and macOS system, which means once you learn it, you can edit files on any server or remote machine without installing anything. This guide teaches you the essentials from scratch.

> 💡 The best way to learn Vim is the built-in tutorial. After reading this guide, run `vimtutor` in the terminal — it takes about 30 minutes and is excellent.

---

## 🤔 Why Learn Vim?

When you first open Vim, it feels strange. Nothing works the way you expect. But there is a good reason to push through that initial friction:

- **It is everywhere.** SSH into any Linux server, cloud machine, or Raspberry Pi — Vim is already there.
- **It is fast.** No mouse, no menus. Every action is a keystroke, and your hands never leave the keyboard.
- **It is permanent knowledge.** The skills transfer across every project and machine you ever work on.
- **It is the default editor for Git.** When Git opens an editor (for commit messages, merges, rebases), it opens Vim.

---

## 🧠 The Most Important Idea: Modes

This is the single thing that confuses every beginner. In most editors, pressing `a` types the letter "a". **In Vim, pressing `a` is a command** — unless you are in Insert mode.

Vim has separate **modes** for different tasks. The key rule is:

> **Always know which mode you are in.**

There are three modes you need to learn now:

| Mode | What it does | How to enter |
|------|-------------|--------------|
| **Normal** | Navigate and run commands | Press `Esc` from anywhere |
| **Insert** | Type text | Press `i` from Normal mode |
| **Command-Line** | Save, quit, search, replace | Press `:` from Normal mode |

When Vim opens, you are in **Normal mode**. This is your home base — you always return here with `Esc`.

### The mode indicator

At the bottom-left of the screen Vim shows which mode you are in:

```
-- INSERT --       ← you are typing text
-- VISUAL --       ← you are selecting text
                   ← blank means Normal mode
```

---

## 🚪 Opening, Saving, and Quitting

Open a file (or create a new one if it does not exist):

```bash
vim hello.txt
```

Once inside Vim, these commands control saving and quitting. Type them from **Normal mode**:

| Command | Action |
|---------|--------|
| `:w` | Save (write) the file |
| `:q` | Quit |
| `:wq` | Save and quit |
| `:q!` | Quit **without** saving (force quit) |

> ⚠️ If you ever feel stuck in Vim, press `Esc` a couple of times and then type `:q!` — this always gets you out.

### 🧪 Try This:

```bash
vim hello.txt
```

Inside Vim:
1. Press `i` to enter Insert mode — you will see `-- INSERT --` at the bottom.
2. Type: `Hello, world!`
3. Press `Esc` to return to Normal mode.
4. Type `:wq` and press `Enter` to save and quit.
5. Back in the terminal, check the result: `cat hello.txt`

---

## 🔁 The Three Modes in Detail

### Normal Mode — your home base

You are here when Vim opens. Every key is a **command**, not a character. Navigate, delete, copy, and move text here. Return here from any mode with `Esc`.

### Insert Mode — typing text

Enter it with `i`. Leave it with `Esc`. There are several ways to enter Insert mode, each starting at a different position:

| Key | Where it inserts |
|-----|-----------------|
| `i` | Before the cursor |
| `a` | After the cursor |
| `I` | At the very start of the line |
| `A` | At the very end of the line |
| `o` | Opens a new blank line **below** and starts typing |
| `O` | Opens a new blank line **above** and starts typing |

**Example:** You want to add a line after the current one.
- Press `o` — a new line opens below and you are in Insert mode immediately.
- Type your text, then press `Esc`.

### Command-Line Mode — running Ex commands

Press `:` from Normal mode. You will see a colon appear at the bottom of the screen. Type your command and press `Enter`. For example:

```vim
:w          ← save
:q          ← quit
:set number ← show line numbers
```

---

## 🧭 Moving Around

In Normal mode, the arrow keys work, but Vim's native movement keys are `h`, `j`, `k`, `l` on the home row of the keyboard. Using them keeps your hands in position.

| Key | Direction |
|-----|-----------|
| `h` | Left |
| `j` | Down |
| `k` | Up |
| `l` | Right |

But moving one character at a time is slow. These jump by larger amounts:

| Key | Jump |
|-----|------|
| `w` | Forward to the start of the next **w**ord |
| `b` | **B**ackward to the start of the previous word |
| `0` | Start of the line |
| `$` | End of the line |
| `gg` | Top of the file |
| `G` | Bottom of the file |
| `:15` | Go to line 15 (replace 15 with any number) |

You can also prefix any motion with a **count**:

| Command | Effect |
|---------|--------|
| `5j` | Move down 5 lines |
| `3w` | Jump forward 3 words |
| `10G` | Go to line 10 |

### 🧪 Try This:

Create a practice file:

```bash
for i in {1..20}; do echo "This is line $i"; done > practice.txt
vim practice.txt
```

Inside Vim (Normal mode):
1. Press `G` — go to the last line.
2. Press `gg` — jump back to the top.
3. Press `10G` — go to line 10.
4. Press `w` repeatedly — jump word by word.
5. Press `$` — go to the end of the line, then `0` to go back to the start.
6. Press `:q` to quit (no changes to save).

---

## ✏️ Editing Text

### Entering and leaving Insert mode

The most common editing pattern is:
1. Navigate in Normal mode to where you want to make a change.
2. Press a key to enter Insert mode.
3. Type your text.
4. Press `Esc` to return to Normal mode.

### Deleting

Deletions happen in **Normal mode** — no need to enter Insert mode.

| Command | Deletes |
|---------|---------|
| `x` | The character under the cursor |
| `dd` | The entire current line |
| `3dd` | 3 lines starting from the current one |
| `dw` | From cursor to the start of the next word |
| `D` | From cursor to the end of the line |

> 💡 Deleted text is not gone — it is saved and can be pasted with `p`.

### The change command

`c` works like `d` (delete) but immediately puts you in Insert mode so you can type a replacement:

| Command | Effect |
|---------|--------|
| `cw` | Delete to next word and start typing |
| `C` | Delete to end of line and start typing |
| `cc` | Delete entire line and start typing |

**Example:** Your cursor is on the word `oldName` and you want to replace it.
- Press `cw`, type `newName`, press `Esc`. Done.

### 🧪 Try This:

```bash
vim practice.txt
```

1. Navigate to line 5 using `5G`.
2. Press `dd` to delete it.
3. Press `u` to undo — the line comes back.
4. Press `cw` and type `CHANGED`, then `Esc`.
5. Press `:q!` to quit without saving.

---

## 📋 Copy and Paste

In Vim, "copy" is called **yank**.

| Command | Effect |
|---------|--------|
| `yy` | Yank (copy) the current line |
| `3yy` | Yank 3 lines |
| `yw` | Yank from cursor to next word |
| `p` | Paste **below** the current line (or after cursor) |
| `P` | Paste **above** the current line (or before cursor) |

> 💡 `dd` (delete) also puts the text in the paste buffer, so `dd` followed by `p` effectively **moves** a line.

### 🧪 Try This:

```bash
vim practice.txt
```

1. Go to line 1 with `gg`.
2. Press `yy` to copy the line.
3. Press `p` to paste a copy below it.
4. Press `dd` to delete the current line.
5. Move somewhere else and press `p` to paste it there.
6. Press `:q!` to quit.

---

## ↩️ Undo and Redo

| Command | Effect |
|---------|--------|
| `u` | Undo the last change |
| `Ctrl+r` | Redo (un-undo) |

You can undo many times in a row. Vim keeps the full history of your changes since you opened the file.

---

## 🔢 Line Numbers

Line numbers are essential for navigating larger files. Turn them on with:

```vim
:set number
```

Turn them off:

```vim
:set nonumber
```

To make line numbers permanent, add `set number` to your `~/.vimrc` file (Vim reads this file every time it starts).

---

## 🔎 Searching

Press `/` in Normal mode, type a search term, and press `Enter`. Vim jumps to the first match and highlights all occurrences.

```vim
/error        ← search forward for "error"
?error        ← search backward for "error"
n             ← jump to next match
N             ← jump to previous match
```

Press `Esc` to cancel a search in progress. To clear the search highlights:

```vim
:noh
```

> 💡 Press `*` in Normal mode to instantly search for the word under the cursor. This is extremely handy for finding all uses of a variable.

### 🧪 Try This:

```bash
vim practice.txt
```

1. Type `/line 1` and press `Enter`.
2. Press `n` to jump to the next match.
3. Press `N` to go back.
4. Press `*` with the cursor on any word to search for it.
5. Press `:noh` to clear the highlights.
6. Press `:q` to quit.

---

## 🔁 Search and Replace

The substitute command replaces text across the file. Run it from Command-Line mode (press `:`):

```vim
:s/old/new/          ← replace first match on the current line
:s/old/new/g         ← replace all matches on the current line
:%s/old/new/g        ← replace all matches in the entire file
:%s/old/new/gc       ← replace all, but ask for confirmation each time
```

The `%` means "the whole file". The trailing `g` means "all occurrences on each line" (without it, only the first match per line is replaced). The `c` flag shows each match and asks: `replace? (y/n/a/q)`.

### Examples

Replace `print` with `log` everywhere in the file:

```vim
:%s/print/log/g
```

Replace only in lines 5 to 10:

```vim
:5,10s/old/new/g
```

Add `#` at the start of lines 3 to 8 (comment them out):

```vim
:3,8s/^/# /
```

Remove the `#` from the start of lines 3 to 8 (uncomment):

```vim
:3,8s/^# //
```

### 🧪 Try This:

```bash
vim practice.txt
```

1. Type `:%s/line/LINE/g` and press `Enter` — all occurrences of "line" become "LINE".
2. Press `u` to undo.
3. Type `:%s/line/LINE/gc` — Vim asks for confirmation on each one. Press `y` to replace, `n` to skip, `q` to stop.
4. Press `:q!` to quit.

---

## 🧹 Visual Mode — Selecting Text

Press `v` in Normal mode to start selecting text character by character. Move the cursor to extend the selection. Then apply a command to the selected region.

| Key | Selection type |
|-----|---------------|
| `v` | Character by character |
| `V` | Whole lines |
| `Ctrl+v` | A rectangular block of columns |

Once text is selected:

| Key | Action |
|-----|--------|
| `d` | Delete the selection |
| `y` | Yank (copy) the selection |
| `>` | Indent the selection right |
| `<` | De-indent the selection left |

### 🧪 Try This:

```bash
vim practice.txt
```

1. Press `V` to start line selection.
2. Press `3j` to extend the selection 3 lines down.
3. Press `>` to indent those lines.
4. Press `u` to undo.
5. Press `Ctrl+v`, then `5j`, then `I# Esc` — this inserts `# ` at the start of 6 lines at once.
6. Press `:q!` to quit.

---

## 💡 The Most Common Beginner Mistakes

### Typing commands in Insert mode

**Symptom:** You press `dd` and instead of deleting a line, you see `dd` appearing in your text.

**Fix:** Press `Esc` first. You are in Insert mode. All editing commands only work in Normal mode.

### Getting lost in modes

**Fix:** If you are unsure which mode you are in, press `Esc` twice. You will always end up in Normal mode.

### Accidentally hitting `Ctrl+s`

**Symptom:** The terminal freezes and nothing responds.

**Fix:** Press `Ctrl+q` to unfreeze. This is a terminal feature unrelated to Vim.

### Forgetting to save

**Fix:** Get into the habit of pressing `:w` often, especially before running your code.

---

## 📊 Quick Reference

```
OPEN / QUIT
  vim file.txt       open a file
  :w                 save
  :q                 quit
  :wq                save and quit
  :q!                quit without saving (force)

MODES
  i                  enter Insert mode (before cursor)
  a                  enter Insert mode (after cursor)
  o                  new line below, enter Insert mode
  Esc                return to Normal mode

MOVEMENT (Normal mode)
  h j k l            left / down / up / right
  w   b              next / previous word
  0   $              start / end of line
  gg  G              top / bottom of file
  :15                go to line 15

EDITING (Normal mode)
  x                  delete character under cursor
  dd                 delete line
  dw                 delete word
  cc                 change entire line (delete + Insert mode)
  cw                 change word
  u                  undo
  Ctrl+r             redo

COPY/PASTE
  yy                 yank (copy) line
  p                  paste below
  P                  paste above

SEARCH
  /pattern           search forward
  n / N              next / previous match
  *                  search for word under cursor

REPLACE
  :%s/old/new/g      replace all in file
  :%s/old/new/gc     replace all, confirm each
```

---

## 🚀 What to Learn Next

Once these basics feel comfortable, the `Vim_intermediate.md` guide covers:
- **Text objects** — operate on words, sentences, paragraphs, and delimited regions (e.g. `ci"`, `dap`)
- **Macros** — record and replay sequences of commands
- **Regular expressions** — powerful pattern-based search and replace
- **Splits and tabs** — work with multiple files simultaneously
- **The dot command** — repeat your last change with `.`

---

## 📚 Resources

- `vimtutor` — run this in the terminal right now. It is the best 30-minute investment in learning Vim.
- `:help` — Vim's built-in documentation. Try `:help dd`, `:help motion`, etc.
- https://www.openvim.com/ — interactive browser-based practice
- https://vim-adventures.com/ — learn Vim through a puzzle game

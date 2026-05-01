# 📝 Vim Beginner’s Guide

Vim is a fast and powerful text editor available in the terminal. This guide teaches you how to use it effectively with practical commands and examples.

---

## 📄 Creating and Saving Files

Open a file (or create a new one):

```bash
vim filename.txt
```

### 🔧 Save & Exit

| Command | Description             |
|---------|-------------------------|
| `:w`    | Save (write) the file   |
| `:q`    | Quit Vim                |
| `:wq`   | Save and quit           |
| `:q!`   | Quit without saving     |

---

## 🔁 Vim Modes

### 1. **Normal Mode** (default)
- Use for navigation, editing commands
- Press `Esc` to enter Normal mode

### 2. **Insert Mode**
- Type text
- Enter with:
  - `i` — before cursor
  - `a` — after cursor
  - `I` — start of line
  - `A` — end of line

### 3. **Visual Mode**
- Select text:
  - `v` — character-wise
  - `V` — line-wise
  - `Ctrl+v` — block/column mode

### 4. **Command-Line Mode**
- Start with `:`
- Used for save, quit, search, replace, etc.

---

## 🧹 Deleting in Vim

### 🧾 Lines

| Command | Description            |
|---------|------------------------|
| `dd`    | Delete current line    |
| `3dd`   | Delete 3 lines         |
| `D`     | Delete to end of line  |

### 🪄 Characters

| Command | Description            |
|---------|------------------------|
| `x`     | Delete character under cursor |
| `X`     | Delete character before cursor |

---

## 🔎 Search and Replace

### 🔍 Search

```vim
/pattern       " Search forward
?pattern       " Search backward
n              " Repeat search
N              " Repeat in opposite direction
```

### 🔁 Replace

| Command | Description                                      |
|---------|--------------------------------------------------|
| `:s/old/new/`         | Replace first `old` with `new` in current line |
| `:s/old/new/g`        | Replace all in current line        |
| `:%s/old/new/g`       | Replace all in entire file         |
| `:%s/old/new/gc`      | Confirm each replacement           |

---

## 📋 Copy and Paste

### 🖱️ In Terminal (outside Vim)

- **Copy**: `Ctrl+Shift+C`
- **Paste**: `Ctrl+Shift+V`

### 📋 In Vim

| Command         | Description                |
|-----------------|----------------------------|
| `yy`            | Copy (yank) current line   |
| `3yy`           | Copy 3 lines               |
| `p`             | Paste below                |
| `P`             | Paste above                |
| `dd`            | Cut current line           |

### 🧠 Copy to System Clipboard (if supported)

```vim
"+y      # Yank selection to system clipboard
"+p      # Paste from system clipboard
```

> Note: Clipboard support requires Vim compiled with `+clipboard`.
> 
> 💡 Depending on the settings you may have to use `:3,5y *`.

---

## 🧭 Moving Around

| Key      | Action                      |
|----------|-----------------------------|
| `h/j/k/l`| Left/Down/Up/Right          |
| `0`      | Start of line               |
| `^`      | First non-blank character   |
| `$`      | End of line                 |
| `w`      | Next word                   |
| `b`      | Previous word               |
| `gg`     | Go to top of file           |
| `G`      | Go to bottom of file        |
| `:10`    | Go to line 10               |

---

## 🔢 Show Line Numbers

Temporary (in Vim):

```vim
:set number
:set relativenumber
:set norelativenumber
:set nonumber
```

Permanent (in `~/.vimrc`):

```vim
set number
set relativenumber
```

---

## ↩️ Undo / Redo

| Command   | Description         |
|-----------|---------------------|
| `u`       | Undo last change    |
| `U`       | Undo all on line    |
| `Ctrl+r`  | Redo undone change  |

---

## 🖥️ Open Terminal Inside Vim

Use this command to open a vertical split terminal:

```vim
:vert term
```

To return from terminal to Vim:

1. Use `Ctrl-w h` or `Ctrl-w l` to switch between terminal and file windows

To close the terminal:

```vim
exit
```

or use:

```vim
:q
```

---

## 🚀 Why Use Vim?

| Feature           | Vim Advantage                                |
|-------------------|-----------------------------------------------|
| Keyboard-driven   | Never take hands off keyboard                 |
| Modal editing     | Efficient separation of tasks                 |
| Lightweight       | Opens instantly, even over SSH                |
| Extensible        | Many plugins (file explorer, Git, LSP, etc.)  |
| Remote-friendly   | Works in headless/terminal environments       |

### 💡 Example: Delete All Blank Lines

```vim
:g/^$/d
```

### 💡 Example: Comment lines 10–20

```vim
:10,20s/^/# /
```

---

## 🧪 Try This Step-by-Step

```bash
vim demo.txt
```

Then in Vim:

1. Press `i` and write:
    ```
    Apple
    Banana
    Cherry
    ```
2. Press `Esc`
3. Press `yy` and `p` to copy/paste
4. Press `u` to undo, `Ctrl+r` to redo
5. Search: `/Banana`
6. Replace: `:%s/Banana/Grapes/g`
7. Open terminal: `:vert term`, then type `ls`, exit with `exit`
8. Quit: `:wq`

---

## 📚 Further Resources

- `:help` — built-in Vim docs
- https://www.openvim.com/
- https://vim-adventures.com/

# Vim — A Practical Guide

Vim is a fast, powerful, and keyboard-driven text editor available on virtually every Unix/Linux system. Once you internalize its logic, editing text becomes dramatically faster than with any mouse-dependent editor. This guide takes you from the basics to genuinely useful features, including regular expressions.

---

## Why Use Vim?

Most editors treat text editing as point-and-click. Vim treats it as a **language**: you compose commands from verbs and nouns, and the editor executes them precisely. Here is why that matters in practice.

### It is everywhere

Vim (or `vi`) is pre-installed on nearly every Linux server, embedded device, and remote machine. When you SSH into a cluster node, a Raspberry Pi, or a cloud VM, Vim is almost certainly there — no installation needed. Learning Vim means you always have a powerful editor available.

### It keeps your hands on the keyboard

The mouse is slow. Every time you reach for it, you break your flow. Vim is designed so that every operation — navigation, selection, deletion, search, replace — is a keystroke. Experienced Vim users edit code significantly faster than in GUI editors because they never context-switch between keyboard and mouse.

### It has a composable command grammar

This is Vim's most important idea. Commands follow a pattern:

```
[count] verb [motion/object]
```

For example:
- `d3w` — **d**elete **3** **w**ords
- `ci"` — **c**hange **i**nside **"** uotes
- `y$` — **y**ank (copy) to end of line
- `>ap` — indent **a** **p**aragraph

Once you learn the verbs, motions, and objects independently, you can combine them freely — thousands of combinations from a few dozen primitives.

### It runs in any terminal

Vim works over SSH, in containers, in tmux sessions, on minimal systems with no graphical environment. It starts in milliseconds. It handles files of any size without lag.

### It is highly configurable

A `~/.vimrc` file lets you customize every aspect of Vim's behavior. A rich plugin ecosystem (file explorers, Git integration, language servers, fuzzy finders) lets you build exactly the editor you want, with no unnecessary overhead.

---

## The Vim Modal System

Unlike most editors where typing always inserts text, Vim separates concerns into **modes**. Understanding modes is the key to Vim.

### Normal Mode (default)

This is where you spend most of your time. Every key is a command, not a character. Press `Esc` from any mode to return here.

```
Esc       → enter Normal mode from anywhere
```

### Insert Mode

This is where you type text. Enter it with:

| Key | Behavior |
|-----|----------|
| `i` | Insert before cursor |
| `a` | Insert after cursor (append) |
| `I` | Insert at start of line |
| `A` | Insert at end of line |
| `o` | Open new line below and insert |
| `O` | Open new line above and insert |
| `s` | Delete character under cursor and insert |
| `S` | Delete entire line and insert |
| `C` | Delete to end of line and insert |

### Visual Mode

Select text, then apply operators to the selection.

| Key | Selection type |
|-----|----------------|
| `v` | Character-wise |
| `V` | Line-wise |
| `Ctrl+v` | Block/column (rectangle) |

After selecting, press an operator: `d` to delete, `y` to yank, `c` to change, `>` to indent, `<` to de-indent.

### Command-Line Mode

Press `:` to enter Command-Line mode. Used for saving, quitting, search/replace, and running Ex commands.

### Replace Mode

Press `R` to enter Replace mode — typing overwrites existing characters one by one (like pressing Insert in a regular editor).

---

## Saving and Quitting

| Command | Action |
|---------|--------|
| `:w` | Save (write) |
| `:q` | Quit |
| `:wq` or `ZZ` | Save and quit |
| `:q!` or `ZQ` | Quit without saving |
| `:w filename` | Save to a new file |
| `:e filename` | Open (edit) another file |

---

## Navigation — Moving Around Precisely

### Basic movement

| Key | Motion |
|-----|--------|
| `h` / `l` | Left / Right (one character) |
| `j` / `k` | Down / Up (one line) |
| `0` | Start of line |
| `^` | First non-blank character of line |
| `$` | End of line |
| `gg` | Top of file |
| `G` | Bottom of file |
| `:42` or `42G` | Go to line 42 |
| `Ctrl+f` | Page down |
| `Ctrl+b` | Page up |
| `Ctrl+d` | Half-page down |
| `Ctrl+u` | Half-page up |

### Word movement

| Key | Motion |
|-----|--------|
| `w` | Next word start (punctuation counts as separate word) |
| `W` | Next WORD start (only whitespace as separator) |
| `b` | Previous word start |
| `B` | Previous WORD start |
| `e` | End of current/next word |
| `E` | End of current/next WORD |

### Character search on the current line

| Key | Motion |
|-----|--------|
| `f{char}` | Jump forward to next occurrence of `{char}` |
| `F{char}` | Jump backward to previous occurrence |
| `t{char}` | Jump to just before next `{char}` |
| `T{char}` | Jump to just after previous `{char}` |
| `;` | Repeat last `f`/`F`/`t`/`T` |
| `,` | Repeat in opposite direction |

**Example:** `dt,` deletes everything from the cursor up to (but not including) the next comma.

### Bracket/block matching

| Key | Action |
|-----|--------|
| `%` | Jump to the matching bracket: `(`, `)`, `[`, `]`, `{`, `}` |

**Example:** Position cursor on `(` and press `%` to jump to the closing `)`. Press `%` again to jump back.

### Marks — saving and returning to positions

Marks let you bookmark positions in the file.

| Command | Action |
|---------|--------|
| `ma` | Set mark `a` at current position |
| `` `a `` | Jump to exact position of mark `a` |
| `'a` | Jump to line of mark `a` |
| `` `` `` | Jump back to position before last jump |
| `''` | Jump back to line before last jump |

Capital letter marks (`mA`) are global — they persist across files.

---

## The Dot Command — Repeat Last Change

The `.` command repeats your last change. This is one of Vim's most useful features and the foundation of efficient editing.

**Scenario:** You want to add a semicolon to the end of every line in a block.
1. Go to first line, press `A;Esc` (append semicolon)
2. Go to next line, press `.` — same change applied instantly
3. Repeat `.` for each remaining line

**Scenario:** Replace a variable name in several places.
1. Search for it: `/oldName`
2. Change it: `ciwNewNameEsc`
3. Press `n` to jump to next match, `.` to apply the same change

---

## Text Objects — Operating on Structured Chunks

Text objects are one of Vim's most powerful features. They let operators act on meaningful units like words, sentences, paragraphs, or delimited regions.

Syntax: `{operator}{a or i}{object}`

- `a` — "around" (includes surrounding delimiters/whitespace)
- `i` — "inside" (excludes delimiters)

### Common text objects

| Command | Acts on |
|---------|---------|
| `iw` / `aw` | Inner word / A word (includes space) |
| `is` / `as` | Inner sentence / A sentence |
| `ip` / `ap` | Inner paragraph / A paragraph |
| `i"` / `a"` | Inside/around double quotes |
| `i'` / `a'` | Inside/around single quotes |
| `i(` / `a(` | Inside/around parentheses (also `ib`) |
| `i[` / `a[` | Inside/around square brackets |
| `i{` / `a{` | Inside/around curly braces (also `iB`) |
| `it` / `at` | Inside/around HTML/XML tag |

### Examples

| Command | Effect |
|---------|--------|
| `diw` | Delete the word under cursor |
| `ci"` | Delete contents of `"..."` and enter Insert mode |
| `ya(` | Yank (copy) everything inside `(...)` including the parens |
| `>ip` | Indent the current paragraph |
| `=i{` | Auto-indent the contents of the current `{...}` block |
| `dap` | Delete the current paragraph including surrounding blank lines |

---

## Operators (Verbs)

| Operator | Action |
|----------|--------|
| `d` | Delete (cuts to register) |
| `y` | Yank (copy) |
| `c` | Change (delete and enter Insert mode) |
| `>` | Indent right |
| `<` | Indent left |
| `=` | Auto-indent |
| `~` | Toggle case |
| `gu` | Make lowercase |
| `gU` | Make uppercase |
| `!` | Filter through external command |

Every operator works with any motion or text object. For example:
- `gUiw` — make current word uppercase
- `gu$` — lowercase from cursor to end of line
- `=G` — auto-indent from current line to end of file

---

## Deleting, Copying, and Pasting

### Deletion

| Command | Effect |
|---------|--------|
| `x` | Delete character under cursor |
| `X` | Delete character before cursor |
| `dd` | Delete current line |
| `D` | Delete to end of line |
| `3dd` | Delete 3 lines |
| `dw` | Delete to next word |
| `diw` | Delete inner word |

### Yanking (copying)

| Command | Effect |
|---------|--------|
| `yy` or `Y` | Yank current line |
| `3yy` | Yank 3 lines |
| `yw` | Yank to next word |
| `y$` | Yank to end of line |

### Pasting

| Command | Effect |
|---------|--------|
| `p` | Paste after cursor (or below line) |
| `P` | Paste before cursor (or above line) |

### Registers — named clipboards

Vim has multiple registers. Use `"` followed by a letter to specify one.

| Command | Effect |
|---------|--------|
| `"ayy` | Yank line into register `a` |
| `"ap` | Paste from register `a` |
| `"+y` | Yank to system clipboard |
| `"+p` | Paste from system clipboard |
| `"_d` | Delete to the black-hole register (nothing is saved) |
| `:reg` | Show contents of all registers |

> **Note:** Clipboard support requires Vim compiled with `+clipboard`. Check with `vim --version | grep clipboard`.

---

## Undo, Redo, and the Undo Tree

| Command | Action |
|---------|--------|
| `u` | Undo last change |
| `U` | Undo all changes on current line |
| `Ctrl+r` | Redo |
| `5u` | Undo last 5 changes |

Vim keeps a full undo tree, not just a linear history. Plugins like `undotree` expose this visually.

---

## Search

```vim
/pattern     " Search forward for pattern
?pattern     " Search backward for pattern
n            " Jump to next match
N            " Jump to previous match
*            " Search forward for word under cursor
#            " Search backward for word under cursor
```

Useful search options:

```vim
:set hlsearch    " Highlight all matches
:set incsearch   " Show matches as you type
:noh             " Clear search highlighting temporarily
:set ignorecase  " Case-insensitive search
:set smartcase   " Case-sensitive only when uppercase is used
```

---

## Regular Expressions in Vim

Vim uses its own regex dialect. Understanding it unlocks powerful search and replace operations.

### Anchors

| Pattern | Matches |
|---------|---------|
| `^` | Start of line |
| `$` | End of line |
| `\<` | Start of a word |
| `\>` | End of a word |

**Example:** `/\<for\>` matches the word `for` but not `forget` or `before`.

### Character classes

| Pattern | Matches |
|---------|---------|
| `.` | Any single character (except newline) |
| `[abc]` | Any one of `a`, `b`, or `c` |
| `[a-z]` | Any lowercase letter |
| `[A-Z]` | Any uppercase letter |
| `[0-9]` | Any digit |
| `[^abc]` | Any character except `a`, `b`, `c` |
| `\d` | Digit (same as `[0-9]`) |
| `\D` | Non-digit |
| `\w` | Word character (letter, digit, underscore) |
| `\W` | Non-word character |
| `\s` | Whitespace (space or tab) |
| `\S` | Non-whitespace |

### Quantifiers

In Vim's default (magic) mode:

| Pattern | Meaning |
|---------|---------|
| `*` | Zero or more of preceding |
| `\+` | One or more of preceding |
| `\?` | Zero or one of preceding (optional) |
| `\{n}` | Exactly n times |
| `\{n,m}` | Between n and m times |
| `\{n,}` | At least n times |

**Example:** `\d\+` matches one or more digits. `/\d\+\.\d\+` matches a decimal number like `3.14`.

### Groups and back-references

| Pattern | Meaning |
|---------|---------|
| `\(pattern\)` | Capture group |
| `\1`, `\2` | Back-reference to group 1, 2, ... |

**Example:** Swap the two words separated by a space:

```vim
:%s/\(\w\+\) \(\w\+\)/\2 \1/g
```

This matches `foo bar` and replaces it with `bar foo`.

### Very magic mode (`\v`)

In `\v` mode, most characters have special meaning without backslashes — similar to PCRE:

```vim
/\v<for>              " word boundary without \< \>
/\v\d+\.\d+           " decimal number (no need for \+)
:%s/\v(\w+) (\w+)/\2 \1/g  " swap words, cleaner syntax
```

### Practical regex examples

**Delete all blank lines:**

```vim
:g/^\s*$/d
```

**Delete lines containing a pattern:**

```vim
:g/TODO/d
```

**Keep only lines matching a pattern (delete everything else):**

```vim
:v/import/d
```

**Remove trailing whitespace from every line:**

```vim
:%s/\s\+$//
```

**Add a `#` comment marker to lines 10–20:**

```vim
:10,20s/^/# /
```

**Remove `#` comment markers from lines 10–20:**

```vim
:10,20s/^# //
```

**Find lines where a number appears twice:**

```vim
/\(\d\+\).*\1
```

**Replace `snake_case` with `camelCase` (first underscore only per line):**

```vim
:%s/_\([a-z]\)/\u\1/g
```

(`\u` uppercases the next character in the replacement.)

---

## The Global Command `:g`

`:g/pattern/command` runs a command on every line that matches a pattern. This is one of Vim's most powerful Ex features.

| Command | Effect |
|---------|--------|
| `:g/TODO/p` | Print all lines containing `TODO` |
| `:g/^$/d` | Delete all blank lines |
| `:g/^#/d` | Delete all comment lines starting with `#` |
| `:g/error/y A` | Append all lines containing `error` to register `a` |
| `:g/pattern/t$` | Copy all matching lines to end of file |

The inverse is `:v/pattern/command` (or `:g!/pattern/command`), which runs on lines that do **not** match:

```vim
:v/def /d    " Delete all lines that do NOT contain 'def '
```

---

## Search and Replace

### Basic substitution

```vim
:s/old/new/         " Replace first match on current line
:s/old/new/g        " Replace all matches on current line
:%s/old/new/g       " Replace all matches in entire file
:%s/old/new/gc      " Replace all, confirm each one
:5,15s/old/new/g    " Replace in lines 5–15
```

### Flags

| Flag | Meaning |
|------|---------|
| `g` | Replace all occurrences on each line |
| `c` | Confirm each replacement interactively |
| `i` | Case-insensitive match |
| `I` | Case-sensitive (overrides `ignorecase`) |
| `n` | Don't replace — just count and report matches |

### Special replacement sequences

| Sequence | Meaning |
|----------|---------|
| `\1`, `\2` | Captured group 1, 2 from the search pattern |
| `\u` | Uppercase next character |
| `\l` | Lowercase next character |
| `\U` | Uppercase rest of replacement |
| `\L` | Lowercase rest of replacement |
| `\E` | End case conversion started by `\U` or `\L` |
| `&` | The entire matched text |

**Example:** Capitalize the first letter of every word on the line:

```vim
:s/\<\w/\u&/g
```

---

## Macros — Recording and Replaying

Macros record a sequence of keystrokes and replay them.

1. Press `qa` — start recording into register `a`
2. Perform your edits (any Normal, Insert, Command-line actions)
3. Press `q` — stop recording
4. Press `@a` — replay the macro
5. Press `@@` — replay the last macro again
6. Press `50@a` — replay 50 times

**Example:** Add a trailing comma to every line in a block.

1. `qa` — start recording
2. `A,Esc` — go to end of line, insert `,`, return to Normal
3. `j` — move down one line
4. `q` — stop recording
5. `30@a` — apply to next 30 lines

---

## Working with Multiple Files: Splits and Tabs

### Splits

| Command | Action |
|---------|--------|
| `:sp filename` | Horizontal split, open file |
| `:vsp filename` | Vertical split, open file |
| `Ctrl+w h/j/k/l` | Move to split left/down/up/right |
| `Ctrl+w =` | Make all splits equal size |
| `Ctrl+w _` | Maximize current horizontal split |
| `Ctrl+w \|` | Maximize current vertical split |
| `Ctrl+w q` | Close current split |

### Tabs

| Command | Action |
|---------|--------|
| `:tabnew filename` | Open file in new tab |
| `gt` | Go to next tab |
| `gT` | Go to previous tab |
| `:tabclose` | Close current tab |
| `:tabs` | List all tabs |

### Navigating the buffer list

| Command | Action |
|---------|--------|
| `:ls` | List all open buffers |
| `:b3` | Switch to buffer 3 |
| `:bn` | Next buffer |
| `:bp` | Previous buffer |
| `:bd` | Delete (close) current buffer |

---

## Open Terminal Inside Vim

```vim
:vert term     " Open terminal in a vertical split
```

- Switch between terminal and file: `Ctrl+w h` / `Ctrl+w l`
- In the terminal, press `Ctrl+w N` to enter Normal mode in the terminal buffer (allows scrolling/copying)
- Close the terminal: type `exit` in the shell

---

## Line Numbers

Temporary (current session):

```vim
:set number          " Show absolute line numbers
:set relativenumber  " Show relative line numbers
:set nonumber        " Turn off line numbers
```

Permanent (in `~/.vimrc`):

```vim
set number
set relativenumber
```

Relative line numbers are especially useful with count-based commands: `3j` moves down exactly 3 lines, and the relative numbers confirm it visually.

---

## A Useful `~/.vimrc` Starter

```vim
set number
set relativenumber
set tabstop=4
set shiftwidth=4
set expandtab          " Use spaces instead of tabs
set hlsearch           " Highlight search results
set incsearch          " Incremental search
set ignorecase         " Case-insensitive search...
set smartcase          " ...unless uppercase is used
set autoindent
set scrolloff=5        " Keep 5 lines visible above/below cursor
set wildmenu           " Tab completion in command mode
syntax on
```

---

## Common Editing Patterns

### Rename a variable throughout a file

```vim
:%s/\<oldName\>/newName/gc
```

Using `\<` and `\>` ensures you only match the exact word, not substrings.

### Delete all lines containing a word

```vim
:g/deprecated/d
```

### Extract all matching lines into a new buffer

```vim
:g/ERROR/y A    " Yank all ERROR lines into register a (appending)
:enew           " Open new buffer
:put a          " Paste register a
```

### Format/indent an entire file

```vim
gg=G
```

(`gg` goes to top, `=G` auto-indents to bottom.)

### Join the next line to the current one

```vim
J
```

### Insert the same text on multiple lines (column edit)

1. `Ctrl+v` — enter block Visual mode
2. Select the lines with `j`
3. `I` — block insert
4. Type your text
5. `Esc` — the text appears on all selected lines

---

## Step-by-Step Practice

```bash
vim demo.py
```

Try these in sequence:

1. Press `i`, type a small Python function, press `Esc`
2. Use `gg` to go to the top, `G` to go to the bottom
3. Press `*` on a variable name to search for all occurrences
4. Press `ciw` on a word to change it; use `n` and `.` to repeat
5. Press `V` to select a line, `j` to extend, `>` to indent the block
6. Type `qa`, make a repetitive edit, press `q`, then `@a` to replay
7. Try `:%s/\(\w\+\) = \(\w\+\)/\2 = \1/gc` to swap assignments
8. Open a split: `:vsp demo2.py`, switch with `Ctrl+w l`, close with `:q`
9. Save and quit: `:wq`

---

## Quick Reference Card

```
MODES         i a o O s S C R    → Insert variants
              v V Ctrl+v         → Visual variants
              Esc                → Normal mode
              : / ?              → Command / Search

MOTION        hjkl  w b e  0 ^ $  gg G
              f{c} t{c} ; ,      → char search on line
              %                  → matching bracket

OPERATORS     d y c > < = ~ gu gU
              + motion or text object

TEXT OBJECTS  iw aw  i" a"  i( a(  ip ap  it at

USEFUL        .    → repeat last change
              *    → search word under cursor
              u    → undo   Ctrl+r → redo
              :g/pat/cmd  → global command
              :s/old/new/flags  → substitute
```

---

## Further Resources

- `vimtutor` — built-in interactive tutorial (run it in the terminal, takes ~30 min)
- `:help {topic}` — Vim's excellent built-in documentation
- https://www.openvim.com/ — interactive browser-based tutorial
- https://vim-adventures.com/ — learn Vim through a game
- https://vimsheet.com/ — concise cheat sheet

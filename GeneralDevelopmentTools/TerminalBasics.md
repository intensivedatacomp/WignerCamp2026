# 🐧 Getting Started with Linux Terminal

This guide introduces the basics of using the Linux terminal, a powerful tool for managing files, navigating the filesystem, and running programs. It includes key commands and practice exercises to help you gain confidence.

---

## 📁 1. Navigating the Filesystem

### 🔧 Common Commands

* `pwd` — Show current directory.
* `cd foldername` — Change to a directory.
* `cd ..` — Go one level up.
* `cd ~` — Go to your home folder.
* `ls` — List directory contents.
* `ls -l` — List in long format.
* `ls -a` — Show hidden files.

### 🧪 Try This:

```bash
pwd
cd ~
mkdir my_stuff
cd my_stuff
ls -la
cd ..
```

---

## 📄 2. Creating, Copying and Moving Files

### 🔧 File Commands

* `touch file.txt` — Create a file.
* `cp source.txt dest.txt` — Copy a file.
* `mv old.txt new.txt` — Rename or move file.
* `mkdir foldername` — Create a directory.
* `mv file.txt folder/` — Move file into folder.

### 🧪 Try This:

```bash
cd ~/my_stuff
touch hello.txt
cp hello.txt copy.txt
mv copy.txt renamed.txt
mkdir subfolder
mv renamed.txt subfolder/
```

---

## 🗑️ 3. Deleting Files and Directories

### 🔧 Delete Commands

* `rm file.txt` — Delete a file.
* `rm -r foldername` — Delete a directory recursively.
* `rm -i` — Interactive prompt before deleting.

> ⚠️ Deletion is permanent — no undo.

### 🧪 Try This:

```bash
rm hello.txt
rm -r subfolder
```

---

## 👓 4. Viewing File Contents

### 🔧 Viewing Tools

* `cat file.txt` — Display the whole file.
* `less file.txt` — Scroll through content (quit with `q`).
* `head file.txt` — Show first 10 lines.
* `tail file.txt` — Show last 10 lines.
* `tail -f file.txt` — Follow changes live (like a log file).
* `wc -l file.txt` — Count lines in file.

### 🧪 Try This:

```bash
echo "First line" > sample.txt
echo "Second line" >> sample.txt
cat sample.txt
```

---

## 🔁 Writing Multiple Lines with Loops

You can use a `for` loop to write multiple lines into a file:

### 🔧 Example:

```bash
for i in {1..150}; do
  echo "This is line $i" >> multi.txt
done
```

This loop:

* Runs `i` from 1 to 5.
* Appends a line to `multi.txt` on each iteration.

You can check the result with:

```bash
cat multi.txt
head multi.txt
tail multi.txt
less multi.txt
more multi.txt
```

> 💡 `>>` appends to the file. Use `>` to overwrite.

### 🧪 Try This:

```bash
rm -f multi.txt
for ((i = 0; i < 15; i++)); do
    echo "Row $i of data" >> multi.txt;
done
wc -l multi.txt
head multi.txt
```

---

## 📝 5. Editing with Vim

### 🔧 Vim Basics

* `vim file.txt` — Open file in Vim.
* Press `i` to enter *insert mode* (to write).
* Press `Esc` to leave insert mode.
* Type `:w` to save, `:q` to quit, `:wq` to save and quit.

> 💡 If stuck, type `Esc`, then `:q!` to quit without saving.

### 🧪 Try This:

```bash
vim mynotes.txt
```

> In Vim:
>
> 1. Press `i` and write: `Hello from Vim!`
> 2. Press `Esc`, type `:wq`, and press `Enter`.

---

## 📊 6. Monitoring and Measuring Programs

### 🔧 Tools

* `htop` — Interactive process viewer. Start with:

  ```bash
  htop
  ```

  (Use arrows to navigate, `q` to quit.)

* `time` — Measure how long a command takes:

  ```bash
  time sleep 2
  ```

* `top` — System resource usage:

  ```bash
  top
  ```

### 🧪 Try This:

```bash
time ls -lR /
```

> Note: You might need to install `htop` using:

```bash
sudo apt install htop   # Debian/Ubuntu
```

---

## 🎯 Challenge Task

Create a full project structure, edit a file, and monitor your system:

```bash
cd ~
mkdir myproject
cd myproject
for i in {1..5}; do echo "Experiment $i result" >> results.txt; done
vim results.txt   # Add extra info
mkdir backup
cp results.txt backup/
htop
cd ..
rm -r myproject
```

---

## ✅ Summary Table

| Action              | Command Example               |
| ------------------- | ----------------------------- |
| Show current folder | `pwd`                         |
| List files          | `ls -l`                       |
| Change folder       | `cd foldername`               |
| Make folder         | `mkdir myfolder`              |
| Create file         | `touch file.txt`              |
| Copy file           | `cp file1.txt file2.txt`      |
| Rename/move file    | `mv old.txt new.txt`          |
| Delete file         | `rm file.txt`                 |
| Delete folder       | `rm -r folder`                |
| View file           | `cat`, `less`, `head`, `tail` |
| Edit file           | `vim file.txt`                |
| Measure time        | `time command`                |
| View processes      | `htop`, `top`                 |

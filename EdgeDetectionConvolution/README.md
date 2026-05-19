# Convolution Learning Materials

This folder contains a structured set of learning materials designed to introduce and practice **convolution**, with a focus on image processing and its implementation in PyTorch.

The content is organized in a progressive way: starting from conceptual understanding, moving to practical API usage, and finally hands-on exercises.

---

## 1. Introduction to Convolution

The following files provide a conceptual introduction to convolution, including visual explanations and intuitive examples:

- 📓 [convolution_presentation.ipynb](./convolution_presentation.ipynb)
- 🌐 [convolution_presentation.slides.html](./convolution_presentation.slides.html)

These two files contain the **same content** in different formats:
- The notebook (`.ipynb`) is ideal for interactive exploration.
- The slides (`.html`) are optimized for presentation.

Topics covered include:
- What convolution is (weighted sum over a neighborhood)
- How kernels (filters) work
- Visual intuition behind image transformations (blur, edge detection, etc.)

---

## 2. Using `conv2d` in PyTorch

- 📓 [conv2d_function.ipynb](./conv2d_function.ipynb)

This notebook introduces the `torch.nn.functional.conv2d` function and demonstrates how convolution is implemented in practice.

Topics covered:
- Input and kernel tensor shapes
- Stride and padding
- Applying a convolution to an image

---

## 3. Practical Exercises

- 📁 [conv2d_exercise](./conv2d_exercise)

This folder contains hands-on exercises to reinforce understanding of convolution using PyTorch.

What you will find:
- Tasks requiring implementation of convolutions with different kernels
- Supporting code and tests to validate your solutions

---

## Suggested Learning Path

1. Start with the **presentation** to build intuition  
2. Move to the **conv2d notebook** to learn the API  
3. Complete the **exercise tasks** to gain practical experience  


---

## Goal

By the end of these materials, you should:
- Understand convolution conceptually
- Be able to apply convolution to images
- Use `conv2d` in PyTorch confidently
- Recognize common kernels and their effects

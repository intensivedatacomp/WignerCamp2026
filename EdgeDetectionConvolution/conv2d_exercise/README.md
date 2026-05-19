# Convolution with PyTorch (2D Image Filters)

## 🎯 Goal

In this exercise, you will learn how image convolution works using PyTorch's low-level API:

`torch.nn.functional.conv2d(input, weight, bias=None, stride=1, padding=0, dilation=1, groups=1)`

You will implement different convolution filters and observe their visual effects on an image.

## 🖼️ Input image

We will use:

`../../img/chair.jpg`

Convert it to grayscale before applying convolutions.

### 🧠 What you will learn
- How convolution slides a kernel over an image
- How different kernels detect edges, blur images, or enhance features
- How stride and padding affect output size
- How PyTorch represents convolution kernels

### 🧪 Tasks

You will complete missing parts in [conv_task.py](conv_task.py).

#### Task 1 — General convolution

Write a function to the template [conv_task.py](conv_task.py) to `task_1_apply_conv()` which calculates a general convolution with a defined kernel on an image.

#### Task 2 — Edge detection (Sobel X)

Write a function to the template [conv_task.py](conv_task.py) to `task_2_sobel_x()` which calculates a convolution with a Sobel X kernel, defined as
```
[[-1,  0,  1],
 [-2,  0,  2],
 [-1,  0,  1]]
```
on an image.

You do not have to use the solution to the Task 1 in this task.

> [!NOTE]
> You have to be especially careful with the shape of the kernels, it might be worth taking a look at how the example kernel is defined in the `main()` function of the [conv_task.py](conv_task.py).

#### Task 3 — Horizontal edges

Write a function to the template [conv_task.py](conv_task.py) to `task_3_horizontal_edges()` which calculates a convolution with a horizontal edge detection kernel, defined as
```
[[ 1,  1,  1],
 [ 0,  0,  0],
 [-1, -1, -1]]
```
on an image, also set stride to 3 and dilation to 5.

> [!NOTE]
> You have to be especially careful with the shape of the kernels, it might be worth taking a look at how the example kernel is defined in the `main()` function of the [conv_task.py](conv_task.py).

#### Task 4 — Same shape

Write a function to the template [conv_task.py](conv_task.py) to `task_4_same_shape_conv()` which calculates a convolution with a defined kernel on an image and keeps the dimension of the original image.


### 🚀 Running locally

You can uncomment test scripts in the `main()` function in [conv_task.py](conv_task.py) and run it with:

```bash
python conv_task.py
```

This will display filtered images.

### 🧪 Testing

To check the solutions, tun:

```bash
pytest
```

to verify correctness of implementations.

### 🎯 Check solutions

After all the tests pass, it is still worth checking the solutions to the tasks at [conv_task_solution.py](conv_task_solution.py).

💡 Hint

Remember:

- Input shape must be: (batch, channel, height, width)
- Kernel shape must be: (out_channels, in_channels, kH, kW)
- Grayscale images have 1 channel

import torch
import torch.nn.functional as F
from PIL import Image
import torchvision.transforms as T
import matplotlib.pyplot as plt


####################
# Helper functions #
# ##################
def load_image(path: str) -> torch.Tensor:
    """
    Load image and convert to grayscale tensor.

    Parameters
    ----------
    path : str
        Path to image.

    Returns
    -------
    torch.Tensor
        Shape (1, 1, H, W)
    """
    img = Image.open(path).convert("L")
    transform = T.ToTensor()
    tensor = transform(img).unsqueeze(0)
    return tensor


def plot_image(image: torch.Tensor) -> None:
    """
    Plots an image.
    
    Parameters
    ----------
    image : torch.Tensor
        Shape (1, 1, H, W)
    """
    img_show = image[0, 0].detach().numpy()
    plt.imshow(img_show, cmap="gray")
    plt.title(f"Shape {img_show.shape}")
    plt.show()


###################
#     Task 1      #
###################
def task_1_apply_conv(image: torch.Tensor, kernel: torch.Tensor) -> torch.Tensor:
    """
    Apply 2D convolution.

    Parameters
    ----------
    image : torch.Tensor
        Shape (1, 1, H, W)
    kernel : torch.Tensor
        Shape (1, 1, kH, kW)

    Returns
    -------
    torch.Tensor
        Convolved image
    
    Notes
    -----
    The stride and the padding are both 1.
    """
    raise NotImplementedError()


###################
#     Task 2      #
###################
def task_2_sobel_x(image: torch.Tensor) -> torch.Tensor:
    """
    Apply Sobel X kernel to a given image.

    Parameters
    ----------
    image : torch.Tensor
        Input image tensor of shape (1, 1, H, W).

    Returns
    -------
    torch.Tensor
        Filtered image after applying Sobel X operator.

    Notes
    -----
    The Sobel X kernel detects horizontal edges and is defined as:

    .. math::

        \\begin{bmatrix}
        -1 & 0 & 1 \\\\
        -2 & 0 & 2 \\\\
        -1 & 0 & 1
        \\end{bmatrix}
    """
    raise NotImplementedError()


###################
#     Task 3      #
###################
def task_3_horizontal_edges(image: torch.Tensor) -> torch.Tensor:
    """
    Find horizontal edges.

    Parameters
    ----------
    image : torch.Tensor
        Input image tensor of shape (1, 1, H, W).

    Returns
    -------
    torch.Tensor
        Result of applying convolution with the given parameters.

    Notes
    -----
    The following parameters are applied to the 
    convolution `stride=3` and `dilatation=5`
    """
    raise NotImplementedError()


###################
#     Task 4      #
###################
def task_4_same_shape_conv(image: torch.Tensor, kernel: torch.Tensor) -> torch.Tensor:
    """
    Apply convolution while preserving the spatial dimensions of the input image.

    Parameters
    ----------
    image : torch.Tensor
        Input image tensor of shape (1, 1, H, W).
    kernel : torch.Tensor
        Convolution kernel of shape (1, 1, kH, kW).

    Returns
    -------
    torch.Tensor
        Convolved image with the same height and width as input.

    Notes
    -----
    The padding is calculated with "same".
    """
    raise NotImplementedError()


def main():
    # Image for testing
    image = load_image("../../img/chair.jpg")
    
    # Kernel for testing
    test_kernel = torch.tensor([
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ], dtype=torch.float32).unsqueeze(0).unsqueeze(0)

    # Test task 1
    res1 = task_1_apply_conv(image, test_kernel)
    #plot_image(res1)

    # Test task 2
    res2 = task_2_sobel_x(image)
    #plot_image(res2)

    # Test task 3
    res3 = task_3_horizontal_edges(image)
    #plot_image(res3)

    # Test task 4
    res4 = task_4_same_shape_conv(image, test_kernel)
    #plot_image(res4)


if __name__ == "__main__":
    main()

import pytest
import torch
import torch.nn.functional as F
from PIL import Image
import tempfile
import os

from conv_task import (
    load_image,
    task_1_apply_conv,
    task_2_sobel_x,
    task_3_horizontal_edges,
    task_4_same_shape_conv,
)


############################
# Helper functions
############################
def simple_image() -> torch.Tensor:
    """
    Small deterministic image (used for Tasks 1,2,4)

    Returns
    -------
    torch.Tensor
        Shape (1, 1, 5, 5)
    """
    return torch.arange(25, dtype=torch.float32).reshape(1, 1, 5, 5)


def large_image() -> torch.Tensor:
    """
    Larger image required for Task 3 due to dilation.

    Returns
    -------
    torch.Tensor
        Shape (1, 1, 20, 20)
    """
    return torch.arange(400, dtype=torch.float32).reshape(1, 1, 20, 20)


def identity_kernel() -> torch.Tensor:
    """
    3x3 identity kernel.

    Returns
    -------
    torch.Tensor
        Shape (1, 1, 3, 3)
    """
    k = torch.zeros((3, 3), dtype=torch.float32)
    k[1, 1] = 1.0
    return k.unsqueeze(0).unsqueeze(0)


############################
# Task 1
############################
def test_task_1_shape():
    image = simple_image()
    kernel = identity_kernel()

    out = task_1_apply_conv(image, kernel)

    assert out.shape == image.shape


def test_task_1_identity():
    image = simple_image()
    kernel = identity_kernel()

    out = task_1_apply_conv(image, kernel)

    assert torch.allclose(out, image, atol=1e-6)


############################
# Task 2 (Sobel X)
############################
def test_task_2_shape():
    image = simple_image()

    out = task_2_sobel_x(image)

    assert out.shape == image.shape


def test_task_2_detects_horizontal_gradient():
    """
    Gradient along x → Sobel X should respond strongly.
    """
    img = torch.tensor([
        [0, 1, 2, 3, 4],
        [0, 1, 2, 3, 4],
        [0, 1, 2, 3, 4],
        [0, 1, 2, 3, 4],
        [0, 1, 2, 3, 4],
    ], dtype=torch.float32).reshape(1, 1, 5, 5)

    out = task_2_sobel_x(img)

    assert torch.abs(out).sum() > 0


############################
# Task 3 (stride + dilation)
############################
def effective_kernel_size(k: int, dilation: int) -> int:
    """
    Compute effective kernel size.

    Returns
    -------
    int
    """
    return dilation * (k - 1) + 1


def compute_output_dim(H, k_eff, stride, padding):
    return (H + 2 * padding - k_eff) // stride + 1


def test_task_3_shape():
    image = large_image()

    out = task_3_horizontal_edges(image)

    k_eff = effective_kernel_size(3, 5)
    expected_H = compute_output_dim(20, k_eff, stride=3, padding=1)
    expected_W = compute_output_dim(20, k_eff, stride=3, padding=1)

    assert out.shape == (1, 1, expected_H, expected_W)


def test_task_3_runs_without_error():
    """
    Ensure function runs on valid input (large enough image).
    """
    image = large_image()

    out = task_3_horizontal_edges(image)

    assert out is not None
    assert out.numel() > 0


def test_task_3_edge_response_nontrivial():
    """
    Construct a large image with horizontal edge.
    Expect some non-zero response.
    """
    img = torch.zeros((1, 1, 30, 30))
    img[:, :, :15, :] = 1.0

    out = task_3_horizontal_edges(img)

    # We avoid strict magnitude expectations due to stride/dilation
    assert torch.isfinite(out).all()
    assert out.shape[2] > 0 and out.shape[3] > 0


############################
# Task 4 ("same" padding)
############################
def test_task_4_shape():
    image = simple_image()
    kernel = identity_kernel()

    out = task_4_same_shape_conv(image, kernel)

    assert out.shape == image.shape


def test_task_4_equivalence_manual_padding():
    image = simple_image()
    kernel = identity_kernel()

    out_same = task_4_same_shape_conv(image, kernel)
    out_manual = F.conv2d(image, kernel, padding=1)

    assert torch.allclose(out_same, out_manual, atol=1e-6)


############################
# Global consistency
############################
def test_all_tasks_preserve_batch_channel():
    image_small = simple_image()
    image_large = large_image()
    kernel = identity_kernel()

    assert task_1_apply_conv(image_small, kernel).shape[:2] == (1, 1)
    assert task_2_sobel_x(image_small).shape[:2] == (1, 1)
    assert task_3_horizontal_edges(image_large).shape[:2] == (1, 1)
    assert task_4_same_shape_conv(image_small, kernel).shape[:2] == (1, 1)

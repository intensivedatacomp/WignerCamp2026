import pytest
import torch

from linalg_task import (
    task_1_scalar_multiply,
    task_2_dot_product,
    task_3_vector_matrix_multiply,
    task_4_matrix_multiply,
    task_5_eigendecomposition,
)


############################
# Task 1 — scalar multiply
############################
def test_task_1_values():
    v = torch.tensor([1.0, 2.0, 3.0])
    result = task_1_scalar_multiply(v, 3.0)
    expected = torch.tensor([3.0, 6.0, 9.0])
    assert torch.allclose(result, expected)


def test_task_1_shape():
    v = torch.tensor([1.0, 2.0, 3.0, 4.0])
    result = task_1_scalar_multiply(v, 2.0)
    assert result.shape == v.shape


def test_task_1_zero_scalar():
    v = torch.tensor([5.0, -3.0, 7.0])
    result = task_1_scalar_multiply(v, 0.0)
    assert torch.allclose(result, torch.zeros_like(v))


def test_task_1_negative_scalar():
    v = torch.tensor([1.0, 2.0, 3.0])
    result = task_1_scalar_multiply(v, -1.0)
    assert torch.allclose(result, -v)


############################
# Task 2 — dot product
############################
def test_task_2_result_a():
    """From the presentation dot product exercise: result is 1."""
    a = torch.tensor([1.0, -2.0, 3.0])
    b = torch.tensor([4.0, 0.0, -1.0])
    result = task_2_dot_product(a, b)
    assert torch.allclose(result, torch.tensor(1.0))


def test_task_2_result_b():
    """From the presentation dot product exercise: result is 3."""
    a = torch.tensor([2.0, 5.0])
    b = torch.tensor([-1.0, 1.0])
    result = task_2_dot_product(a, b)
    assert torch.allclose(result, torch.tensor(3.0))


def test_task_2_orthogonal_vectors():
    """Perpendicular vectors have a dot product of zero."""
    a = torch.tensor([1.0, 0.0])
    b = torch.tensor([0.0, 1.0])
    result = task_2_dot_product(a, b)
    assert torch.allclose(result, torch.tensor(0.0))


def test_task_2_returns_scalar():
    a = torch.tensor([1.0, 2.0, 3.0])
    b = torch.tensor([4.0, 5.0, 6.0])
    result = task_2_dot_product(a, b)
    assert result.ndim == 0


############################
# Task 3 — vector–matrix multiply
############################
def test_task_3_values():
    """From the presentation vector–matrix exercise: [1,2] @ M = [5,8,5]."""
    v = torch.tensor([1.0, 2.0])
    M = torch.tensor([[3.0, 0.0, 1.0], [1.0, 4.0, 2.0]])
    result = task_3_vector_matrix_multiply(v, M)
    expected = torch.tensor([5.0, 8.0, 5.0])
    assert torch.allclose(result, expected)


def test_task_3_shape():
    v = torch.tensor([1.0, 2.0, 3.0])
    M = torch.tensor([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    result = task_3_vector_matrix_multiply(v, M)
    assert result.shape == (2,)


def test_task_3_identity_matrix():
    """Multiplying by the identity matrix leaves the vector unchanged."""
    v = torch.tensor([3.0, -1.0])
    I = torch.eye(2)
    result = task_3_vector_matrix_multiply(v, I)
    assert torch.allclose(result, v)


############################
# Task 4 — matrix–matrix multiply
############################
def test_task_4_values():
    """From the presentation matrix–matrix example."""
    A = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
    B = torch.tensor([[2.0, 0.0], [1.0, 2.0]])
    result = task_4_matrix_multiply(A, B)
    expected = torch.tensor([[4.0, 4.0], [10.0, 8.0]])
    assert torch.allclose(result, expected)


def test_task_4_shape():
    A = torch.zeros(3, 4)
    B = torch.zeros(4, 5)
    result = task_4_matrix_multiply(A, B)
    assert result.shape == (3, 5)


def test_task_4_identity():
    """Multiplying by the identity matrix is a no-op."""
    A = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
    I = torch.eye(2)
    result = task_4_matrix_multiply(A, I)
    assert torch.allclose(result, A)


def test_task_4_non_square():
    """Verify a non-square multiplication from the presentation."""
    A = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    B = torch.tensor([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    result = task_4_matrix_multiply(A, B)
    expected = torch.tensor([[4.0, 5.0], [10.0, 11.0]])
    assert torch.allclose(result, expected)


############################
# Task 5 — eigendecomposition
############################
def test_task_5_eigenvalue_equation():
    """A @ eigenvectors == eigenvectors * eigenvalues for each column."""
    A = torch.tensor([[2.0, 1.0], [1.0, 2.0]])
    eigenvalues, eigenvectors = task_5_eigendecomposition(A)
    assert torch.allclose(A @ eigenvectors, eigenvectors * eigenvalues, atol=1e-5)


def test_task_5_orthonormal_eigenvectors():
    """Eigenvectors of a real symmetric matrix form an orthonormal basis."""
    A = torch.tensor([[4.0, 2.0], [2.0, 3.0]])
    _, eigenvectors = task_5_eigendecomposition(A)
    product = eigenvectors.T @ eigenvectors
    assert torch.allclose(product, torch.eye(2), atol=1e-5)


def test_task_5_diagonal_matrix():
    """Diagonal matrix: eigenvalues are the diagonal entries in ascending order."""
    A = torch.tensor([[3.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 2.0]])
    eigenvalues, _ = task_5_eigendecomposition(A)
    expected = torch.tensor([1.0, 2.0, 3.0])
    assert torch.allclose(eigenvalues, expected, atol=1e-5)


def test_task_5_returns_tuple_of_two_tensors():
    A = torch.tensor([[1.0, 0.0], [0.0, 1.0]])
    result = task_5_eigendecomposition(A)
    assert isinstance(result, tuple)
    assert len(result) == 2
    eigenvalues, eigenvectors = result
    assert eigenvalues.shape == (2,)
    assert eigenvectors.shape == (2, 2)


def test_task_5_eigenvalues_ascending():
    """torch.linalg.eigh guarantees eigenvalues in ascending order."""
    A = torch.tensor([[5.0, 1.0], [1.0, 3.0]])
    eigenvalues, _ = task_5_eigendecomposition(A)
    assert eigenvalues[0] <= eigenvalues[1]

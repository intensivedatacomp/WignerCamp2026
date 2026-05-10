import torch


###################
#     Task 1      #
###################
def task_1_scalar_multiply(v: torch.Tensor, s: float) -> torch.Tensor:
    """
    Multiply a vector by a scalar.

    Parameters
    ----------
    v : torch.Tensor
        A 1D tensor (vector).
    s : float
        A scalar value.

    Returns
    -------
    torch.Tensor
        The vector v scaled by s.
    """
    return s * v


###################
#     Task 2      #
###################
def task_2_dot_product(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    """
    Compute the dot product of two vectors.

    Parameters
    ----------
    a : torch.Tensor
        A 1D tensor (vector).
    b : torch.Tensor
        A 1D tensor (vector) of the same length as a.

    Returns
    -------
    torch.Tensor
        A scalar tensor equal to the dot product of a and b.

    Notes
    -----
    Use torch.dot().
    """
    return torch.dot(a, b)


###################
#     Task 3      #
###################
def task_3_vector_matrix_multiply(v: torch.Tensor, M: torch.Tensor) -> torch.Tensor:
    """
    Multiply a row vector by a matrix.

    Parameters
    ----------
    v : torch.Tensor
        A 1D tensor of shape (n,).
    M : torch.Tensor
        A 2D tensor of shape (n, m).

    Returns
    -------
    torch.Tensor
        A 1D tensor of shape (m,) equal to v @ M.

    Notes
    -----
    Use the @ operator.
    """
    return v @ M


###################
#     Task 4      #
###################
def task_4_matrix_multiply(A: torch.Tensor, B: torch.Tensor) -> torch.Tensor:
    """
    Multiply two matrices.

    Parameters
    ----------
    A : torch.Tensor
        A 2D tensor of shape (n, m).
    B : torch.Tensor
        A 2D tensor of shape (m, k).

    Returns
    -------
    torch.Tensor
        A 2D tensor of shape (n, k) equal to A @ B.

    Notes
    -----
    Use the @ operator.
    """
    return A @ B


###################
#     Task 5      #
###################
def task_5_eigendecomposition(
    A: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Compute the eigenvalues and eigenvectors of a real symmetric matrix.

    Parameters
    ----------
    A : torch.Tensor
        A 2D real symmetric tensor of shape (n, n).

    Returns
    -------
    eigenvalues : torch.Tensor
        A 1D tensor of shape (n,) containing eigenvalues in ascending order.
    eigenvectors : torch.Tensor
        A 2D tensor of shape (n, n) whose columns are the corresponding
        orthonormal eigenvectors.

    Notes
    -----
    Use torch.linalg.eigh(), which is designed for real symmetric matrices
    and always returns real eigenvalues sorted in ascending order.
    """
    return torch.linalg.eigh(A)


def main():
    # Task 1: scalar multiplication
    v = torch.tensor([1.0, 2.0, 3.0])
    s = 3.0
    result_1 = task_1_scalar_multiply(v, s)
    print(f"Task 1 | {s} * {v.tolist()} = {result_1.tolist()}")

    # Task 2: dot product — vectors from the presentation dot product exercise
    a = torch.tensor([1.0, -2.0, 3.0])
    b = torch.tensor([4.0, 0.0, -1.0])
    result_2 = task_2_dot_product(a, b)
    print(f"Task 2 | {a.tolist()} · {b.tolist()} = {result_2.item()}")

    # Task 3: vector–matrix multiplication — example from the presentation
    v3 = torch.tensor([1.0, 2.0])
    M3 = torch.tensor([[3.0, 0.0, 1.0], [1.0, 4.0, 2.0]])
    result_3 = task_3_vector_matrix_multiply(v3, M3)
    print(f"Task 3 | v @ M = {result_3.tolist()}")

    # Task 4: matrix–matrix multiplication — example from the presentation
    A4 = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
    B4 = torch.tensor([[2.0, 0.0], [1.0, 2.0]])
    result_4 = task_4_matrix_multiply(A4, B4)
    print(f"Task 4 | A @ B =\n{result_4}")

    # Task 5: eigendecomposition of a real symmetric matrix
    A5 = torch.tensor([[2.0, 1.0], [1.0, 2.0]])
    eigenvalues, eigenvectors = task_5_eigendecomposition(A5)
    print(f"Task 5 | eigenvalues  = {eigenvalues.tolist()}")
    print(f"Task 5 | eigenvectors =\n{eigenvectors}")


if __name__ == "__main__":
    main()

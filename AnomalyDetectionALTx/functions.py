import torch

def generate_recursive_array(weights: list[float], start_values: list[float], length: int) -> torch.Tensor:
    """
    Generate a 1D tensor by recursively applying a linear relation.

    Each new value is computed as a linear combination of the last `len(weights)` values,
    using the provided `weights`. The recursion starts from the initial values in `start_values`.

    Parameters
    ----------
    weights : list[float]
        The weights to apply in the linear recursion. Must match the length of `start_values`.
    start_values : list[float]
        The initial values that seed the recursion. Must match the length of `weights`.
    length : int
        The total number of elements to generate (must be >= len(start_values)).

    Returns
    -------
    torch.Tensor
        A 1D tensor of shape `(length,)` containing the generated sequence.

    Raises
    ------
    AssertionError
        If `len(weights)` is not equal to `len(start_values)`.
    """
    assert len(weights) == len(start_values), "Weights and starting values must be the same length."
    result = start_values[:]
    
    for i in range(len(start_values), length):
        next_value = sum(weights[j] * result[i - len(weights) + j] for j in range(len(weights)))
        result.append(next_value)
    
    return torch.tensor(result, dtype=torch.float32)

def extract_symmetric_laws(x: torch.Tensor) -> torch.Tensor:
    """
    Extract normalized eigenvectors of 2x2 symmetric matrices constructed from a 1D tensor.

    Given a 1D tensor `x` of length `n`, constructs `n-2` symmetric 2x2 matrices of the form:
    [[x[i], x[i+1]],
     [x[i+1], x[i+2]]]
    Then computes the eigenvector corresponding to the eigenvalue with the smallest absolute value
    and returns them as a tensor.

    Assumes all constructed matrices are symmetric.

    Parameters
    ----------
    x : torch.Tensor or list[float]
        1D tensor of shape `(n,)` with `n >= 3`.

    Returns
    -------
    torch.Tensor
        A tensor of shape `(2, n-2)` where each column is a normalized eigenvector
        of the corresponding 2x2 matrix.
    
    Raises
    ------
    ValueError
        If the input tensor is not 1D or has fewer than 3 elements.
    """
    if type(x) is list:
        x = torch.tensor(x, dtype=torch.float32)
    
    if x.ndim != 1 or x.shape[0] < 3:
        raise ValueError("Input must be a 1D tensor with at least 3 elements.")
    
    result = []
    for i in range(len(x) - 2):
        S = torch.tensor([[x[i], x[i+1]],
                          [x[i+1], x[i+2]]], dtype=torch.float32)
        eigvals, eigvecs = torch.linalg.eig(S)
        eigvals_abs = eigvals.abs()
        min_idx = torch.argmin(eigvals_abs)
        real_vec = eigvecs[:, min_idx].real
        result.append(real_vec / real_vec.norm())

    return torch.stack(result).T

def embed_as_pairs(x: torch.Tensor) -> torch.Tensor:
    """
    Embed a 1D tensor into overlapping pairs of adjacent elements.

    For an input tensor `x` of length `n`, returns a 2D tensor of shape `(n-1, 2)` where each row is:
    [x[i], x[i+1]] for i in 0 to n-2.

    Parameters
    ----------
    x : torch.Tensor
        1D input tensor of shape `(n,)` with `n >= 2`.

    Returns
    -------
    torch.Tensor
        2D tensor of shape `(n-1, 2)`, containing adjacent pairs from the input.
    
    Raises
    ------
    ValueError
        If the input tensor is not 1D or has fewer than 2 elements.
    """
    if type(x) is list:
        x = torch.tensor(x, dtype=torch.float32)
    
    if x.ndim != 1 or x.shape[0] < 2:
        raise ValueError("Input must be a 1D tensor with at least 2 elements.")
    
    return torch.stack([x[:-1], x[1:]], dim=1)

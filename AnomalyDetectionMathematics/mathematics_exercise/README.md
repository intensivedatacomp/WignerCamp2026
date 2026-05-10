# Linear Algebra with PyTorch

## Goal

In this exercise you will practise the fundamental linear algebra operations covered in the presentation using PyTorch tensors.

You will complete the missing implementations in [linalg_task.py](linalg_task.py).

## What you will learn

- How to create and manipulate `torch.Tensor` objects as vectors and matrices.
- How scalar multiplication, the dot product, and matrix products are expressed in PyTorch.
- How to use the `@` operator for vector–matrix and matrix–matrix multiplication.
- How to compute eigenvalues and eigenvectors of a real symmetric matrix with `torch.linalg.eigh`.

## Tasks

### Task 1 — Scalar multiplication

Complete `task_1_scalar_multiply(v, s)` in [linalg_task.py](linalg_task.py).

Given a 1D tensor `v` and a scalar `s`, return the vector scaled by `s`.

### Task 2 — Dot product

Complete `task_2_dot_product(a, b)` in [linalg_task.py](linalg_task.py).

Given two 1D tensors of equal length, return their dot product as a scalar tensor.

Use `torch.dot()`.

### Task 3 — Vector–matrix multiplication

Complete `task_3_vector_matrix_multiply(v, M)` in [linalg_task.py](linalg_task.py).

Given a 1D tensor `v` of shape `(n,)` and a 2D tensor `M` of shape `(n, m)`, return the result of multiplying the row vector by the matrix.

Use the `@` operator.

### Task 4 — Matrix–matrix multiplication

Complete `task_4_matrix_multiply(A, B)` in [linalg_task.py](linalg_task.py).

Given two 2D tensors `A` of shape `(n, m)` and `B` of shape `(m, k)`, return their matrix product.

Use the `@` operator.

### Task 5 — Eigendecomposition

Complete `task_5_eigendecomposition(A)` in [linalg_task.py](linalg_task.py).

Given a real symmetric 2D tensor `A` of shape `(n, n)`, return a tuple `(eigenvalues, eigenvectors)` where:

- `eigenvalues` is a 1D tensor of shape `(n,)` with eigenvalues in ascending order,
- `eigenvectors` is a 2D tensor of shape `(n, n)` whose columns are the corresponding orthonormal eigenvectors.

Use `torch.linalg.eigh()`, which is designed for real symmetric matrices.

## Running locally

You can run the task file directly to see the output of your implementations:

```bash
python linalg_task.py
```

## Testing

Run the test suite with:

```bash
pytest
```

All five tasks must pass before you check the solutions.

## Check solutions

After all tests pass, compare your implementations with [linalg_task_solution.py](linalg_task_solution.py).

"""
BIT 2118: SCIENTIFIC COMPUTING
Task 8: Iterative Methods for Linear Systems

B. Identify the input values and the mathematical operation performed.
- Input values: A tridiagonal coefficient matrix `A` modeling 1D diffusion, and a boundary condition vector `b`.
- Mathematical operations: Matrix operations inside a loop to iteratively estimate the solution using Jacobi and Gauss-Seidel formulas, updating `x` until the infinite norm of the error drops below `tol`.

C. Change at least one input/parameter and explain how the result changes.
- Change: Increase the tolerance `tol` from `1e-8` to `1e-3`.
- Result: Both Jacobi and Gauss-Seidel will stop after fewer iterations. The final concentration estimates will be computed faster but will be slightly less accurate compared to the exact direct solution.

D. Explain the meaning of the output in words and interpret the graph where necessary.
- Output meaning: The script outputs the equilibrium chemical concentrations across interior nodes. The graph plots the error at each iteration on a logarithmic scale, showing that Gauss-Seidel converges to the solution faster (steeper downward slope) than Jacobi.

E. Modify the program to solve a different but related real-world case.
- New Case: Chemical concentration diffusion in a pipe connecting two reservoirs. The ends are kept at constant concentrations (e.g., 50 mol/L and 10 mol/L), and we need the steady-state concentration at intermediate points.
"""
import numpy as np
import matplotlib.pyplot as plt

# Chemical diffusion 1D model (5 interior points)
A = np.array([
    [ 2., -1.,  0.,  0.,  0.],
    [-1.,  2., -1.,  0.,  0.],
    [ 0., -1.,  2., -1.,  0.],
    [ 0.,  0., -1.,  2., -1.],
    [ 0.,  0.,  0., -1.,  2.]
])

# Boundary conditions: left reservoir = 50 mol/L, right = 10 mol/L
b = np.array([50., 0., 0., 0., 10.])

def jacobi(A, b, tol=1e-8, max_iter=500):
    D = np.diag(A)
    R = A - np.diagflat(D)
    x = np.zeros_like(b)
    errors = []
    for _ in range(max_iter):
        x_new = (b - R @ x) / D
        error = np.linalg.norm(x_new - x, ord=np.inf)
        errors.append(error)
        if error < tol: break
        x = x_new
    return x, errors

def gauss_seidel(A, b, tol=1e-8, max_iter=500):
    x = np.zeros_like(b)
    errors = []
    for _ in range(max_iter):
        old = x.copy()
        for i in range(len(b)):
            x[i] = (b[i] - A[i, :i] @ x[:i] - A[i, i+1:] @ old[i+1:]) / A[i, i]
        error = np.linalg.norm(x - old, ord=np.inf)
        errors.append(error)
        if error < tol: break
    return x, errors

x_j, err_j = jacobi(A, b)
x_gs, err_gs = gauss_seidel(A, b)
x_exact = np.linalg.solve(A, b)

print("Jacobi concentrations:", x_j)
print("Gauss-Seidel concentrations:", x_gs)
print("Direct exact solution:", x_exact)

plt.semilogy(err_j, label="Jacobi")
plt.semilogy(err_gs, label="Gauss-Seidel")
plt.xlabel("Iteration")
plt.ylabel("Maximum change (Error)")
plt.title("Convergence of iterative diffusion solution")
plt.legend()
plt.grid(True)
plt.savefig("task08_graph.png")
print("Graph saved as task08_graph.png")

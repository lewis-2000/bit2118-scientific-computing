"""
BIT 2118: SCIENTIFIC COMPUTING
Task 6: Solution of Systems of Linear Equations

B. Identify the input values and the mathematical operation performed.
- Input values: Coefficient matrix A (labor and wood requirements per product) and vector b (total available resources).
- Mathematical operations: Linear system solver `np.linalg.solve(A, b)` to find the exact quantity of each product to manufacture. Matrix-vector multiplication `A @ solution` to verify the residual.

C. Change at least one input/parameter and explain how the result changes.
- Change: Increase available wood (the second element in vector b) from 80 to 100.
- Result: The production quantities will change. The solver will output a higher number of products that require more wood, maximizing the new resource limit.

D. Explain the meaning of the output in words and interpret the graph where necessary.
- Output meaning: The script determines exactly how many units of Product A and Product B should be manufactured to completely use up the available labor and materials, leaving zero waste. The residual validates the mathematical correctness.

E. Modify the program to solve a different but related real-world case.
- New Case: Factory production planning. A factory makes Chairs (Product A) and Tables (Product B), constrained by total available Labor Hours and Wood (kg).
"""
import numpy as np

# Product A (Chairs) needs 3 hours labor, 4 kg wood
# Product B (Tables) needs 5 hours labor, 10 kg wood
# Total available: 45 hours labor, 80 kg wood
A = np.array([
    [3.0, 5.0],  # Labor equation
    [4.0, 10.0]  # Wood equation
])
b = np.array([45.0, 80.0])

solution = np.linalg.solve(A, b)
residual = b - A @ solution

print(f"Produce Chairs (Product A): {solution[0]:.0f}")
print(f"Produce Tables (Product B): {solution[1]:.0f}")
print("Verification A @ solution:", A @ solution)
print("Residual norm:", np.linalg.norm(residual))

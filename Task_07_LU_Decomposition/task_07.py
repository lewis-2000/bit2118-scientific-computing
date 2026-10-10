"""
BIT 2118: SCIENTIFIC COMPUTING
Task 7: Gaussian Elimination and LU Decomposition

B. Identify the input values and the mathematical operation performed.
- Input values: A constant stiffness matrix `A` for a physical structure, and a list of load vectors `measurement_sets`.
- Mathematical operations: `lu_factor` factors the matrix into Lower and Upper triangular matrices. `lu_solve` solves the system for multiple right-hand sides efficiently.

C. Change at least one input/parameter and explain how the result changes.
- Change: Double the values of the first load vector.
- Result: Since it is a linear system, the resulting displacement solution for that vector will also exactly double.

D. Explain the meaning of the output in words and interpret the graph where necessary.
- Output meaning: The output represents the physical displacement of structural nodes under different load conditions. Factoring once and solving multiple times is shown to be accurate (low residual) and is computationally much faster for large systems.

E. Modify the program to solve a different but related real-world case.
- New Case: Structural engineering. Calculating the displacement of a bridge's truss nodes. The stiffness matrix of the bridge is constant, but the load vectors change rapidly as different vehicles drive across it.
"""
import numpy as np
from scipy.linalg import lu_factor, lu_solve

# Stiffness matrix K for a 3-node structure
K = np.array([
    [ 5.0, -2.0,  0.0],
    [-2.0,  6.0, -3.0],
    [ 0.0, -3.0,  4.0]
])

# Different load scenarios (Forces applied to nodes)
load_scenarios = [
    np.array([10.0, 0.0, 0.0]),   # Load on node 1
    np.array([0.0, 15.0, 0.0]),   # Load on node 2
    np.array([5.0, 5.0, 10.0])    # Distributed load
]

lu, piv = lu_factor(K)

for i, F in enumerate(load_scenarios, start=1):
    displacement = lu_solve((lu, piv), F)
    residual = F - K @ displacement
    print(f"Load Scenario {i}")
    print("Node Displacements:", displacement)
    print("Residual norm:", np.linalg.norm(residual), "\n")

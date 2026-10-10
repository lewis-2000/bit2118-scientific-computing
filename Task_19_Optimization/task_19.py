"""
BIT 2118: SCIENTIFIC COMPUTING
Task 19: Numerical Optimization

B. Identify the input values and the mathematical operation performed.
- Input values: Cost function, constraint requirements, and variable bounds.
- Mathematical operations: `scipy.optimize.minimize` (using SLSQP) finds the minimum value of a multivariate cost function while ensuring the output state doesn't violate inequalities (constraints).

C. Change at least one input/parameter and explain how the result changes.
- Change: Increase the minimum demand required from 2000 to 3000.
- Result: The optimizer will output higher production allocations for the factories, resulting in a significantly higher minimum operational cost.

D. Explain the meaning of the output in words and interpret the graph where necessary.
- Output meaning: The exact amount of production to allocate to Factory X vs Factory Y to fulfill a market demand of 2000 units while keeping manufacturing and logistics costs as low as mathematically possible.

E. Modify the program to solve a different but related real-world case.
- New Case: Supply Chain Logistics. Minimizing the production and shipping costs across two different factories with varying efficiencies, subject to meeting a minimum market demand constraint.
"""
import numpy as np
from scipy.optimize import minimize

# x = Production at Factory X
# y = Production at Factory Y
# Factory X cost per unit: $15
# Factory Y cost per unit: $22
def cost_function(vars):
    x, y = vars
    return 15*x + 22*y

# Factory X can output 1.0 unit per hour, Factory Y outputs 1.5 units per hour.
# Constraint: Total production output must be >= 2000 units
def demand_constraint(vars):
    x, y = vars
    return 1.0*x + 1.5*y - 2000

constraints = {"type": "ineq", "fun": demand_constraint}
# Factories can't produce negative amounts
bounds = [(0, None), (0, None)]

solution = minimize(
    cost_function,
    x0=[500, 500],
    method="SLSQP",
    bounds=bounds,
    constraints=constraints
)

print(f"Optimization Success: {solution.success}")
print(f"Allocate to Factory X: {solution.x[0]:.2f} hours")
print(f"Allocate to Factory Y: {solution.x[1]:.2f} hours")
print(f"Total Minimum Cost: ${solution.fun:,.2f}")

"""
BIT 2118: SCIENTIFIC COMPUTING
Task 10: Root Finding: Bisection and Fixed-Point Methods

B. Identify the input values and the mathematical operation performed.
- Input values: A continuous profit function `f(x)` and its fixed-point equivalent `g(x)`, along with a search bracket `[0, 50]` and initial guess `x=10`.
- Mathematical operations: `root_scalar(method="bisect")` halves the interval to isolate the root. The fixed-point iteration computes `x_{n+1} = g(x_n)` in a loop.

C. Change at least one input/parameter and explain how the result changes.
- Change: Increase the fixed cost from 5 to 15 in the profit equation.
- Result: The break-even production volume will increase. It requires selling more products to cover the higher fixed costs. Both bisection and fixed-point methods will converge on this new, higher root.

D. Explain the meaning of the output in words and interpret the graph where necessary.
- Output meaning: The output gives the exact production volume `x` required to make zero profit (break-even). The graph visually shows the profit curve crossing the x-axis (y=0) at the calculated root.

E. Modify the program to solve a different but related real-world case.
- New Case: Business economics. Finding the break-even production point where nonlinear manufacturing costs exactly match the non-linear revenue curve.
"""
import numpy as np
from scipy.optimize import root_scalar
import matplotlib.pyplot as plt

# Break-even model: Profit = Revenue - Cost
# Profit(x) = 20 * sqrt(x) - (5 + 2*x) = 0
def profit_function(x):
    return 20 * np.sqrt(x) - (5 + 2 * x)

# Bisection method (bracket where sign changes)
solution = root_scalar(
    profit_function,
    bracket=[0, 50],
    method="bisect",
    xtol=1e-10
)

# Fixed-point formulation:
# 2x = 20*sqrt(x) - 5  =>  x = 10*sqrt(x) - 2.5
def g(x):
    return 10 * np.sqrt(x) - 2.5

x_val = 10.0 # Initial guess
history = [x_val]
for _ in range(100):
    x_new = g(x_val)
    history.append(x_new)
    if abs(x_new - x_val) < 1e-10:
        break
    x_val = x_new

print(f"Bisection break-even volume: {solution.root:.4f} units")
print(f"Fixed-point break-even volume: {history[-1]:.4f} units")
print(f"Fixed-point iterations: {len(history)-1}")

# Plotting
volumes = np.linspace(0, 50, 300)
profits = profit_function(volumes)

plt.plot(volumes, profits, label="Profit Curve")
plt.axhline(0, color='red', linestyle='--', linewidth=1, label="Break-Even Line (y=0)")
plt.axvline(solution.root, color='green', linestyle=':', label=f"Root: {solution.root:.2f}")
plt.xlabel("Production Volume (x)")
plt.ylabel("Profit ($)")
plt.title("Manufacturing Break-Even Analysis")
plt.legend()
plt.grid(True)
plt.savefig("task10_graph.png")
print("Graph saved as task10_graph.png")

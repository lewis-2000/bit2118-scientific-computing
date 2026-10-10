"""
BIT 2118: SCIENTIFIC COMPUTING
Task 4: Floating-Point Arithmetic and Numerical Errors

B. Identify the input values and the mathematical operation performed.
- Input values: Float values representing prices, and coefficients of a quadratic equation (a, b, c).
- Mathematical operations:
  - Iterative addition (`0.1 + 0.1 ...`).
  - Standard quadratic formula operations: `-b + sqrt(b^2 - 4ac) / 2a`.
  - Stable quadratic formula operations: `-2c / (b + sqrt(b^2 - 4ac))` (using rationalization).

C. Change at least one input/parameter and explain how the result changes.
- Change: Change `b` in the quadratic formula from 10000.0 to 10.0.
- Result: When `b` is smaller, `b^2` is much closer in magnitude to `4ac`. This reduces the catastrophic cancellation (loss of significance) when computing `sqrt(b^2 - 4ac) - b`. Consequently, the direct and stable methods yield much closer or identical results.

D. Explain the meaning of the output in words and interpret the graph where necessary.
- Output meaning: The script shows that summing 0.1 ten times does not exactly equal 1.0 due to binary floating-point representation limits. It also shows two ways to calculate roots of a quadratic equation. The 'direct' way suffers from catastrophic cancellation when subtracting nearly equal numbers, leading to precision loss. The 'stable' formulation avoids this, yielding a highly accurate root.

E. Modify the program to solve a different but related real-world case.
- New Case: In physics simulations (e.g., calculating the trajectory of a projectile), finding the roots of a quadratic equation often determines boundary conditions or intersection points. Using an unstable formula can lead to physically impossible results or simulation crashes due to accumulated numerical errors.
"""

import numpy as np

# Floating-point representation issue (common in finance)
# E.g., summing 10 cents ten times
calculated_sum = sum([0.1] * 10)
expected_sum = 1.0

print(f"Sum of ten 0.1s: {calculated_sum}")
print(f"Exact comparison (calculated == 1.0): {calculated_sum == expected_sum}")
print(f"Tolerance-based comparison: {np.isclose(calculated_sum, expected_sum)}\n")


# Loss of significance in physics simulation (solving ax^2 + bx + c = 0)
# Suppose a and c are small, but b is large.
# Equation: 1e-4 * x^2 + 10000.0 * x + 1e-4 = 0

a = 1e-4
b = 10000.0
c = 1e-4

# We want the root close to zero.
# Standard quadratic formula: (-b + sqrt(b^2 - 4ac)) / 2a
# Because b is large and a, c are small, sqrt(b^2 - 4ac) is very close to b.
# Subtracting b from this value causes catastrophic cancellation.
direct_root = (-b + np.sqrt(b**2 - 4*a*c)) / (2*a)

# Numerically stable formulation (multiply numerator and denominator by conjugate)
# (-b + sqrt(b^2 - 4ac)) * (-b - sqrt(b^2 - 4ac)) / (2a * (-b - sqrt(b^2 - 4ac)))
# = (b^2 - (b^2 - 4ac)) / (2a * (-b - sqrt(b^2 - 4ac)))
# = 4ac / (2a * (-b - sqrt(b^2 - 4ac)))
# = 2c / (-b - sqrt(b^2 - 4ac))
stable_root = (2*c) / (-b - np.sqrt(b**2 - 4*a*c))

print(f"Coefficients: a={a}, b={b}, c={c}")
print(f"Root using direct formula (loss of precision): {direct_root}")
print(f"Root using stable formula (accurate):        {stable_root}")

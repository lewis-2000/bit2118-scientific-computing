"""
BIT 2118: SCIENTIFIC COMPUTING
Task 11: Root Finding: Newton-Raphson and Secant Methods

B. Identify the input values and the mathematical operation performed.
- Input values: Parameters for the Van der Waals gas equation (Pressure, Temperature, constants a, b, R).
- Mathematical operations: Newton-Raphson uses the function and its analytical derivative to iterate `v_{n+1} = v_n - f(v)/f'(v)`. Secant method uses two initial guesses to approximate the derivative.

C. Change at least one input/parameter and explain how the result changes.
- Change: Increase the Pressure (P) from 1 atm to 10 atm.
- Result: The gas will compress, so the root (specific volume 'v') will decrease significantly.

D. Explain the meaning of the output in words and interpret the graph where necessary.
- Output meaning: Finds the exact specific volume (m^3/kg) of a real gas under specific temperature and pressure conditions, correcting for the volume of gas molecules and intermolecular forces.

E. Modify the program to solve a different but related real-world case.
- New Case: Chemical Thermodynamics. Using the non-linear Van der Waals equation to find the specific volume of Carbon Dioxide (CO2) instead of financial IRR.
"""
from scipy.optimize import root_scalar

# Van der Waals parameters for CO2:
a = 3.59    # L^2 atm / mol^2
b = 0.0427  # L / mol
R = 0.08206 # L atm / (mol K)
T = 300.0   # Kelvin
P = 1.0     # atm

# (P + a/v^2)(v - b) = RT
# f(v) = (P + a/v^2)(v - b) - RT = 0
def vdw(v):
    return (P + a/v**2) * (v - b) - R * T

def d_vdw(v):
    return (P + a/v**2) + (v - b) * (-2 * a / v**3)

# Ideal gas law provides a good initial guess: v = RT/P
v_ideal = R * T / P

newton = root_scalar(vdw, fprime=d_vdw, x0=v_ideal, method="newton", xtol=1e-10)
secant = root_scalar(vdw, x0=v_ideal, x1=v_ideal*0.9, method="secant", xtol=1e-10)

print(f"Ideal Gas Volume (Guess): {v_ideal:.4f} L/mol")
print(f"Van der Waals Volume (Newton): {newton.root:.4f} L/mol")
print(f"Van der Waals Volume (Secant): {secant.root:.4f} L/mol")

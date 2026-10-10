"""
BIT 2118: SCIENTIFIC COMPUTING
Task 14: Curve Fitting and Approximation

B. Identify the input values and the mathematical operation performed.
- Input values: Time points and corresponding bacteria population counts.
- Mathematical operations: `scipy.optimize.curve_fit` uses non-linear least squares to find parameters `A` (initial pop) and `k` (growth rate) that minimize the squared residuals.

C. Change at least one input/parameter and explain how the result changes.
- Change: Increase the population count at the final time point drastically.
- Result: The algorithm will adjust the `k` parameter upward (higher growth rate) to try and minimize the new error, pulling the entire curve upwards.

D. Explain the meaning of the output in words and interpret the graph where necessary.
- Output meaning: The output gives the estimated initial population and the specific exponential growth rate constant. The graph plots the raw bacteria counts alongside the smooth mathematical model fit.

E. Modify the program to solve a different but related real-world case.
- New Case: Biology/Epidemiology. Fitting an exponential growth curve `P(t) = A * e^(kt)` to bacteria population measurements in a lab culture.
"""
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Time (hours) and Bacteria count (millions)
time_hrs = np.array([0, 1, 2, 3, 4, 5, 6], dtype=float)
bacteria_pop = np.array([2.1, 3.5, 6.2, 11.5, 19.8, 35.0, 60.5], dtype=float)

# Exponential model: P(t) = A * exp(k*t)
def exp_model(t, A, k):
    return A * np.exp(k * t)

# Initial guess: A=2.0, k=0.5
parameters, covariance = curve_fit(exp_model, time_hrs, bacteria_pop, p0=[2.0, 0.5])
A, k = parameters

predicted = exp_model(time_hrs, A, k)
rmse = np.sqrt(np.mean((bacteria_pop - predicted)**2))

print(f"Fitted model: Population = {A:.2f} * exp({k:.4f} * t)")
print(f"RMSE: {rmse:.2f} million")
print(f"Predicted population at 8 hours: {exp_model(8, A, k):.2f} million")

t_plot = np.linspace(0, 8, 100)
plt.scatter(time_hrs, bacteria_pop, label="Lab Measurements")
plt.plot(t_plot, exp_model(t_plot, A, k), color='orange', label="Fitted Exponential Curve")
plt.xlabel("Time (Hours)")
plt.ylabel("Bacteria Population (Millions)")
plt.title("Bacteria Exponential Growth Model")
plt.legend()
plt.grid(True)
plt.savefig("task14_graph.png")

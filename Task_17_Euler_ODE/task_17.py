"""
BIT 2118: SCIENTIFIC COMPUTING
Task 17: Ordinary Differential Equations – Euler Method

B. Identify the input values and the mathematical operation performed.
- Input values: Initial population, intrinsic growth rate (r), carrying capacity (K), and step size (h).
- Mathematical operations: Iterative Euler method: `P_{next} = P_{current} + h * (dP/dt)`.

C. Change at least one input/parameter and explain how the result changes.
- Change: Increase the step size `h` from 1.0 to 10.0.
- Result: The numerical approximation becomes unstable and inaccurate, potentially causing the population to wildly overshoot the carrying capacity or oscillate.

D. Explain the meaning of the output in words and interpret the graph where necessary.
- Output meaning: Simulates population growth over time. The graph shows an S-curve (logistic growth), where the population grows exponentially at first but slows and flattens out as it reaches the carrying capacity limit of the environment.

E. Modify the program to solve a different but related real-world case.
- New Case: Ecology. Modeling the logistic population growth of a species restricted by environmental carrying capacity, instead of Newton's law of cooling.
"""
import numpy as np
import matplotlib.pyplot as plt

# Logistic Growth ODE: dP/dt = r * P * (1 - P/K)
P_initial = 10.0
r = 0.2     # Growth rate
K = 1000.0  # Carrying capacity
h = 1.0     # Time step (months)
end_time = 50.0

def population_growth(P):
    return r * P * (1 - P / K)

time = np.arange(0, end_time + h, h)
population = np.zeros_like(time)
population[0] = P_initial

for i in range(len(time) - 1):
    population[i + 1] = population[i] + h * population_growth(population[i])

# Analytical exact solution for logistic growth
exact_pop = K / (1 + ((K - P_initial)/P_initial) * np.exp(-r * time))

print(f"Euler Population at month 50: {population[-1]:.1f}")
print(f"Exact Population at month 50: {exact_pop[-1]:.1f}")

plt.plot(time, population, 'o-', markersize=4, label="Euler Method")
plt.plot(time, exact_pop, label="Exact Solution")
plt.axhline(K, color='r', linestyle='--', label="Carrying Capacity (K)")
plt.xlabel("Time (Months)")
plt.ylabel("Population Count")
plt.title("Logistic Population Growth")
plt.legend()
plt.grid(True)
plt.savefig("task17_graph.png")

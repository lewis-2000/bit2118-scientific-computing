"""
BIT 2118: SCIENTIFIC COMPUTING
Task 18: Numerical Solution of ODEs Using SciPy

B. Identify the input values and the mathematical operation performed.
- Input values: Infection rate (beta), recovery rate (gamma), and initial populations (Susceptible, Infected, Recovered).
- Mathematical operations: `scipy.integrate.solve_ivp` numerically integrates a system of 3 coupled non-linear ODEs over a time domain.

C. Change at least one input/parameter and explain how the result changes.
- Change: Increase the infection rate (`beta`) from 0.3 to 0.6.
- Result: The disease spreads much faster. The peak of the infected curve will occur sooner in time and will reach a much higher maximum number of concurrent infections.

D. Explain the meaning of the output in words and interpret the graph where necessary.
- Output meaning: Models an epidemic outbreak over time. The graph shows the classic epidemiological curves: Susceptible drops as people get sick, Infected spikes then falls ("flattening the curve"), and Recovered climbs steadily.

E. Modify the program to solve a different but related real-world case.
- New Case: Epidemiology. Using SciPy ODE solvers to model the SIR (Susceptible, Infected, Recovered) dynamics of a viral disease outbreak.
"""
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# SIR Epidemic Model
N = 1000       # Total population
I0 = 1         # Initial infected
R0 = 0         # Initial recovered
S0 = N - I0 - R0 # Initial susceptible
beta = 0.3     # Infection rate
gamma = 0.1    # Recovery rate

# dS/dt = -beta*S*I/N
# dI/dt = beta*S*I/N - gamma*I
# dR/dt = gamma*I
def sir_model(t, y):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return [dSdt, dIdt, dRdt]

t_eval = np.linspace(0, 100, 200)
sol = solve_ivp(sir_model, (0, 100), [S0, I0, R0], t_eval=t_eval)

print(f"Solver Success: {sol.success}")
print(f"Max Infected concurrently: {np.max(sol.y[1]):.0f} people")
print(f"Final Recovered (Total infected): {sol.y[2][-1]:.0f} people")

plt.plot(sol.t, sol.y[0], label="Susceptible")
plt.plot(sol.t, sol.y[1], label="Infected")
plt.plot(sol.t, sol.y[2], label="Recovered")
plt.xlabel("Time (Days)")
plt.ylabel("Population")
plt.title("SIR Epidemic Model")
plt.legend()
plt.grid(True)
plt.savefig("task18_graph.png")

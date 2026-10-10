"""
BIT 2118: SCIENTIFIC COMPUTING
Task 20: Random Numbers and Monte Carlo Methods

B. Identify the input values and the mathematical operation performed.
- Input values: Mean durations and standard deviations for 3 sequential project tasks.
- Mathematical operations: `np.random.normal` generates 100,000 random samples. Vector addition sums the durations. A boolean comparison `total_time <= deadline` calculates the empirical probability.

C. Change at least one input/parameter and explain how the result changes.
- Change: Increase the standard deviation (uncertainty) of Task B from 2.0 to 10.0 days.
- Result: The spread of the final project times becomes much wider, significantly decreasing the probability that the project finishes under the strict 55-day deadline.

D. Explain the meaning of the output in words and interpret the graph where necessary.
- Output meaning: The estimated probability that a multi-stage project will finish before a deadline. The graph shows that the Monte Carlo estimate stabilizes/converges to the true theoretical probability as the number of simulations increases.

E. Modify the program to solve a different but related real-world case.
- New Case: Project Management (PERT Analysis). Using a Monte Carlo simulation to estimate the probability that a project with 3 sequential, highly uncertain tasks will be completed by a specific deadline.
"""
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)

# Sequential tasks in a project (Mean days, StdDev days)
task_A_mean, task_A_std = 15.0, 3.0
task_B_mean, task_B_std = 20.0, 2.0
task_C_mean, task_C_std = 12.0, 4.0

deadline = 50.0  # target days
N_sims = 100_000

# Simulate 100,000 scenarios for each task
sim_A = rng.normal(task_A_mean, task_A_std, N_sims)
sim_B = rng.normal(task_B_mean, task_B_std, N_sims)
sim_C = rng.normal(task_C_mean, task_C_std, N_sims)

total_project_time = sim_A + sim_B + sim_C

# Count how many scenarios finished on or before the deadline
successes = total_project_time <= deadline
success_probability = successes.mean()

print(f"Estimated probability of meeting {deadline}-day deadline: {success_probability:.2%}")

# Running probability to show convergence
running_prob = np.cumsum(successes) / np.arange(1, N_sims + 1)
indices = np.unique(np.logspace(1, np.log10(N_sims), 200).astype(int)) - 1

plt.semilogx(indices + 1, running_prob[indices])
plt.xlabel("Number of Simulations (Log Scale)")
plt.ylabel("Estimated Probability")
plt.title("Monte Carlo Convergence: Project Deadline")
plt.grid(True)
plt.savefig("task20_graph.png")

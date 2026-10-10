"""
BIT 2118: SCIENTIFIC COMPUTING
Task 9: Eigenvalues and Eigenvectors

B. Identify the input values and the mathematical operation performed.
- Input values: A 3x3 Leslie matrix containing birth rates (top row) and survival probabilities (sub-diagonal) of an animal population.
- Mathematical operations: `np.linalg.eig(A)` computes the eigenvalues and eigenvectors.

C. Change at least one input/parameter and explain how the result changes.
- Change: Increase the birth rate of the adult stage (top right element) from 1.2 to 3.0.
- Result: The dominant eigenvalue will increase significantly, indicating a faster population growth rate. The stable age distribution (eigenvector) will also shift slightly.

D. Explain the meaning of the output in words and interpret the graph where necessary.
- Output meaning: The dominant eigenvalue represents the long-term population growth rate (if > 1, the population grows). The corresponding normalized eigenvector gives the stable age distribution—the percentage of the population in each age class once it reaches equilibrium.

E. Modify the program to solve a different but related real-world case.
- New Case: Ecological modeling. Using a Leslie matrix to predict the long-term growth rate and stable age structure (Juveniles, Young Adults, Older Adults) of an endangered species to guide conservation efforts.
"""
import numpy as np

# Leslie Matrix for 3 age classes (Juveniles, Young Adults, Older Adults)
# Row 0: Fecundity (birth rates)
# Sub-diagonal: Survival rates to next age class
Leslie = np.array([
    [0.0, 1.5, 1.2],
    [0.4, 0.0, 0.0],
    [0.0, 0.6, 0.0]
])

eigenvalues, eigenvectors = np.linalg.eig(Leslie)

# Find the dominant eigenvalue (largest real part)
index = np.argmax(np.real(eigenvalues))
dominant_value = np.real(eigenvalues[index])
dominant_vector = np.abs(np.real(eigenvectors[:, index]))

# Normalize to get demographic percentages
age_distribution = dominant_vector / dominant_vector.sum()
age_classes = ["Juveniles", "Young Adults", "Older Adults"]

print(f"Dominant Eigenvalue (Growth rate): {dominant_value:.4f}")
print("Stable Age Distribution:")
for age_class, percent in zip(age_classes, age_distribution):
    print(f"{age_class}: {percent:.2%}")

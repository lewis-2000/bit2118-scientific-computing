"""
BIT 2118: SCIENTIFIC COMPUTING
Task 2: NumPy Arrays and Numerical Computation

B. Identify the input values and the mathematical operation performed.
- Input values: An array of 24 hourly humidity readings (percentages).
- Mathematical operations:
  - np.mean(): Calculates the average humidity.
  - np.min(): Finds the lowest humidity.
  - np.max(): Finds the highest humidity.
  - scalar division (humidity / 100): Normalizes the values to a range [0, 1].

C. Change at least one input/parameter and explain how the result changes.
- Change: We can change one of the humidity readings to a very high value, e.g., changing 50.5 to 99.0.
- Result: The mean will increase, the maximum will be 99.0, and the normalized values will reflect this higher upper bound if we divide by max (but here we divide by 100 to normalize to a fraction). If we used max normalization, all other normalized values would decrease.

D. Explain the meaning of the output in words and interpret the graph where necessary.
- Output meaning: The script prints the average humidity for the day, the lowest and highest humidity recorded, and the first few normalized humidity values. This allows the greenhouse operator to understand the environment's daily profile and ensures it stays within optimal bounds for plant growth.

E. Modify the program to solve a different but related real-world case.
- New Case: Monitoring greenhouse humidity levels (instead of temperature) and normalizing them to a 0-1 scale to feed into a machine learning model that controls the irrigation and ventilation systems.
"""

import numpy as np

# 24 hourly humidity readings in percentage (%)
humidity_levels = np.array([
    60.5, 61.0, 62.2, 65.5, 68.9, 70.0,
    72.5, 70.8, 68.6, 65.1, 60.3, 55.0,
    50.4, 48.1, 45.5, 47.6, 50.2, 53.8,
    56.4, 58.1, 60.0, 61.2, 60.6, 60.0
])

mean_humidity = np.mean(humidity_levels)
min_humidity = np.min(humidity_levels)
max_humidity = np.max(humidity_levels)

# Vectorized normalization to [0, 1] range for Machine Learning input
normalized_humidity = humidity_levels / 100.0

print(f"Daily mean humidity: {mean_humidity:.2f}%")
print(f"Minimum humidity: {min_humidity:.2f}%")
print(f"Maximum humidity: {max_humidity:.2f}%")
print("First six normalized readings:", normalized_humidity[:6])

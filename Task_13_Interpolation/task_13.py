"""
BIT 2118: SCIENTIFIC COMPUTING
Task 13: Interpolation

B. Identify the input values and the mathematical operation performed.
- Input values: Sparse arrays of time and an object's X-position.
- Mathematical operations: `interp1d` and `CubicSpline` calculate intermediate points. Splines construct piecewise cubic polynomials ensuring smooth first and second derivatives.

C. Change at least one input/parameter and explain how the result changes.
- Change: Request interpolation at `t = 2.5` instead of `t = 1.5`.
- Result: The functions will output the mathematically interpolated position corresponding specifically to that new timestamp based on surrounding data points.

D. Explain the meaning of the output in words and interpret the graph where necessary.
- Output meaning: Fills in the missing frames of an animation/trajectory. The graph shows that linear interpolation creates jerky, straight-line movements between keyframes, while cubic splines create smooth, natural-looking curves.

E. Modify the program to solve a different but related real-world case.
- New Case: Animation and Robotics. Interpolating an object's trajectory between sparse "keyframes" to ensure smooth motion at a high frame rate.
"""
import numpy as np
from scipy.interpolate import interp1d, CubicSpline
import matplotlib.pyplot as plt

# Sparse Keyframes: Time (sec) and X-position
time_keyframes = np.array([0, 1, 2, 3, 4, 5], dtype=float)
x_position = np.array([0.0, 1.5, 2.0, 5.0, 5.5, 6.0])

linear = interp1d(time_keyframes, x_position, kind="linear")
cubic = CubicSpline(time_keyframes, x_position)

# High frame-rate interpolation (e.g., 60fps)
dense_time = np.linspace(0, 5, 300)
linear_path = linear(dense_time)
cubic_path = cubic(dense_time)

target_time = 1.5
print(f"Linear estimate at t={target_time}: {float(linear(target_time)):.2f}m")
print(f"Cubic estimate at t={target_time}: {float(cubic(target_time)):.2f}m")

plt.scatter(time_keyframes, x_position, color='red', label="Keyframes", zorder=5)
plt.plot(dense_time, linear_path, '--', label="Linear (Jerky)")
plt.plot(dense_time, cubic_path, label="Cubic Spline (Smooth)")
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title("Trajectory Keyframe Interpolation")
plt.legend()
plt.grid(True)
plt.savefig("task13_graph.png")

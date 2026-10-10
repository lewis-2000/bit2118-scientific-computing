"""
BIT 2118: SCIENTIFIC COMPUTING
Task 12: Polynomial and Nonlinear Equation Solving

B. Identify the input values and the mathematical operation performed.
- Input values: Target (x,y) coordinates and lengths of two robotic arm segments (L1, L2).
- Mathematical operations: `scipy.optimize.root` solves a system of two non-linear trigonometric equations to find the required joint angles.

C. Change at least one input/parameter and explain how the result changes.
- Change: Move the target x-coordinate further away (e.g., from x=2 to x=3).
- Result: The joint angles will adjust (straighten out) to reach the new target. If the target is beyond L1+L2, the solver will fail to converge to a zero residual.

D. Explain the meaning of the output in words and interpret the graph where necessary.
- Output meaning: The output gives the specific angles (in radians and degrees) that the motors of a robotic arm must rotate to so the hand reaches a specific point in space.

E. Modify the program to solve a different but related real-world case.
- New Case: Robotics Kinematics. Inverse kinematics for a 2-DOF planar robotic arm, translating desired hand positions into joint rotations.
"""
import numpy as np
from scipy.optimize import root

# 2-DOF Robotic Arm Inverse Kinematics
L1, L2 = 2.0, 1.5
target_x, target_y = 1.0, 2.0

# Equations:
# L1*cos(theta1) + L2*cos(theta1 + theta2) - target_x = 0
# L1*sin(theta1) + L2*sin(theta1 + theta2) - target_y = 0
def kinematics(angles):
    t1, t2 = angles
    return [
        L1 * np.cos(t1) + L2 * np.cos(t1 + t2) - target_x,
        L1 * np.sin(t1) + L2 * np.sin(t1 + t2) - target_y
    ]

# Try different initial guesses ("elbow up" vs "elbow down" configurations)
for guess in ([np.pi/4, np.pi/4], [np.pi, -np.pi/4]):
    sol = root(kinematics, guess)
    if sol.success:
        t1, t2 = sol.x
        print(f"Initial guess: {np.degrees(guess)}")
        print(f"Solution angles (deg): Theta1={np.degrees(t1):.1f}, Theta2={np.degrees(t2):.1f}")
        print(f"Residuals: {kinematics(sol.x)}\n")

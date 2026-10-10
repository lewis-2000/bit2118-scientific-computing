"""
BIT 2118: SCIENTIFIC COMPUTING
Task 16: Numerical Integration

B. Identify the input values and the mathematical operation performed.
- Input values: Time intervals (hours) and water flow rates (cubic meters per second).
- Mathematical operations: Uses the Trapezoidal rule (linear segments) and Simpson's rule (parabolic segments) to calculate the area under the flow-rate curve. Note: conversion factor applied for seconds to hours.

C. Change at least one input/parameter and explain how the result changes.
- Change: Increase the flow rate at the 6-hour mark from 50 to 100 m^3/s.
- Result: The total integrated volume of water will increase by the area of the curve associated with that peak.

D. Explain the meaning of the output in words and interpret the graph where necessary.
- Output meaning: The script computes the total cumulative volume of water that passed through a dam over 12 hours. Simpson's rule usually provides a more accurate estimate for smooth flows.

E. Modify the program to solve a different but related real-world case.
- New Case: Hydrology/Civil Engineering. Integrating water flow rates (m^3/s) recorded at a dam over a day to calculate the total total volume of water discharged (m^3).
"""
import numpy as np
from scipy.integrate import simpson

# Time every 2 hours (0, 2, 4...)
time_hours = np.array([0, 2, 4, 6, 8, 10, 12], dtype=float)
# Flow rate in cubic meters per second (m^3/s)
flow_rate_m3_s = np.array([20.0, 25.0, 35.0, 50.0, 45.0, 30.0, 20.0])

# To integrate over hours but flow is per second, multiply time by 3600
time_seconds = time_hours * 3600

vol_trapezoid = np.trapezoid(flow_rate_m3_s, time_seconds)
vol_simpson = simpson(flow_rate_m3_s, x=time_seconds)

print(f"Total Volume discharged (Trapezoidal): {vol_trapezoid:,.0f} m^3")
print(f"Total Volume discharged (Simpson's):   {vol_simpson:,.0f} m^3")
print(f"Difference between methods: {abs(vol_simpson - vol_trapezoid):,.0f} m^3")

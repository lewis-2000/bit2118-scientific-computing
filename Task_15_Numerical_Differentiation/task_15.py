"""
BIT 2118: SCIENTIFIC COMPUTING
Task 15: Numerical Differentiation

B. Identify the input values and the mathematical operation performed.
- Input values: Time points (days) and stock prices.
- Mathematical operations: Forward, central, and backward finite differences `[f(x+h) - f(x-h)] / 2h` to approximate the derivative (rate of change or momentum).

C. Change at least one input/parameter and explain how the result changes.
- Change: Increase a single stock price in the middle of the array.
- Result: The rate of change before that point will sharply increase (positive momentum), and the rate of change after it will sharply decrease (negative momentum).

D. Explain the meaning of the output in words and interpret the graph where necessary.
- Output meaning: Evaluates the daily momentum (change in price per day). A positive number means the stock is trending up, while negative means a downtrend. The graph overlays the stock price and its momentum.

E. Modify the program to solve a different but related real-world case.
- New Case: Finance. Estimating the daily rate of change (momentum) of a stock price to build algorithmic trading signals.
"""
import numpy as np
import matplotlib.pyplot as plt

# Stock data: Day and closing price
days = np.array([0, 1, 2, 3, 4, 5, 6, 7], dtype=float)
price = np.array([100.0, 102.5, 101.0, 105.0, 110.0, 108.0, 115.0, 120.0])
momentum = np.zeros_like(price)

# Forward difference at the start
momentum[0] = (price[1] - price[0]) / (days[1] - days[0])

# Central differences for interior points
for i in range(1, len(days) - 1):
    momentum[i] = (price[i + 1] - price[i - 1]) / (days[i + 1] - days[i - 1])

# Backward difference at the end
momentum[-1] = (price[-1] - price[-2]) / (days[-1] - days[-2])

for d, p, m in zip(days, price, momentum):
    print(f"Day {d:.0f}: Price=${p:.2f}, Momentum=${m:.2f}/day")

fig, ax1 = plt.subplots()
ax1.plot(days, price, 'b-o', label="Stock Price")
ax1.set_xlabel("Day")
ax1.set_ylabel("Price ($)", color='b')
ax1.tick_params(axis='y', labelcolor='b')

ax2 = ax1.twinx()
ax2.bar(days, momentum, alpha=0.3, color='g', label="Momentum")
ax2.set_ylabel("Momentum ($/day)", color='g')
ax2.tick_params(axis='y', labelcolor='g')
plt.title("Stock Price and Daily Momentum")
plt.savefig("task15_graph.png")

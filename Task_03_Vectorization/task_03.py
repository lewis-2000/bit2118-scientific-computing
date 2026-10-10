"""
BIT 2118: SCIENTIFIC COMPUTING
Task 3: Mathematical Functions and Vectorization

B. Identify the input values and the mathematical operation performed.
- Input values: An array of 1,000,000 transaction amounts (in USD).
- Mathematical operations:
  - Scalar multiplication (amounts * 0.15) to calculate a 15% tax.
  - Vector addition (amounts + tax) to calculate total amounts.

C. Change at least one input/parameter and explain how the result changes.
- Change: Change the number of transactions from 1,000,000 to 5,000,000.
- Result: Both the loop and vectorized execution times will increase. However, the loop execution time will increase dramatically compared to the vectorized version, leading to an even higher speed-up ratio for vectorization. This demonstrates the scalability of NumPy for big data.

D. Explain the meaning of the output in words and interpret the graph where necessary.
- Output meaning: The script prints the first few total transaction amounts including tax, the time it took to calculate this using a standard Python loop, the time using NumPy vectorization, and the speed-up ratio. This highlights how vectorization is significantly more efficient than standard loops for processing large datasets.

E. Modify the program to solve a different but related real-world case.
- New Case: An e-commerce platform processing a massive volume of transactions. The system needs to calculate the tax and total cost for millions of transactions quickly to generate daily financial reports without delaying other services.
"""

import numpy as np
import timeit

# Simulated e-commerce transaction amounts in USD
rng = np.random.default_rng(42)
transactions_usd = rng.uniform(10.0, 500.0, 1_000_000)

TAX_RATE = 0.15

def loop_version():
    totals = []
    for amount in transactions_usd:
        tax = amount * TAX_RATE
        totals.append(amount + tax)
    return totals

def vectorized_version():
    tax = transactions_usd * TAX_RATE
    return transactions_usd + tax

loop_time = timeit.timeit(loop_version, number=1)
vector_time = timeit.timeit(vectorized_version, number=3) / 3

result = vectorized_version()

print("First five total amounts (including tax):", result[:5])
print(f"Loop time: {loop_time:.4f} s")
print(f"Vectorized time: {vector_time:.4f} s")
print(f"Approximate speed-up: {loop_time/vector_time:.1f}x")

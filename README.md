# BIT 2118: Scientific Computing Group Work

This repository contains the implementation of the tasks for the BIT 2118 Scientific Computing assignment. 
The code solves mathematical problems using Python's scientific libraries.

## Environment Setup and Dependencies (.venv)

To isolate the project dependencies and avoid conflicts with the system Python, a Python virtual environment (`.venv`) is used. The environment has been populated with the required libraries for numerical computing, data vectorization, and data visualization.

### Installed Libraries
The following core libraries (and their respective sub-dependencies) are installed in the `.venv` directory:
- **NumPy** (`numpy`): Used for high-performance vectorized mathematical operations and multidimensional array logic.
- **SciPy** (`scipy`): Used for scientific algorithms (required for subsequent tasks like numerical integration, ODEs, and optimization).
- **Matplotlib** (`matplotlib`): Used for data visualization and graphing (required for subsequent tasks).

You can see the exact versions of all installed packages (including dependencies like `contourpy`, `cycler`, `kiwisolver`, `pillow`, `pyparsing`, `python-dateutil`) in the `Requirements.txt` file.

### How to use the Virtual Environment
To run these scripts, you should activate the environment first:
```bash
# Activate the environment
source .venv/bin/activate

# (Optional) If setting up on a new machine, install dependencies with:
pip install -r Requirements.txt
```

---

## Tasks Documentation

### Task 2: NumPy Arrays and Numerical Computation
**File:** `Task_02_Numpy/task_02.py`
* **B. Input values and mathematical operation performed:**
  - **Inputs:** An array of 24 hourly humidity readings (percentages).
  - **Operations:** Calculations of average (`np.mean`), lowest (`np.min`), and highest (`np.max`) humidity. Normalization of the array to a fractional scale using scalar division (`humidity / 100.0`).
* **C. Change input/parameter and result:**
  - **Change:** Replacing a standard humidity reading with an extremely high one (e.g., 99.0%).
  - **Result:** The mean increases, the max value changes to 99.0%, and the normalized array reflects this new data point as `0.99`.
* **D. Meaning of the output:**
  - **Output:** The script outputs the mean, minimum, and maximum humidity of the day, along with the normalized array.
  - **Interpretation:** This provides a statistical profile of the daily environment to ensure it stays within optimal bounds.
* **E. Real-world case modification:**
  - **Case:** Modified from a generic weather station tracking temperature to a greenhouse system monitoring humidity levels. The data is normalized to a 0-1 scale, a common requirement for feeding features into Machine Learning models that control automated irrigation and ventilation.

### Task 3: Mathematical Functions and Vectorization
**File:** `Task_03_Vectorization/task_03.py`
* **B. Input values and mathematical operation performed:**
  - **Inputs:** An array of 1,000,000 simulated transaction amounts in USD.
  - **Operations:** Scalar multiplication (`amounts * 0.15`) to calculate a 15% tax, followed by vector addition (`amounts + tax`) to obtain the total amount.
* **C. Change input/parameter and result:**
  - **Change:** Increasing the dataset size from 1,000,000 to 5,000,000 transactions.
  - **Result:** Execution times for both the traditional Python loop and the NumPy vectorized method increase. However, the loop's execution time scales poorly and takes significantly longer, which widens the speed-up ratio and proves NumPy's efficiency.
* **D. Meaning of the output:**
  - **Output:** The script displays the first five calculated totals and compares the execution times of a standard `for` loop versus NumPy vectorization.
  - **Interpretation:** The drastic speed-up demonstrates that vectorized operations are highly optimized (written in C) and should be used instead of Python loops when processing large numerical datasets.
* **E. Real-world case modification:**
  - **Case:** Changed from network latency conversion to an e-commerce platform that must quickly process millions of financial transactions (calculating tax and totals) for a daily financial report.

### Task 4: Floating-Point Arithmetic and Numerical Errors
**File:** `Task_04_Numerical_Errors/task_04.py`
* **B. Input values and mathematical operation performed:**
  - **Inputs:** Decimal values representing prices (`0.1`), and coefficients for a quadratic equation (`a=1e-4`, `b=10000.0`, `c=1e-4`).
  - **Operations:** Iterative floating-point addition, and finding roots using two quadratic formula variations: the standard formula `(-b + sqrt(b^2 - 4ac)) / 2a` and the algebraically stabilized formula `2c / (-b - sqrt(b^2 - 4ac))`.
* **C. Change input/parameter and result:**
  - **Change:** Decreasing the `b` coefficient in the quadratic equation from `10000.0` to `10.0`.
  - **Result:** `b^2` becomes much closer in magnitude to `4ac`, meaning that evaluating `sqrt(b^2 - 4ac)` doesn't yield a value near `b`. This prevents catastrophic cancellation during subtraction, and both the direct and stable formulas output identical (or nearly identical) correct answers.
* **D. Meaning of the output:**
  - **Output:** Shows that `10 * 0.1` isn't stored internally as exactly `1.0`. Also compares the root of the quadratic equation generated by a standard formula versus a stable formula.
  - **Interpretation:** The direct formula suffers from precision loss (loss of significance) due to subtracting two nearly identical large numbers, yielding a wildly inaccurate root. The stable formula circumvents this and yields the exact accurate root.
* **E. Real-world case modification:**
  - **Case:** Applied to physics simulations (like determining projectile boundary conditions), where a loss of significance in intermediate mathematical steps can cascade, resulting in physically impossible trajectories or a complete simulation crash.
### Task 5: Matrix Algebra and Matrix Operations
**File:** `Task_05_Matrix_Algebra/task_05.py`
* **B. Input values and mathematical operation performed:**
  - **Inputs:** A 2D array of coordinates representing an image bounding box, a scaling matrix, and a shear matrix.
  - **Operations:** Matrix multiplication (`@`) to apply transformations, and `np.linalg.det` to find the determinant.
* **C. Change input/parameter and result:**
  - **Change:** Increase the shear factor from 0.5 to 1.5.
  - **Result:** The bounding box skews significantly more along the x-axis. The determinant (area scale factor) remains the same if it's a pure shear, but the shape distorts.
* **D. Meaning of the output:**
  - **Output:** Original coordinates, the combined transformation matrix, the new coordinates, and the determinant.
  - **Interpretation:** Shows how 2D vectors are manipulated in space, with the determinant providing the scaling factor of the object's area.
* **E. Real-world case modification:**
  - **Case:** Computer vision. Transforming a 2D bounding box detected around an object to normalize its perspective (scaling and shearing) before classification.

### Task 6: Solution of Systems of Linear Equations
**File:** `Task_06_Linear_Systems/task_06.py`
* **B. Input values and mathematical operation performed:**
  - **Inputs:** Coefficient matrix `A` (labor/wood per product) and vector `b` (total resources).
  - **Operations:** Linear system solver `np.linalg.solve(A, b)` and verification using matrix multiplication (`A @ solution`).
* **C. Change input/parameter and result:**
  - **Change:** Increase available wood (vector `b`).
  - **Result:** The exact production quantities will change to maximize the new resource constraints.
* **D. Meaning of the output:**
  - **Output:** The exact number of each product to manufacture and the residual.
  - **Interpretation:** Determines the optimal production mix to consume all available resources with zero waste.
* **E. Real-world case modification:**
  - **Case:** Factory production planning, replacing the abstract server resource model.

### Task 7: Gaussian Elimination and LU Decomposition
**File:** `Task_07_LU_Decomposition/task_07.py`
* **B. Input values and mathematical operation performed:**
  - **Inputs:** Stiffness matrix `K` and load vectors `F`.
  - **Operations:** `lu_factor` to factor the matrix into LU, and `lu_solve` to efficiently solve for displacements.
* **C. Change input/parameter and result:**
  - **Change:** Double the values of a load vector.
  - **Result:** Since the system is linear, the displacement solution exactly doubles.
* **D. Meaning of the output:**
  - **Output:** Node displacements and the residual norm.
  - **Interpretation:** The physical displacement of structural nodes under different loads. Factoring once saves computation when analyzing multiple loads.
* **E. Real-world case modification:**
  - **Case:** Structural engineering model of a bridge under various traffic loads.

### Task 8: Iterative Methods for Linear Systems
**File:** `Task_08_Iterative_Methods/task_08.py`
* **B. Input values and mathematical operation performed:**
  - **Inputs:** Tridiagonal matrix `A` (diffusion) and boundary conditions `b`.
  - **Operations:** Iterative matrix updates using Jacobi and Gauss-Seidel formulas until the error is below a tolerance.
* **C. Change input/parameter and result:**
  - **Change:** Increase tolerance from `1e-8` to `1e-3`.
  - **Result:** Algorithms stop in fewer iterations. The result is computed faster but has higher error compared to the exact solution.
* **D. Meaning of the output:**
  - **Output:** Steady-state concentrations and a convergence graph (saved as PNG).
  - **Interpretation:** Gauss-Seidel converges to the solution faster (steeper slope) than Jacobi.
* **E. Real-world case modification:**
  - **Case:** 1D chemical concentration diffusion in a pipe connecting two reservoirs, modified from the heat equation.

### Task 9: Eigenvalues and Eigenvectors
**File:** `Task_09_Eigenvalues/task_09.py`
* **B. Input values and mathematical operation performed:**
  - **Inputs:** A 3x3 Leslie matrix of birth and survival rates.
  - **Operations:** `np.linalg.eig(A)` to compute eigenvalues and eigenvectors.
* **C. Change input/parameter and result:**
  - **Change:** Increase an adult birth rate.
  - **Result:** The dominant eigenvalue (population growth rate) increases, and the age distribution shifts.
* **D. Meaning of the output:**
  - **Output:** The dominant eigenvalue and corresponding normalized eigenvector.
  - **Interpretation:** The eigenvalue acts as the long-term growth rate multiplier (λ). The eigenvector represents the stable percentage distribution of age classes in the population.
* **E. Real-world case modification:**
  - **Case:** Ecological modeling of animal populations using Leslie matrices instead of network centrality.

### Task 10: Root Finding: Bisection and Fixed-Point Methods
**File:** `Task_10_Root_Finding/task_10.py`
* **B. Input values and mathematical operation performed:**
  - **Inputs:** Continuous profit function `f(x)`, fixed-point equivalent `g(x)`, a search bracket, and an initial guess.
  - **Operations:** `root_scalar` (bisection) halves the bracket. Fixed-point iteration recursively computes `x_{n+1} = g(x_n)`.
* **C. Change input/parameter and result:**
  - **Change:** Increase the fixed cost from 5 to 15.
  - **Result:** The break-even point shifts higher since more units must be produced to cover costs.
* **D. Meaning of the output:**
  - **Output:** The exact production volume to break even, and a plot (saved as PNG).
  - **Interpretation:** The visual intersection where profit goes from negative to positive.
* **E. Real-world case modification:**
  - **Case:** Business economics. Finding the manufacturing break-even point rather than thermal equilibrium.

### Task 11: Root Finding: Newton-Raphson and Secant Methods
**File:** `Task_11_Newton_Secant/task_11.py`
* **B. Input values and mathematical operation performed:** Inputs are parameters for the Van der Waals gas equation. Newton-Raphson uses `f(v)` and `f'(v)` to iterate; Secant uses function evaluations from two points.
* **C. Change input/parameter and result:** Increasing Pressure (P) compresses the gas, resulting in a lower specific volume (root).
* **D. Meaning of the output:** The exact specific volume of a real gas under given conditions, factoring in intermolecular forces.
* **E. Real-world case modification:** Chemical Thermodynamics. Finding specific volume using the Van der Waals equation instead of financial Net Present Value.

### Task 12: Polynomial and Nonlinear Equation Solving
**File:** `Task_12_Nonlinear_Systems/task_12.py`
* **B. Input values and mathematical operation performed:** Target (x,y) and robot arm lengths. `scipy.optimize.root` solves the non-linear trigonometric system.
* **C. Change input/parameter and result:** Moving the target coordinates further forces the solver to find straightened joint angles.
* **D. Meaning of the output:** The exact motor angles required for a robotic arm hand to reach a specific 2D coordinate.
* **E. Real-world case modification:** Robotics Kinematics. Inverse kinematics for a 2-DOF robotic arm instead of circle-parabola intersections.

### Task 13: Interpolation
**File:** `Task_13_Interpolation/task_13.py`
* **B. Input values and mathematical operation performed:** Sparse time and position data points. `interp1d` (linear) and `CubicSpline` calculate the intermediate data values.
* **C. Change input/parameter and result:** Changing the target time evaluates the interpolant at a different location on the generated curve.
* **D. Meaning of the output:** Mathematical approximation of missing frames. Linear yields straight paths, cubic spline creates natural curves.
* **E. Real-world case modification:** Animation/Robotics. Smoothing object trajectories between keyframes instead of temperature interpolation.

### Task 14: Curve Fitting and Approximation
**File:** `Task_14_Curve_Fitting/task_14.py`
* **B. Input values and mathematical operation performed:** Time and bacteria population. `curve_fit` minimizes squared residuals to find exponential parameters `A` and `k`.
* **C. Change input/parameter and result:** A higher population spike at the end increases parameter `k` to minimize the new error.
* **D. Meaning of the output:** The fitted growth rate of a population, visually matching an exponential curve to raw lab data.
* **E. Real-world case modification:** Biology. Fitting an exponential growth curve to bacteria data instead of server response times.

### Task 15: Numerical Differentiation
**File:** `Task_15_Numerical_Differentiation/task_15.py`
* **B. Input values and mathematical operation performed:** Stock prices over time. Forward, central, and backward differences approximate the derivative.
* **C. Change input/parameter and result:** Artificially spiking a single price creates strong positive momentum before it and negative momentum after.
* **D. Meaning of the output:** The daily rate of change (momentum). Positive means trending up, negative means down.
* **E. Real-world case modification:** Finance. Calculating algorithmic trading momentum signals instead of GPS vehicle speed.

### Task 16: Numerical Integration
**File:** `Task_16_Numerical_Integration/task_16.py`
* **B. Input values and mathematical operation performed:** Hourly water flow rates. Trapezoidal and Simpson's rules compute the area under the curve.
* **C. Change input/parameter and result:** Increasing a peak flow rate adds to the total area, increasing the final volume output.
* **D. Meaning of the output:** The total cumulative volume of water discharged through a dam over a 12-hour period.
* **E. Real-world case modification:** Hydrology. Integrating dam water flow into total volume instead of smart meter electrical energy.

### Task 17: Ordinary Differential Equations – Euler Method
**File:** `Task_17_Euler_ODE/task_17.py`
* **B. Input values and mathematical operation performed:** Initial population, carrying capacity, step size. Iterative updates via `P += h * (dP/dt)`.
* **C. Change input/parameter and result:** Increasing step size `h` makes the model unstable, causing large overshoot errors.
* **D. Meaning of the output:** Logistic population growth forming an S-curve that flattens at environmental limits.
* **E. Real-world case modification:** Ecology. Modeling carrying-capacity restricted population growth instead of Newton's law of cooling.

### Task 18: Numerical Solution of ODEs Using SciPy
**File:** `Task_18_SciPy_ODE/task_18.py`
* **B. Input values and mathematical operation performed:** SIR disease parameters. `solve_ivp` integrates the 3 coupled non-linear ODEs.
* **C. Change input/parameter and result:** Increasing the infection rate makes the infected peak higher and earlier.
* **D. Meaning of the output:** The epidemiological curves (Susceptible, Infected, Recovered) tracking an outbreak over time.
* **E. Real-world case modification:** Epidemiology. Modeling viral disease spread (SIR model) instead of RC circuit charging.

### Task 19: Numerical Optimization
**File:** `Task_19_Optimization/task_19.py`
* **B. Input values and mathematical operation performed:** Factory costs and constraints. `minimize` (SLSQP) finds the lowest cost allocation.
* **C. Change input/parameter and result:** Raising the minimum demand constraint forces higher production and thus a higher minimum total cost.
* **D. Meaning of the output:** The optimal factory production split to minimize costs while strictly meeting market demand.
* **E. Real-world case modification:** Supply Chain. Minimizing multi-factory production costs subject to demand instead of cloud server allocation.

### Task 20: Random Numbers and Monte Carlo Methods
**File:** `Task_20_Monte_Carlo/task_20.py`
* **B. Input values and mathematical operation performed:** Mean and std dev for project tasks. `np.random.normal` generates scenarios to find an empirical probability.
* **C. Change input/parameter and result:** Increasing task uncertainty widens the total duration spread, reducing the chance of meeting a strict deadline.
* **D. Meaning of the output:** The probability of finishing a project on time. The graph shows the Monte Carlo accuracy stabilizing over many simulations.
* **E. Real-world case modification:** Project Management. Using PERT analysis simulations for project deadlines instead of server network overloads.

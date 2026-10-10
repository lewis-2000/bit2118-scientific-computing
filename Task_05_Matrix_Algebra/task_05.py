"""
BIT 2118: SCIENTIFIC COMPUTING
Task 5: Matrix Algebra and Matrix Operations

B. Identify the input values and the mathematical operation performed.
- Input values: A 2D array of coordinates representing an image bounding box (points), a scaling matrix, and a shear matrix.
- Mathematical operations: Matrix multiplication (`@`) to apply the shear and scale transformations to the coordinates. `np.linalg.det` to find the determinant.

C. Change at least one input/parameter and explain how the result changes.
- Change: Increase the shear factor from 0.5 to 1.5.
- Result: The bounding box will be skewed significantly more along the x-axis, shifting the top coordinates much further to the right. The determinant of the transformation matrix will remain the same if it's a pure shear, but the physical shape is more distorted.

D. Explain the meaning of the output in words and interpret the graph where necessary.
- Output meaning: Shows the original coordinates of the box and their new coordinates after being scaled up and sheared. The determinant of the transformation indicates how much the area of the bounding box has scaled.

E. Modify the program to solve a different but related real-world case.
- New Case: Computer vision/graphics. Transforming a 2D bounding box detected around an object in an image to normalize its perspective (scaling and shearing) before feeding it into a neural network for classification.
"""
import numpy as np

# Original bounding box corners [x, y]
bounding_box = np.array([
    [0.0, 0.0],
    [2.0, 0.0],
    [2.0, 2.0],
    [0.0, 2.0]
])

# Scale matrix (double in size)
scale = np.array([
    [2.0, 0.0],
    [0.0, 2.0]
])

# Shear matrix (shear along x-axis)
shear_factor = 0.5
shear = np.array([
    [1.0, shear_factor],
    [0.0, 1.0]
])

transformation = shear @ scale
transformed_box = bounding_box @ transformation.T

print("Original bounding box:\n", bounding_box)
print("Transformation matrix:\n", transformation)
print("Transformed bounding box:\n", transformed_box)
print("Determinant (Area scale factor):", np.linalg.det(transformation))

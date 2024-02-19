import numpy as np
np.set_printoptions(suppress=True)

# Points from the map and corresponding points on the json repr
map_points = np.array([(-1000, 0), (-1500, -1500), (0, 0)])

json_points = np.array([(500, 1500), (0, 0), (1500, 1500)])

# Compute transformation matrix using Affine Transformation
transformation_matrix = np.linalg.lstsq(map_points, json_points, rcond=None)[0]

# Adding ones to the map points for affine transformation
map_points_homogeneous = np.hstack([map_points, np.ones((map_points.shape[0], 1))])

# Compute transformation matrix using Affine Transformation
transformation_matrix, residuals, rank, s = np.linalg.lstsq(map_points_homogeneous, json_points, rcond=None)
transformation_matrix = transformation_matrix.T
print(transformation_matrix)
# Function to transform any given point
def transform_point(map_point):
    map_point_homogeneous = np.array([*map_point, 1])
    return np.dot(transformation_matrix, map_point_homogeneous)

# Example usage
transformed_point = transform_point([-132, 243])
print(f"Transformed Point: {transformed_point}")

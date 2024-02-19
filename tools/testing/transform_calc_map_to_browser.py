import numpy as np
np.set_printoptions(suppress=True)

# Points from the map and corresponding points on the image
map_points = np.array([(0, 0), (-1000, 0), (-132, 243), (-110.39, 399.55),
                       (516.46, 407), (666.89, 482.17), (-145, -642.41),
                       (-722.45, -527.50), (-507.89, -800.35), (-237.44, -429.18),
                       (213.43, 128.79), (818.6, 823.18), (396, 803.77)])

image_points = np.array([(480, 0), (0, 0), (276, -78), (284, -128),
                         (482, -129), (530, -154), (272, 205),
                         (91, 167), (159, 251), (245, 134),
                         (387, -41), (578, -261), (444, -253)])

# Compute transformation matrix using Affine Transformation
transformation_matrix = np.linalg.lstsq(map_points, image_points, rcond=None)[0]

# Adding ones to the map points for affine transformation
map_points_homogeneous = np.hstack([map_points, np.ones((map_points.shape[0], 1))])

# Compute transformation matrix using Affine Transformation
transformation_matrix, residuals, rank, s = np.linalg.lstsq(map_points_homogeneous, image_points, rcond=None)
transformation_matrix = transformation_matrix.T
print(transformation_matrix)
# Function to transform any given point
def transform_point(map_point):
    map_point_homogeneous = np.array([*map_point, 1])
    return np.dot(transformation_matrix, map_point_homogeneous)

# Example usage
transformed_point = transform_point([-132, 243])
print(f"Transformed Point: {transformed_point}")

import numpy as np
np.set_printoptions(suppress=True)
# for a map 1000x1000
# Points from the map and corresponding points on the json repr
json_points = np.array([(276.6379,724.0268), (733.577, 730.3), (565.325,435.934),
                        (414.82,413.8), (471.137,591.269), (511.5399,519.476),
                        (625.6,592.1)])

browser_points = np.array([(429,260), (861,254), (703, 532), (559,552), (611,385),
                           (651,453), (758,383)])

# Compute transformation matrix using Affine Transformation
transformation_matrix = np.linalg.lstsq(json_points, browser_points, rcond=None)[0]

# Adding ones to the map points for affine transformation
json_points_homogeneous = np.hstack([json_points, np.ones((json_points.shape[0], 1))])

# Compute transformation matrix using Affine Transformation
transformation_matrix, residuals, rank, s = np.linalg.lstsq(json_points_homogeneous, browser_points, rcond=None)
transformation_matrix = transformation_matrix.T
print(transformation_matrix)
# Function to transform any given point
def transform_point(map_point):
    json_point_homogeneous = np.array([*map_point, 1])
    return np.dot(transformation_matrix, json_point_homogeneous)

# Example usage
transformed_point = transform_point([625.5999, 592.100])
print(f"Transformed Point: {transformed_point}")

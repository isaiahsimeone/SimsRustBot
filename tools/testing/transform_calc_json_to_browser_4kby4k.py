import numpy as np
np.set_printoptions(suppress=True)
# for a map 4000x4000
# Points from the map and corresponding points on the json repr
json_points = np.array([(894.87,970),(794,1341), (703,1763), (540.5,1989.34), (643.18, 2498.75),
                        (823.05, 2696.49), (867.88, 3265.46), (1322.47, 3042.088), (1619.922, 2863.55),
                        (1995.56, 3202.17), (2714.8, 3297.85), (3300.30, 2979.151), (3285.75,373.08),
                        (2403.33, 354.48)])

browser_points = np.array([(378,715), (355,627), (333,528), (295, 474), (319, 354),
                           (362, 243), (373,173), (479, 225), (550, 269), (638, 189),
                           (808, 166), (947,241), (944, 846), (734,862)])

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
transformed_point = transform_point([-132, 243])
print(f"Transformed Point: {transformed_point}")

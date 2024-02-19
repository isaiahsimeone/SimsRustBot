import numpy as np
np.set_printoptions(suppress=True)
# for a map 3000x3000
# Points from the map and corresponding points on the json repr
json_points = np.array([(1119,805), (1692,1402), (2014,1904), (2169,1981), (2320,2324), (1343,2298), (566,2492), (380, 1755), (433,1419),
                        (729,1332), (771, 970), (917,972), (1083, 934), (1943,442), (2403,355), (2581.4,1217.5),
                        (2460.58,2225.5), (2251,2532), (1897.99,2659.1), (1425.44,2403.07), (879.22,2341.97)])

browser_points = np.array([(521,945), (576,503), (802,343), (850,319), (897,215), (591,220), (353,161), (287,389), (305,498), (396,525),
                           (412,639), (457,638), (508,651), (779,806), (927,833), (980,561), (943,243),
                           (876,147), (765,107), (616,188), (444,206)])

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

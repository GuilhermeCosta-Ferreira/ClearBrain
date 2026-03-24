# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from scipy.spatial import KDTree



# ================================================================
# 1. Section: Functions
# ================================================================
def filter_low_density_points(
    points: np.ndarray,
    density_radius: float,
    min_density: int,
) -> np.ndarray:
    tree = KDTree(points)
    densities = np.array(
        [len(tree.query_ball_point(p, r=density_radius)) - 1 for p in points]
    )
    return points[densities > min_density]

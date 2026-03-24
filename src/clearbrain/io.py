# ================================================================
# 0. Section: IMPORTS
# ================================================================
import os
import json

import numpy as np

from pathlib import Path



# ================================================================
# 1. Section: Functions
# ================================================================
def load_points(filepath: Path) -> np.ndarray:
    # A. Makes sure there is a file
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    # 1. Extracts the data from the JSON
    with open(filepath, "r") as f:
        points = np.array(json.load(f), dtype=float)

    # B. Makes sure the file is not empty and the shape is ok
    if points.size == 0:
        raise ValueError(f"Points file is empty: {filepath}")
    if points.shape[1] != 2 and points.shape[1] != 3:
        raise ValueError(f"Expected shape (N, 3), got {points.shape} in file: {filepath}")

    return points

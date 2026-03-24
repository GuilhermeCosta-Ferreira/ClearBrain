# ================================================================
# 0. Section: IMPORTS
# ================================================================
from pathlib import Path

from clearbrain import (
    load_points,
    scale_points,
    filter_low_density_points,
    get_centerline,
    smooth_centerline,
    plot_3d_clearD,
    save_centerline,
    get_density
)



# ================================================================
# 1. Section: INPUTS
# ================================================================
# IO Settings
DATA_FOLDER: Path = Path("data")
PLOT_FOLDER: Path = Path("out")
JSON_FILES: list = ["32B_SC_sensitive.json"]

# Scaling Settings
X_SCALE: float = 2.22  # Why?
Y_SCALE: float = 1.0
Z_SCALE: float = 1.0

# Cenetrline Settings
DENSITY_RADIUS: int = 50
MIN_DENSITY: int = 20
BIN_WIDTH: int = 500

# Centerline Smoothing Settings
SPLINE_SMOOTHING: float = 5000.0  # ← extremely smooth (as requested)
N_POINTS_ON_LINE: float = 4000  # more points = perfectly smooth visual
PLOT_SUBSAMPLE: int = 80  # for fast & clean 3D plot



# ================================================================
# 2. Section: MAIN
# ================================================================
if __name__ == "__main__":
    for filename in JSON_FILES:
        filepath = DATA_FOLDER / filename

        # 1. Load the points
        points = load_points(filepath)
        points = scale_points(points, (X_SCALE, Y_SCALE, Z_SCALE))
        #density = get_density(points, DENSITY_RADIUS)


        # 2. Remove sparse points
        #points = filter_low_density_points(points, DENSITY_RADIUS, MIN_DENSITY)

        # 3. Get the centerline and smooths it
        centerline = get_centerline(points, BIN_WIDTH)
        #centerline = smooth_centerline(centerline, SPLINE_SMOOTHING, N_POINTS_ON_LINE)

        # 4. Generate the 3D plot
        fig_3d = plot_3d_clearD(points, centerline, filepath.stem, PLOT_SUBSAMPLE)
        fig_3d.show()

        # 5. Saved the data
        save_centerline(centerline, fig_3d, PLOT_FOLDER, filepath.stem)

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from matplotlib import pyplot as plt
import numpy as np



# ================================================================
# 1. Section: Functions
# ================================================================
def plot_clear_data_with_centerline(
    points: np.ndarray,
    centerline: np.ndarray,
    plot_subsample: int = 80,
    highlight_centerline: bool = False,
) -> tuple:

    # 1. Instantiates the Plot
    fig_3d = plt.figure(figsize=(10, 6))
    ax = fig_3d.add_subplot(projection='3d', computed_zorder= not highlight_centerline)

    # 2. Loads and Plots the ClearData in a subsample manner
    reduced_points = points[::plot_subsample]
    x = reduced_points[:, 0]
    y = reduced_points[:, 1]
    z = reduced_points[:, 2]
    ax.scatter(x, y, z, s=1, label="High-density cFos cells") # type: ignore
    ax.set_box_aspect((np.ptp(x), np.ptp(y), np.ptp(z)))

    # 3. Loads Plots the centerline
    if highlight_centerline:
        centerline_z_order = 10
    else:
        centerline_z_order = None

    x = centerline[:, 0]
    y = centerline[:, 1]
    z = centerline[:, 2]
    ax.scatter(x, y, z, s=1, color='red', label="Centerline", zorder=centerline_z_order) # type: ignore

    # 4. Remove extra visual clutter
    ax.grid(False)
    ax.set_axis_off()

    return fig_3d, ax

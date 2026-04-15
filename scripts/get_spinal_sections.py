# ================================================================
# 0. Section: IMPORTS
# ================================================================
from matplotlib import pyplot as plt

from pathlib import Path

from clearbrain.sections import get_spinal_sections, plot_spinal_sections
from clearbrain.save import save_to_json
from clearbrain import load_points



# ================================================================
# 1. Section: INPUTS
# ================================================================
# IO Settings
DATA_FOLDER: Path = Path("data")
MICE: list = ["32B"]
FILE_TARGET: str = "filtered_points_sc.json"

PRISM_HALF_WIDTH: int = 1000        # ← 2000×2000 square base (as requested)
PRISM_HALF_THICKNESS: int = 250     # ← 500 units thick
N_CUTS: int = 10                    # 10 axial cuts



# ================================================================
# 3. Section: MAIN
# ================================================================
if __name__ == '__main__':
    for mouse in MICE:
        filepath = DATA_FOLDER / mouse / FILE_TARGET
        centerline_path = DATA_FOLDER / mouse / "centerline_sc.json"

        # 1. Load the points
        points = load_points(filepath)
        centerline = load_points(centerline_path)

        # 2. Get the spinal sections
        spinal_sections = get_spinal_sections(centerline, N_CUTS, PRISM_HALF_WIDTH, PRISM_HALF_THICKNESS)

        # 3. Generate the 3D plot
        plot_spinal_sections(spinal_sections, points, centerline)
        plt.show()

        # 4. Saved the data
        out_path = save_to_json(centerline.tolist(), filepath.parent, "sections_sc.json")
        print(f"Saved filtered data from {mouse} into {out_path}")

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from matplotlib import pyplot as plt

from pathlib import Path

from clearbrain import ClearData, plot_3d_clearD


# ================================================================
# 1. Section: INPUTS
# ================================================================
BASE_FOLDER: Path = Path("data")
CLEAR_DATA_FILE: str = "32B_SC_sensitive.json"



# ================================================================
# 2. Section: FUNCTIONS
# ================================================================



# ================================================================
# 3. Section: MAIN
# ================================================================
if __name__ == '__main__':
    # 1. Import the data
    file_path = BASE_FOLDER / CLEAR_DATA_FILE
    clear_spine = ClearData(file_path)

    #fig_3d = plot_3d_clearD(clear_spine.points, file_path.stem, 1)
    #fig_3d.show()

    clear_space = clear_spine.space

    plt.imshow(clear_space[:,:, 0])
    plt.show()

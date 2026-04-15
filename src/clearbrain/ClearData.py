# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from pathlib import Path

from .io import load_points



# ================================================================
# 1. Section: Functions
# ================================================================
class ClearData:
    def __init__(self, file_path: Path) -> None:
        self.path = file_path
        self.points = load_points(self.path)

    @property # needs downsample
    def space(self):
        x = self.points[:,0].max()
        y = self.points[:,1].max()
        z = self.points[:,2].max()

        print(int(x))
        print(int(y))
        print(int(z))

        #space = np.zeros((int(x)+1, int(y)+1, int(z)+1))
        #pts = self.points.astype(np.uint8)
        #np.add.at(space, (pts[:, 0], pts[:, 1], pts[:, 2]), 1)

        return x

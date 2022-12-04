import numpy as np

class Grid:

    def __init__(self, height, width) -> None:
        self.grid = np.zeros((height, width))

    def __repr__(self) -> str:
        return str(self.grid)

    def reset(self) -> None:
        self.__init__(self.grid.shape[0], self.grid.shape[1])

    def set(self, model) -> None:
        self.grid = model
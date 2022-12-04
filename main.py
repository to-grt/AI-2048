import numpy as np
from Grid import Grid


shape = (4, 4)
model = np.arange(shape[0] * shape[1]).reshape(shape)

grid = Grid(shape[0], shape[1])
grid.initialization(2)
print(grid)
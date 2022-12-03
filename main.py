import numpy as np
from Grid import Grid


shape = (5, 5)
model = np.arange(shape[0] * shape[1]).reshape(shape)

grid = Grid(shape[0], shape[1])
print(grid)

grid.set(model)
print(grid)

grid.reset()
print(grid)
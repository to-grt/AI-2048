import numpy as np
from Grid import Grid


shape = (6, 6)

grid = Grid(height=shape[0], width=shape[1], prints=False, nb_cells=5)
print(grid)

#TODO faire des tests avec ça
"""
row = np.array([2,2,0,0])
print("initial row: ", row)
grid.perform_simplification(row)
print("resulted row: ", row, '\n')

row = np.array([0,2,0,0])
print("initial row: ", row)
grid.perform_simplification(row)
print("resulted row: ", row, '\n')

row = np.array([8,8,8,8])
print("initial row: ", row)
grid.perform_simplification(row)
print("resulted row: ", row, '\n')

row = np.array([32,16,8,4])
print("initial row: ", row)
grid.perform_simplification(row)
print("resulted row: ", row, '\n')

row = np.array([0,2,0,0])
print("initial row: ", row)
grid.perform_simplification(row)
print("resulted row: ", row, '\n')

row = np.array([0,16,16,0])
print("initial row: ", row)
grid.perform_simplification(row)
print("resulted row: ", row, '\n')
"""

grid.roll_left()
print(grid)
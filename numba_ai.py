import numpy as np
import time

from numba import jit, int32


@jit(nopython=True)
def all_posibilities(grid):
    result = [] 
    for index_y in range(grid.shape[0]):
        for index_x in range(grid.shape[1]):
            if grid[index_y, index_x] == 0:
                grid[index_y, index_x] = 2
                result.append(np.copy(grid))
                grid[index_y, index_x] = 4
                result.append(np.copy(grid))
                grid[index_y, index_x] = 0
    return result

@jit(int32[:](int32[:]), nopython=True) 
def perform_simplification(row):
    if np.sum(row) != 0:
        initial_length = row.shape[0]
        row = row[row != 0]
        for index in range(initial_length-1):
            if row[index] == row[index+1]:
                row[index] *= 2
                row[index+1] = 0
        row = np.append(row, np.zeros(shape=(initial_length-row.shape[0])))
        return row.astype('int32')
    else: return row

@jit(nopython=True)
def roll_left(grid):
    resulted_grid = np.copy(grid)
    for index, row in enumerate(resulted_grid):
        resulted_grid[index] = perform_simplification(row)
    return resulted_grid

@jit(nopython=True)
def roll_right(grid):
    resulted_grid = np.copy(grid)
    for index, row in enumerate(resulted_grid):
        resulted_grid[index] = np.flip(perform_simplification(np.flip(row)))
    return resulted_grid

@jit(nopython=True)
def roll_up(grid):
    resulted_grid = np.copy(grid)
    for index in range(resulted_grid.shape[1]):
        col = resulted_grid[:, index]
        resulted_grid[:, index] = perform_simplification(col)
    return resulted_grid

@jit(nopython=True)
def roll_down(grid):
    resulted_grid = np.copy(grid)
    for index in range(resulted_grid.shape[1]):
        col = resulted_grid[:, index]
        resulted_grid[:, index] = np.flip(perform_simplification(np.flip(col)))
    return resulted_grid   









grid = np.array([[0,1,2,3], [4,5,6,7], [8,9,10,11], [12,13,14,15]])

ja = all_posibilities(grid)

start = time.time()
print("initial:\n", grid)
grid = roll_left(grid)
print("left:\n", grid)
grid = roll_right(grid)
print("right:\n", grid)
grid = roll_up(grid)
print("up:\n", grid)
grid = roll_down(grid)
print("down:\n", grid)

end = time.time()
print("elapsed time: ", end-start)
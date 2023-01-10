import numpy as np
import time

from numba import jit, int32

MAX_DEPTH       = 2
SUM_MAX         = 0
MAX_DISTANCES   = 0

"""@jit(nopython=True)
def get_esperances(grid, depth):
    esperances = []

    right = roll_right(grid)
    if (right != grid).any():   
        esperance_right = compute_esperance(all_posibilities(right), depth)
        esperances.append(esperance_right)
    else: esperances.append(0)

    left = roll_left(grid)
    if (left != grid).any():
        esperance_left = compute_esperance(all_posibilities(left), depth)
        esperances.append(esperance_left)
    else: esperances.append(0)

    up = roll_up(grid)
    if (up != grid).any():
        esperance_up = compute_esperance(all_posibilities(up), depth)
        esperances.append(esperance_up)
    else: esperances.append(0)

    down = roll_down(grid)
    if (down != grid).any():
        esperance_down = compute_esperance(all_posibilities(down), depth)
        esperances.append(esperance_down)
    else: esperances.append(0)
    
    return esperances"""


"""@jit(nopython=True)
def compute_esperance(successors, depth):    # a successor is just a grid
    lenght = successors.shape[0]
    scores = np.zeros(shape=lenght)
    for index, successor in enumerate(successors):
        if depth == MAX_DEPTH: scores[index] = policies(successor)
        else: scores[index] = np.max(get_esperances(successor, depth+1))
    scores[0:lenght:2] *= 0.9
    scores[1:lenght:2] *= 0.1
    return np.sum(scores)/(lenght/2)"""


@jit(nopython=True)
def policies(grid, SUM_MAX, MAX_DISTANCES):
    if is_game_over(grid): return (0.001, SUM_MAX, MAX_DISTANCES)
    score_nb_empty_cells = min_max_norm(np.sum(grid==0), 0, 16)
    print("score_nb_empty_cells: ", score_nb_empty_cells)
    sum_grid = np.sum(grid)
    if sum_grid > SUM_MAX: SUM_MAX = sum_grid
    score_sum_grid = min_max_norm(sum_grid, 0, SUM_MAX)
    arg_max = np.unravel_index(np.argmax(grid, axis=None), grid.shape)
    distance_closest_corner = np.min(np.array([np.sqrt((arg_max[0] - 0)**2 + (arg_max[1] - 0)**2), np.sqrt((arg_max[0] - grid.shape[0]-1)**2 + (arg_max[1] - grid.shape[1]-1)**2), np.sqrt((arg_max[0] - grid.shape[0]-1)**2 + (arg_max[1] - 0)**2), np.sqrt((arg_max[0] - grid.shape[0]-1)**2 + (arg_max[1] - grid.shape[1]-1)**2)]))
    score_distance_corner = 1-min_max_norm(distance_closest_corner, 0, np.sqrt(18))
    sum_distance = 0
    for index_y, row in enumerate(grid):
        for index_x, _ in enumerate(row):
            if index_x != 0:                sum_distance += np.abs(grid[index_y, index_x-1] - grid[index_y, index_x])
            if index_x != grid.shape[1]-1:  sum_distance += np.abs(grid[index_y, index_x+1] - grid[index_y, index_x])
            if index_y != 0:                sum_distance += np.abs(grid[index_y-1, index_x] - grid[index_y, index_x])
            if index_y != grid.shape[0]-1:  sum_distance += np.abs(grid[index_y+1, index_x] - grid[index_y, index_x])
    if sum_distance > MAX_DISTANCES: MAX_DISTANCES = sum_distance
    score_sum_distance = 1-min_max_norm(sum_distance, 0, MAX_DISTANCES)
    coefficients = [1.5, 1.5, 1.5, 1]
    score = coefficients[0]*score_nb_empty_cells + coefficients[1]*score_sum_grid + coefficients[2]*score_distance_corner +  coefficients[3]*score_sum_distance
    return (score, SUM_MAX, MAX_DISTANCES)


@jit(nopython=True)
def min_max_norm(value, min, max):
    return (value-min)/(max - min)


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

@jit(nopython=True)
def is_game_over(grid) -> bool:
    down = roll_down(grid)
    if not np.array_equal(grid, down): return False
    up = roll_up(grid)
    if not np.array_equal(grid, up): return False
    left = roll_left(grid)
    if not np.array_equal(grid, left): return False
    right = roll_right(grid)
    if not np.array_equal(grid, right): return False    
    return True    

@jit(nopython=True)
def is_win(grid) -> bool:
    if np.max(grid) >= 10000: return True
    return False  

@jit(nopython=True)
def set_random_cells(grid, nb_cells):
    resulted_grid = np.copy(grid)
    for _ in range(nb_cells):
        index_row = np.random.randint(0, resulted_grid.shape[0])
        index_column = np.random.randint(0, resulted_grid.shape[1])
        if resulted_grid[index_row, index_column] == 0:
            random_value = np.random.randint(0, 10)
            resulted_grid[index_row, index_column] = 2 if random_value <= 8 else 4
        else: 
            return set_random_cells(grid, 1)
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
is_game = is_game_over(grid)
print("is_game_over? ", is_game)
is_it_win = is_win(grid)
print("is_it_win? ", is_it_win)
result = set_random_cells(grid, 1)
print("set_random_cells:\n", result)
result = min_max_norm(100, 0, 1000)
print("min_max_norm: ", result)
score, sum_max, max_distances = policies(grid, SUM_MAX, MAX_DISTANCES)
print("policies: ", score, sum_max, max_distances)

end = time.time()
print("elapsed time: ", end-start)
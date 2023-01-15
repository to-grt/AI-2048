import os
import time
import numpy as np
import numba as nb

from numba import jit, int32
from bcolors import bcolors as bc

def repr(grid):
    repr = "\n"
    max_len = len(str(int(np.max(grid))))
    for y in range(grid.shape[1]):
        for _ in range(max_len*grid.shape[0]+5):
            repr += '-'
        repr += '\n'
        for x in range(grid.shape[1]):
            value = str(int(grid[y,x]))
            repr += '|'
            for _ in range(max_len - len(value)): repr += ' '
            if value == '0': repr += bc.OKGREEN + value + bc.ENDC
            elif int(value) <= 32: repr += bc.FAIL + value + bc.ENDC
            else: repr += bc.OKBLUE + value + bc.ENDC
        repr += '|\n'
    for _ in range(max_len*grid.shape[0]+5):
        repr += '-'
    return repr

@jit(nb.float64(nb.int32, nb.int32, nb.int32), nopython=True)
def min_max_norm(value, min, max):
    return (value-min)/(max - min)

@jit(nb.int32[:,:,:](nb.int32[:,:]), nopython=True, cache=True)
def all_posibilities(grid):
    result = np.empty(shape=(0, grid.shape[0], grid.shape[1]), dtype=np.int32) 
    copied_grid = np.expand_dims(np.copy(grid), axis=0)
    for index_y in range(grid.shape[0]):
        for index_x in range(grid.shape[1]):
            if copied_grid[0, index_y, index_x] == 0:
                copied_grid[0, index_y, index_x] = 2
                result = np.concatenate((result, copied_grid))
                copied_grid[0, index_y, index_x] = 4
                result = np.concatenate((result, copied_grid))
                copied_grid[0, index_y, index_x] = 0
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

@jit(nb.int32[:,:](nb.int32[:,:]), nopython=True)
def roll_left(grid):
    resulted_grid = np.copy(grid)
    for index, row in enumerate(resulted_grid):
        resulted_grid[index] = perform_simplification(row)
    return resulted_grid

@jit(nb.int32[:,:](nb.int32[:,:]), nopython=True)
def roll_right(grid):
    resulted_grid = np.copy(grid)
    for index, row in enumerate(resulted_grid):
        resulted_grid[index] = np.flip(perform_simplification(np.flip(row)))
    return resulted_grid

@jit(nb.int32[:,:](nb.int32[:,:]), nopython=True)
def roll_up(grid):
    resulted_grid = np.copy(grid)
    for index in range(resulted_grid.shape[1]):
        col = resulted_grid[:, index]
        resulted_grid[:, index] = perform_simplification(col)
    return resulted_grid

@jit(nb.int32[:,:](nb.int32[:,:]), nopython=True)
def roll_down(grid):
    resulted_grid = np.copy(grid)
    for index in range(resulted_grid.shape[1]):
        col = resulted_grid[:, index]
        resulted_grid[:, index] = np.flip(perform_simplification(np.flip(col)))
    return resulted_grid

@jit(nb.boolean(nb.int32[:,:]), nopython=True)
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

@jit(nb.boolean(nb.int32[:,:]), nopython=True)
def is_win(grid) -> bool:
    if np.max(grid) >= 10000: return True
    return False  

@jit(nb.int32[:,:](nb.int32[:,:], int32),nopython=True)
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

@jit(nb.float64[:](nb.int32[:,:], nb.int32, nb.int32), nopython=True)
def policies(grid, SUM_MAX, MAX_DISTANCES):
    if is_game_over(grid): return np.array([0.001, SUM_MAX, MAX_DISTANCES])
    score_nb_empty_cells = min_max_norm(np.sum(grid==0), 0, 14)
    sum_grid = np.sum(grid)
    if sum_grid > SUM_MAX: SUM_MAX = sum_grid
    score_sum_grid = min_max_norm(sum_grid, 0, SUM_MAX)
    index_max = np.argmax(grid, axis=None)
    arg_max = (index_max // grid.shape[1], index_max % grid.shape[1])
    distance_closest_corner = np.min(np.array([np.sqrt((arg_max[0] - 0)**2 + (arg_max[1] - 0)**2), np.sqrt((arg_max[0] - grid.shape[0]-1)**2 + (arg_max[1] - grid.shape[1]-1)**2), np.sqrt((arg_max[0] - grid.shape[0]-1)**2 + (arg_max[1] - 0)**2), np.sqrt((arg_max[0] - grid.shape[0]-1)**2 + (arg_max[1] - grid.shape[1]-1)**2)]))
    score_distance_corner = 1-min_max_norm(distance_closest_corner, 0, np.sqrt(18))
    sum_distance = 0
    for index_y, row in enumerate(grid):
        for index_x, _  in enumerate(row):
            if index_x != 0:                sum_distance += np.abs(grid[index_y, index_x-1] - grid[index_y, index_x])
            if index_x != grid.shape[1]-1:  sum_distance += np.abs(grid[index_y, index_x+1] - grid[index_y, index_x])
            if index_y != 0:                sum_distance += np.abs(grid[index_y-1, index_x] - grid[index_y, index_x])
            if index_y != grid.shape[0]-1:  sum_distance += np.abs(grid[index_y+1, index_x] - grid[index_y, index_x])
    if sum_distance > MAX_DISTANCES: MAX_DISTANCES = sum_distance
    score_sum_distance = 1-min_max_norm(sum_distance, 0, MAX_DISTANCES)
    coefficients = [1.5, 1.5, 1.5, 1]
    score = coefficients[0]*score_nb_empty_cells + coefficients[1]*score_sum_grid + coefficients[2]*score_distance_corner +  coefficients[3]*score_sum_distance
    return np.array([score, SUM_MAX, MAX_DISTANCES])

# beaucoup de répétition de code dans cette fonction, mais c'est à cause de numba, les fonctions s'appelant les unes et les autres posent des soucis
@jit(nb.float64[:](nb.int32[:,:], nb.int32, nb.int32, nb.int32, nb.int32), nopython=True)
def get_esperances(grid, depth, MAX_DEPTH, SUM_MAX, MAX_DISTANCES):
    scores=None
    esperances = np.empty(shape=(7,), dtype=np.float64)
    esperances[4] = MAX_DEPTH
    esperances[5] = SUM_MAX
    esperances[6] = MAX_DISTANCES
    right = roll_right(grid)
    if (right != grid).any():
        successors = all_posibilities(right)
        nb_successors = successors.shape[0]
        scores = np.zeros(shape=nb_successors)
        for index, successor in enumerate(successors):
            if depth == MAX_DEPTH:
                scores[index], temp_sum_max, temp_max_dist = policies(successor, SUM_MAX, MAX_DISTANCES)
                if temp_sum_max > esperances[5]: esperances[5] = temp_sum_max
                if temp_max_dist > esperances[6]: esperances[6] = temp_max_dist
            else:
                s_esp_0, s_esp_1, s_esp_2, s_esp_3, MAX_DEPTH, SUM_MAX, MAX_DISTANCES = get_esperances(successor, depth+1, MAX_DEPTH, SUM_MAX, MAX_DISTANCES)
                s_esp = np.array([s_esp_0, s_esp_1, s_esp_2, s_esp_3])
                scores[index] = np.max(s_esp)
        scores[0:nb_successors:2] *= 0.9
        scores[1:nb_successors:2] *= 0.1
        esperances[0] = np.sum(scores)/(nb_successors/2) #esperance right
    else: esperances[0] = 0

    left = roll_left(grid)
    if (left != grid).any():
        successors = all_posibilities(left)
        nb_successors = successors.shape[0]
        scores = np.zeros(shape=nb_successors)
        for index, successor in enumerate(successors):
            if depth == MAX_DEPTH:
                scores[index], temp_sum_max, temp_max_dist = policies(successor, SUM_MAX, MAX_DISTANCES)
                if temp_sum_max > esperances[5]: esperances[5] = temp_sum_max
                if temp_max_dist > esperances[6]: esperances[6] = temp_max_dist
            else:
                s_esp_0, s_esp_1, s_esp_2, s_esp_3, MAX_DEPTH, SUM_MAX, MAX_DISTANCES = get_esperances(successor, depth+1, MAX_DEPTH, SUM_MAX, MAX_DISTANCES)
                s_esp = np.array([s_esp_0, s_esp_1, s_esp_2, s_esp_3])
                scores[index] = np.max(s_esp)
        scores[0:nb_successors:2] *= 0.9
        scores[1:nb_successors:2] *= 0.1
        esperances[1] = np.sum(scores)/(nb_successors/2) #esperance right
    else: esperances[1] = 0

    up = roll_up(grid)
    if (up != grid).any():
        successors = all_posibilities(up)
        nb_successors = successors.shape[0]
        scores = np.zeros(shape=nb_successors)
        for index, successor in enumerate(successors):
            if depth == MAX_DEPTH:
                scores[index], temp_sum_max, temp_max_dist = policies(successor, SUM_MAX, MAX_DISTANCES)
                if temp_sum_max > esperances[5]: esperances[5] = temp_sum_max
                if temp_max_dist > esperances[6]: esperances[6] = temp_max_dist
            else:
                s_esp_0, s_esp_1, s_esp_2, s_esp_3, MAX_DEPTH, SUM_MAX, MAX_DISTANCES = get_esperances(successor, depth+1, MAX_DEPTH, SUM_MAX, MAX_DISTANCES)
                s_esp = np.array([s_esp_0, s_esp_1, s_esp_2, s_esp_3])
                scores[index] = np.max(s_esp)
        scores[0:nb_successors:2] *= 0.9
        scores[1:nb_successors:2] *= 0.1
        esperances[2] = np.sum(scores)/(nb_successors/2) #esperance right
    else: esperances[2] = 0

    down = roll_down(grid)
    if (down != grid).any():
        successors = all_posibilities(down)
        nb_successors = successors.shape[0]
        scores = np.zeros(shape=nb_successors)
        for index, successor in enumerate(successors):
            if depth == MAX_DEPTH:
                scores[index], temp_sum_max, temp_max_dist = policies(successor, SUM_MAX, MAX_DISTANCES)
                if temp_sum_max > esperances[5]: esperances[5] = temp_sum_max
                if temp_max_dist > esperances[6]: esperances[6] = temp_max_dist
            else:
                s_esp_0, s_esp_1, s_esp_2, s_esp_3, MAX_DEPTH, SUM_MAX, MAX_DISTANCES = get_esperances(successor, depth+1, MAX_DEPTH, SUM_MAX, MAX_DISTANCES)
                s_esp = np.array([s_esp_0, s_esp_1, s_esp_2, s_esp_3])
                scores[index] = np.max(s_esp)
        scores[0:nb_successors:2] *= 0.9
        scores[1:nb_successors:2] *= 0.1
        esperances[3] = np.sum(scores)/(nb_successors/2) #esperance right-è
    else: esperances[3] = 0
    
    return esperances

def clear(): os.system('cls')

def ai_loop(grid):


    SUM_MAX = 0
    MAX_DISTANCES = 0
    command = ""
    while not is_game_over(grid) and not is_win(grid) and command != "exit":


        nb_empty_cells = np.sum(grid==0)
        if nb_empty_cells >= 5: DEPTH_MAX = 2
        else: DEPTH_MAX = 3
        results = get_esperances(grid, depth=1, MAX_DEPTH=DEPTH_MAX, SUM_MAX=SUM_MAX, MAX_DISTANCES=MAX_DISTANCES)
        esperances = results[:4]
        SUM_MAX = results[5]
        MAX_DISTANCES = results[6]
        best_choice = np.argmax(esperances)
        if best_choice==0: command="right"
        elif best_choice==1: command="left"
        elif best_choice==2: command="up"
        elif best_choice==3: command="down"
        else: command="exit"
        
        if command == "up" or command == "z":
            up = roll_up(grid)
            if (up != grid).any(): grid = set_random_cells(up, 1)
        elif command == "down" or command == "s":
            down = roll_down(grid)
            if (down != grid).any(): grid = set_random_cells(down, 1)
        elif command == "left" or command == "q":
            left = roll_left(grid)
            if (left != grid).any(): grid = set_random_cells(left, 1)
        elif command == "right" or command == "d":
            right = roll_right(grid)
            if (right != grid).any(): grid = set_random_cells(right, 1)
        elif command == "exit": pass
        else: input("Command not recognized, press ay key to continue...\n>> ")
    
        clear()
        print("----------------------\n\n","DEPTH_MAX=", DEPTH_MAX,"\n", repr(grid), "\n\n")

        
        if is_game_over(grid):
            clear()
            print("----------------------\n\n", repr(grid), "\n\n")
            print("Game over :( Good job going that far !\nMax cell achieved:", np.max(grid))
        
        if is_win(grid):
            clear()
            print("----------------------\n\n", repr(grid), "\n\n")
            print("You won the game !! Good job")
        
        if command == "exit":
            clear()
            print("----------------------\n\n", repr(grid), "\n\n")
            print("You decided to exit the game, we hope to see you soon")
            input("Press any key to continue...\n>> ")
            pass
            
        




grid = np.array([[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]])
grid = set_random_cells(grid, 2)
start = time.time()
ai_loop(grid=grid)
end = time.time()
print("elapsed time: ", end-start)
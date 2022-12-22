from bcolors import bcolors as bc
import numpy as np
import os

class State:

    def __init__(self) -> None:
        self.max_distances = 0

    #-------------------------------------------------------------------------------------------
    #------------------------USUAL FUNCTIONS----------------------------------------------------  

    def repr(self, grid) -> str:
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

    #-------------------------------------------------------------------------------------------
    #------------------------STATE FUNCTIONS----------------------------------------------------  

    def get_esperances(self, grid) -> list:
        esperances = []

        right = self.roll_right(grid)
        if (right != grid).any():
            esperance_right = self.compute_esperance(self.all_posibilities(right))
            esperances.append(esperance_right)
        else: esperances.append(0)

        left = self.roll_left(grid)
        if (left != grid).any():
            esperance_left = self.compute_esperance(self.all_posibilities(left))
            esperances.append(esperance_left)
        else: esperances.append(0)

        up = self.roll_up(grid)
        if (up != grid).any():
            esperance_up = self.compute_esperance(self.all_posibilities(up))
            esperances.append(esperance_up)
        else: esperances.append(0)

        down = self.roll_down(grid)
        if (down != grid).any():
            esperance_down = self.compute_esperance(self.all_posibilities(down))
            esperances.append(esperance_down)
        else: esperances.append(0)
        
        return esperances

    # compute the esperance of a move
    def compute_esperance(self, successors) -> int:
        lenght = successors.shape[0]
        scores = np.zeros(shape=lenght)
        for index, successor in enumerate(successors):
            scores[index] = self.policies(successor)
        scores[0:lenght:2] *= 0.9
        scores[1:lenght:2] *= 0.1
        return np.sum(scores)/(lenght/2)

    # score of a grid, where the policies applied.
    def policies(self, grid) -> int:
        score_nb_empty_cells = self.min_max_norm(grid[grid==0].shape[0], 0, 16)
        score_sum_grid = self.min_max_norm(np.sum(grid), 0, np.max(grid))
        arg_max = np.unravel_index(np.argmax(grid, axis=None), grid.shape)
        score_distance_corner = self.min_max_norm(np.sqrt((arg_max[0] - 3)**2 + (arg_max[1] - 0)**2), 0, np.sqrt(18))
        sum_distance = 0
        for index_y, row in enumerate(grid):
            for index_x, _ in enumerate(row):
                if index_x != 0: sum_distance += np.abs(grid[index_y, index_x-1] - grid[index_y, index_x])
                if index_x != grid.shape[1]-1: sum_distance += np.abs(grid[index_y, index_x+1] - grid[index_y, index_x])
                if index_y != 0: sum_distance += np.abs(grid[index_y-1, index_x] - grid[index_y, index_x])
                if index_y != grid.shape[0]-1: sum_distance += np.abs(grid[index_y+1, index_x] - grid[index_y, index_x])
        if sum_distance > self.max_distances: self.max_distances = sum_distance
        score_sum_distance = self.min_max_norm(sum_distance, 0, self.max_distances)
        score = score_nb_empty_cells + score_sum_grid + (1-score_distance_corner) +  (1-score_sum_distance)
        return score

    def min_max_norm(self, value, min, max) -> float:
        return (value-min)/(max - min)

    #-------------------------------------------------------------------------------------------
    #------------------------ENGINE FUNCTIONS---------------------------------------------------

    def clear(self): os.system('cls')

    def ai_loop(self, grid) -> None:

        command = ""
        while not self.is_game_over(grid) and not self.is_win(grid) and command != "exit":

            self.clear()
            print("----------------------\n\n",self.repr(grid), "\n\n")
            esperances = self.get_esperances(grid)
            print("espectation of the ai (1 deep): right:", esperances[0], "  left: ", esperances[1], "  up: ", esperances[2], "  down: ", esperances[3])
            best_choice = np.argmax(esperances)
            if best_choice==0: command="right"
            elif best_choice==1: command="left"
            elif best_choice==2: command="up"
            elif best_choice==3: command="down"
            else: command="exit"
            
            print(">> ai's choice: ", command)
            if command == "up" or command == "z":
                print("up")
                up = self.roll_up(grid)
                if (up != grid).any(): grid = self.set_random_cells(up, 1)
            elif command == "down" or command == "s":
                print("down")
                down = self.roll_down(grid)
                if (down != grid).any(): grid = self.set_random_cells(down, 1)
            elif command == "left" or command == "q":
                print("left")
                left = self.roll_left(grid)
                if (left != grid).any(): grid = self.set_random_cells(left, 1)
            elif command == "right" or command == "d":
                print("right")
                right = self.roll_right(grid)
                if (right != grid).any(): grid = self.set_random_cells(right, 1)
            elif command == "exit": pass
            else: input("Command not recognized, press ay key to continue...\n>> ")
            
            if self.is_game_over(grid):
                self.clear()
                print("----------------------\n\n",self.repr(grid), "\n\n")
                print("You have lost the game, the higher cell you reached was: ", np.max(grid))
                input("Press any key to continue...\n>> ")
            
            if self.is_win(grid):
                self.clear()
                print("----------------------\n\n",self.repr(grid), "\n\n")
                print("You won the game !! Good job")
                input("Press any key to continue...\n>> ")
            
            if command == "exit":
                self.clear()
                print("----------------------\n\n",self.repr(grid), "\n\n")
                print("You decided to exit the game, we hope to see you soon")
                input("Press any key to continue...\n>> ")
                pass

    def game_loop(self, grid) -> None:

        command = ""
        while not self.is_game_over(grid) and not self.is_win(grid) and command != "exit":

            self.clear()
            print("----------------------\n\n",self.repr(grid), "\n\n")
            esperances = self.get_esperances(grid)
            print("espectation of the ai (1 deep): right:", esperances[0], "  left: ", esperances[1], "  up: ", esperances[2], "  down: ", esperances[3])
            command = input("What do you want to do?\n>> ")
            if command == "up" or command == "z":
                print("up")
                up = self.roll_up(grid)
                if (up != grid).any(): grid = self.set_random_cells(up, 1)
            elif command == "down" or command == "s":
                print("down")
                down = self.roll_down(grid)
                if (down != grid).any(): grid = self.set_random_cells(down, 1)
            elif command == "left" or command == "q":
                print("left")
                left = self.roll_left(grid)
                if (left != grid).any(): grid = self.set_random_cells(left, 1)
            elif command == "right" or command == "d":
                print("right")
                right = self.roll_right(grid)
                if (right != grid).any(): grid = self.set_random_cells(right, 1)
            elif command == "exit": pass
            else: input("Command not recognized, press ay key to continue...\n>> ")
            
            if self.is_game_over(grid):
                self.clear()
                print("----------------------\n\n",self.repr(grid), "\n\n")
                print("You have lost the game, the higher cell you reached was: ", np.max(grid))
                input("Press any key to continue...\n>> ")
            
            if self.is_win(grid):
                self.clear()
                print("----------------------\n\n",self.repr(grid), "\n\n")
                print("You won the game !! Good job")
                input("Press any key to continue...\n>> ")
            
            if command == "exit":
                self.clear()
                print("----------------------\n\n",self.repr(grid), "\n\n")
                print("You decided to exit the game, we hope to see you soon")
                input("Press any key to continue...\n>> ")
                pass

    def set_random_cells(self, grid, nb_cells) -> np.array:
        resulted_grid = np.array(grid)
        for _ in range(nb_cells):
            index_row = np.random.randint(0, resulted_grid.shape[0])
            index_column = np.random.randint(0, resulted_grid.shape[1])
            if resulted_grid[index_row, index_column] == 0:
                random_value = np.random.randint(0, 10)
                resulted_grid[index_row, index_column] = 2 if random_value <= 8 else 4
            else: 
                return self.set_random_cells(grid, 1)
        return resulted_grid

    def is_game_over(self, grid) -> bool:     #TODO probably optimizable
        down = self.roll_down(grid)
        if not np.array_equal(grid, down): return False
        up = self.roll_up(grid)
        if not np.array_equal(grid, up): return False
        left = self.roll_left(grid)
        if not np.array_equal(grid, left): return False
        right = self.roll_right(grid)
        if not np.array_equal(grid, right): return False    
        return True    

    def is_win(self, grid) -> bool:
        if np.max(grid) >= 2048: return True
        return False     

    def perform_simplification(self, row) -> np.array:
        if np.sum(row) == 0: return row
        initial_shape = row.shape[0]
        row = row[row != 0]
        for index in range(row.shape[0]-1):
            if row[index] == row[index+1]:
                row[index] *= 2
                row[index+1] = 0
        row = row[row != 0]
        row = np.append(row, np.zeros(shape=(initial_shape-row.shape[0])))
        return row

    def roll_left(self, grid) -> np.array:
        resulted_grid = np.array(grid) # a copy but faster
        for index, row in enumerate(resulted_grid):
            resulted_grid[index] = self.perform_simplification(row)
        return resulted_grid

    def roll_right(self, grid) -> np.array:
        resulted_grid = np.array(grid) # a copy but faster
        for index, row in enumerate(resulted_grid):
            resulted_grid[index] = np.flip(self.perform_simplification(np.flip(row)))
        return resulted_grid

    def roll_up(self, grid) -> np.array:
        resulted_grid = np.array(grid) # a copy but faster
        for index in range(resulted_grid.shape[1]):
            col = resulted_grid[:, index]
            resulted_grid[:, index] = self.perform_simplification(col)
        return resulted_grid

    def roll_down(self, grid) -> np.array:
        resulted_grid = np.array(grid) # a copy but faster
        for index in range(resulted_grid.shape[1]):
            col = resulted_grid[:, index]
            resulted_grid[:, index] = np.flip(self.perform_simplification(np.flip(col)))
        return resulted_grid    

    # after a mouvement is made, we attribute a value (2 or 4) to a random empty cell
    # this list all of the possibilities
    def all_posibilities(self, grid) -> np.array:
        possibilities = []
        memory = np.array(grid)
        for index_y in range(memory.shape[0]):
            for index_x in range(memory.shape[1]):
                if memory[index_y, index_x] == 0:
                    memory[index_y, index_x] = 2
                    possibilities.append(np.array(memory))
                    memory[index_y, index_x] = 4
                    possibilities.append(np.array(memory))
                    memory[index_y, index_x] = 0
        return np.array(possibilities)
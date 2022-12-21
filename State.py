import numpy as np
import os

class State:

    #-------------------------------------------------------------------------------------------
    #------------------------STATE FUNCTIONS----------------------------------------------------  

    def get_esperances(self, grid) -> list:
        esperances = []

        right = self.roll_right(grid)
        if (right != grid).any(): esperance_right = self.compute_esperance(self.all_posibilities(right))
        esperances.append(esperance_right)

        left = self.roll_left(grid)
        if (left != grid).any(): esperance_left = self.compute_esperance(self.all_posibilities(left))
        esperances.append(esperance_left)

        up = self.roll_up(grid)
        if (up != grid).any(): esperance_up = self.compute_esperance(self.all_posibilities(up))
        esperances.append(esperance_up)

        down = self.roll_down(grid)
        if (down != grid).any(): esperance_down = self.compute_esperance(self.all_posibilities(down))
        esperances.append(esperance_down)
        
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

    # score of a grid
    def policies(self, grid) -> int:
        score = 0
        for row in grid:
            for cell in row:
                if cell != 0:
                    score += np.log(cell)
        return score

    #-------------------------------------------------------------------------------------------
    #------------------------ENGINE FUNCTIONS---------------------------------------------------

    def clear(self): os.system('cls')

    def game_loop(self, grid) -> None:

        command = ""
        while not self.is_game_over(grid) and not self.is_win(grid) and command != "exit":

            self.clear()
            print("----------------------\n\n",grid, "\n\n")
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
                print("----------------------\n\n",grid, "\n\n")
                print("You have lost the game, the higher cell you reached was: ", np.max(grid))
                input("Press any key to continue...\n>> ")
            
            if self.is_win(grid):
                self.clear()
                print("----------------------\n\n",grid, "\n\n")
                print("You won the game !! Good job")
                input("Press any key to continue...\n>> ")
            
            if command == "exit":
                self.clear()
                print("----------------------\n\n",grid, "\n\n")
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
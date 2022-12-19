import numpy as np

class State:

    #-------------------------------------------------------------------------------------------
    #------------------------STATE FUNCTIONS----------------------------------------------------  

    def get_successors(self, grid) -> list:
        succesors = []
        right = self.roll_right(grid)
        print(right)
        succesors.extend(self.all_posibilities(right))
        left = self.roll_left(grid)
        succesors.extend(self.all_posibilities(left))
        up = self.roll_up(grid)
        succesors.extend(self.all_posibilities(up))
        down = self.roll_down(grid)
        succesors.extend(self.all_posibilities(down))
        return succesors

    # score of a grid
    def policies(self, grid) -> int:
        return np.sum(grid)

    def esperance_successors(self, successors) -> int:
        results = np.empty(shape=len(successors))
        for index, successor in enumerate(successors):
            results[index] = self.policies(successor)
        return np.mean(results)

        
    
    #-------------------------------------------------------------------------------------------
    #------------------------ENGINE FUNCTIONS---------------------------------------------------

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
        return possibilities
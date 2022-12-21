import numpy as np

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
        return np.sum(grid)

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
        return np.array(possibilities)
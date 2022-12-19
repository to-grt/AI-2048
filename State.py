import numpy as np

class State:

    def __init__(self) -> None:
        self.grid = np.zeros(shape=(4,4))
    
    def set(self, model) -> None:
        self.grid = model

    #------------------------------------------------------------------------
    #------------------------STATE FUNCTIONS---------------------------------    

    def get_successors(self) -> None:
        succesors = []
        right = self.roll_right()
        left = self.roll_left()
        up = self.roll_up()
        down = self.roll_down()
        succesors.extend([right, left, up, down])
        return succesors
    



    #------------------------------------------------------------------------
    #------------------------ENGINE FUNCTIONS--------------------------------

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

    def roll_left(self) -> np.array:
        resulted_array = np.array(self.grid) # a copy but faster
        for index, row in enumerate(self.grid):
            resulted_array[index] = self.perform_simplification(row)
        return resulted_array

    def roll_right(self) -> np.array:
        resulted_array = np.array(self.grid) # a copy but faster
        for index, row in enumerate(self.grid):
            resulted_array[index] = np.flip(self.perform_simplification(np.flip(row)))
        return resulted_array

    def roll_up(self) -> np.array:
        resulted_array = np.array(self.grid) # a copy but faster
        for index in range(self.grid.shape[1]):
            col = self.grid[:, index]
            resulted_array[:, index] = self.perform_simplification(col)
        return resulted_array

    def roll_down(self) -> np.array:
        resulted_array = np.array(self.grid) # a copy but faster
        for index in range(self.grid.shape[1]):
            col = self.grid[:, index]
            resulted_array[:, index] = np.flip(self.perform_simplification(np.flip(col)))
        return resulted_array    

    # after a mouvement is made, we attribute a value (2 or 4) to a random empty cell
    # this list all of the possibilities
    def all_posibilities(self) -> np.array:

        pass
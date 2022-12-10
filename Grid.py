import random
import numpy as np

class Grid:

    def __init__(self, height, width, prints, nb_cells) -> None:
        self.grid = np.zeros((height, width))
        self.shape = self.grid.shape
        self.prints = prints
        self.set_random_cells(nb_cells)

    def __repr__(self) -> str:
        return str(self.grid)

    def reset(self) -> None:
        self.__init__(self.shape[0], self.shape[1])

    def set(self, model) -> None:
        self.grid = model

    # TODO peut etre optimisé, très long lorsque la grille est presque pleine, a corriger later, modifier la fonction depuis le else
    def set_random_cells(self, nb_cells) -> None:         
        for _ in range(nb_cells):
            if self.prints: print("setting cell number: ", _)
            index_row = np.random.randint(0, self.grid.shape[0])
            index_column = np.random.randint(0, self.grid.shape[1])
            if self.grid[index_row, index_column] == 0:
                random_value = np.random.randint(0, 10)
                if self.prints: print("coords of the cell: ", index_row, ", ", index_column, "\n")
                self.grid[index_row, index_column] = 2 if random_value <= 8 else 4
            else: 
                if self.prints: print("this cell is not empty, restarting...")
                self.set_random_cells(1)

    def perform_simplification(self, row) -> None: #TODO for optimization, numpylize all this
        index_max = row.shape[0]-1
        if self.prints: print("index_max=", index_max, "and row: ", row)
        for index, _cell in enumerate(row):
            if self.prints: print("index=", index, "  and _cell=", _cell)
            # sum part
            if index == index_max:
                if self.prints: print("last index of the array, we don't check the next cell")
            else:   #TODO implement here the following case: [0,2,0,2]
                if row[index] != 0 and row[index] == row[index+1]:
                    row[index] = row[index] * 2
                    row[index+1] = 0
                    if self.prints: print("merging! row[index]= ", row[index], "  and row[index+1]= ", row[index+1])

            # moving part
            if index == 0:
                if self.prints: print("first index of the array, we don't check the previous cells")
            elif row[index] == 0:
                if self.prints: print("the value here is 0, no need to move it anywhere")
            else:
                if self.prints: print("lets try to move it")
                done = False
                moving_index = 1

                while not done and index-moving_index >= 0:
                    if self.prints: print("at this point, row= ", row)
                    if self.prints: print("index= ", index, "moving_index=", moving_index)
                    if row[index-moving_index] == 0:
                        if index-moving_index == 0:
                            if self.prints: print("reached further index, we move to here")
                            done = True
                            break
                        if self.prints: print("value here: ", row[index-moving_index], "can go further, we keep going")
                        moving_index += 1
                        continue
                    else:
                        if self.prints: print("value here: ", row[index-moving_index], "cant go here, going back")
                        moving_index -= 1
                        done = True
                        break
                
                if moving_index != 0:
                    row[index-moving_index] = row[index]
                    row[index] = 0

            # the end ?

    def roll_left(self) -> None:
        for index, row in enumerate(self.grid):
            if self.prints: print("performing simplication on the row number: ", index, "\nrow=  ", row)
            # ici nous n'inversons pas, la foncion perform_simplification est initialement créee pour les roll vers la gauche
            self.perform_simplification(row)
        self.set_random_cells(1)

    def roll_right(self) -> None:
        for index, row in enumerate(self.grid):
            if self.prints: print("performing simplication on the row number: ", index, "\nrow=  ", row)
            # TODO ici nous allons inverser la ligne pour qu'elle soit optimisable

            self.perform_simplification(row)
        self.set_random_cells(1)
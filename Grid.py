import numpy as np

class Grid:

    def __init__(self, height, width, nb_cells, prints=False) -> None:
        self.grid = np.zeros((height, width))
        self.shape = self.grid.shape
        self.prints = prints
        #self.set_random_cells(nb_cells)

    def __repr__(self) -> str:
        return str(self.grid)

    def reset(self) -> None:
        self.__init__(self.shape[0], self.shape[1], 0)

    def set(self, model) -> None:
        assert model.shape == self.grid.shape, "The model and the grid must have the same shapes"
        self.grid = np.copy(model)

    # Maybe its opti...
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

    def perform_simplification(self, row) -> None:
        if np.sum(row) == 0:
            if self.prints: print("null row, skipping")
            return row
        if self.prints: print("initial: ", row)
        initial_shape = row.shape[0]
        row = row[row != 0]
        if self.prints: print("mid: ", row)
        for index in range(row.shape[0]-1):
            if row[index] == row[index+1]:
                row[index] *= 2
                row[index+1] = 0
        if self.prints: print("mid_too: ", row)
        row = row[row != 0]
        row = np.append(row, np.zeros(shape=(initial_shape-row.shape[0])))
        if self.prints: print("final: ", row)
        return row

    def roll_left(self) -> None:
        for index, row in enumerate(self.grid):
            if self.prints: print("performing simplication on the row:")
            # ici nous n'inversons pas, la foncion perform_simplification est initialement créee pour les roll vers la gauche
            self.grid[index] = self.perform_simplification(row)
            if self.prints: print("--------------")

    def roll_right(self) -> None:
        for index, row in enumerate(self.grid):
            if self.prints: print("performing simplication on the row:\ninitial: ", row)
            # ici nous allons inverser la ligne pour qu'elle soit optimisable
            self.grid[index] = np.flip(self.perform_simplification(np.flip(row)))
            if self.prints: print("--------------")

    def roll_up(self) -> None:
        for index in range(self.grid.shape[1]):
            col = self.grid[:, index]
            if self.prints: print("performing simplication on the col number: ", index, "\ninitial: ", col)
            # ici nous n'inversons pas, la foncion perform_simplification est initialement créee pour les roll vers la gauche
            self.grid[:, index] = self.perform_simplification(col)
            if self.prints: print("--------------")

    def roll_down(self) -> None:
        for index in range(self.grid.shape[1]):
            col = self.grid[:, index]
            if self.prints: print("performing simplication on the col number: ", index, "\ninitial: ", col)
            # ici nous n'inversons pas, la foncion perform_simplification est initialement créee pour les roll vers la gauche
            self.grid[:, index] = np.flip(self.perform_simplification(np.flip(col)))
            if self.prints: print("--------------")
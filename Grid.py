from bcolors import bcolors as bc
import numpy as np
import os

class Grid:

    def __init__(self, height, width, prints=False) -> None:
        self.grid = np.zeros((height, width))
        self.shape = self.grid.shape
        self.prints = prints
        self.clear = lambda: os.system('cls')

    def __repr__(self) -> str:
        repr = "\n"
        max_len = len(str(int(np.max(self.grid))))
        for y in range(self.shape[1]):
            for _ in range(max_len*self.shape[0]+5):
                repr += '-'
            repr += '\n'
            for x in range(self.shape[1]):
                value = str(int(self.grid[y,x]))
                repr += '|'
                for _ in range(max_len - len(value)): repr += ' '
                if value == '0': repr += bc.OKGREEN + value + bc.ENDC
                elif int(value) <= 32: repr += bc.FAIL + value + bc.ENDC
                else: repr += bc.OKBLUE + value + bc.ENDC
            repr += '|\n'
        for _ in range(max_len*self.shape[0]+5):
            repr += '-'
        return repr

    def game_loop(self) -> None:
        command = ""
        self.set_random_cells(2)

        while not self.is_game_over() and not self.is_win() and command != "exit":

            self.clear()
            print("----------------------\n\n",self, "\n\n")
            command = input("What do you want to do?\n>> ")
            if command == "up" or command == "z":
                before = self.roll_up()
                if (before != self.grid).any(): self.set_random_cells(1)
            elif command == "down" or command == "s":
                before = self.roll_down()
                if (before != self.grid).any(): self.set_random_cells(1)
            elif command == "left" or command == "q":
                before = self.roll_left()
                if (before != self.grid).any(): self.set_random_cells(1)
            elif command == "right" or command == "d":
                before = self.roll_right()
                if (before != self.grid).any(): self.set_random_cells(1)
            elif command == "exit": pass
            else: input("Command not recognized, press ay key to continue...\n>> ")
            
            if self.is_game_over():
                self.clear()
                print("----------------------\n\n",self, "\n\n")
                print("You have lost the game, the higher cell you reached was: ", np.max(self.grid))
                input("Press any key to continue...\n>> ")
            
            if self.is_win():
                self.clear()
                print("----------------------\n\n",self, "\n\n")
                print("You won the game !! Good job")
                input("Press any key to continue...\n>> ")
            
            if command == "exit":
                self.clear()
                print("----------------------\n\n",self, "\n\n")
                print("You decided to exit the game, we hope to see you soon")
                input("Press any key to continue...\n>> ")
                pass

    def is_game_over(self) -> bool:     #TODO probably optimizable
        memory = self.roll_down()
        if not np.array_equal(self.grid, memory):
            self.set(memory)
            return False
        memory = self.roll_up()
        if not np.array_equal(self.grid, memory):
            self.set(memory)
            return False
        memory = self.roll_left()
        if not np.array_equal(self.grid, memory):
            self.set(memory)
            return False
        memory = self.roll_right()
        if not np.array_equal(self.grid, memory):
            self.set(memory)
            return False    
        return True

    def is_win(self) -> bool:
        if np.max(self.grid) >= 2048: return True
        return False        

    def reset(self) -> None:
        self.__init__(self.shape[0], self.shape[1], 0)

    def set(self, model) -> None:
        assert model.shape == self.grid.shape, "The model and the grid must have the same shapes. model's shape: "
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

    def perform_simplification(self, row):
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

    def roll_left(self) -> bool:
        memory = np.copy(self.grid)
        for index, row in enumerate(self.grid):
            if self.prints: print("performing simplication on the row:")
            # ici nous n'inversons pas, la foncion perform_simplification est initialement créee pour les roll vers la gauche
            self.grid[index] = self.perform_simplification(row)
            if self.prints: print("--------------")
        return memory

    def roll_right(self) -> None:
        memory = np.copy(self.grid)
        for index, row in enumerate(self.grid):
            if self.prints: print("performing simplication on the row:\ninitial: ", row)
            # ici nous allons inverser la ligne pour qu'elle soit optimisable
            self.grid[index] = np.flip(self.perform_simplification(np.flip(row)))
            if self.prints: print("--------------")
        return memory

    def roll_up(self) -> None:
        memory = np.copy(self.grid)
        for index in range(self.grid.shape[1]):
            col = self.grid[:, index]
            if self.prints: print("performing simplication on the col number: ", index, "\ninitial: ", col)
            # ici nous n'inversons pas, la foncion perform_simplification est initialement créee pour les roll vers la gauche
            self.grid[:, index] = self.perform_simplification(col)
            if self.prints: print("--------------")
        return memory

    def roll_down(self) -> None:
        memory = np.copy(self.grid)
        for index in range(self.grid.shape[1]):
            col = self.grid[:, index]
            if self.prints: print("performing simplication on the col number: ", index, "\ninitial: ", col)
            # ici nous n'inversons pas, la foncion perform_simplification est initialement créee pour les roll vers la gauche
            self.grid[:, index] = np.flip(self.perform_simplification(np.flip(col)))
            if self.prints: print("--------------")
        return memory
import sys
import numpy as np
import tkinter as tk
import tkinter.messagebox as messagebox

CELL_PADDING = 10
BACKGROUND_COLOR = '#92877d'
EMPTY_CELL_COLOR = '#9e948a'
CELL_BACKGROUND_COLOR_DICT = {
    '2.0': '#eee4da',
    '4.0': '#ede0c8',
    '8.0': '#f2b179',
    '16.0': '#f59563',
    '32.0': '#f67c5f',
    '64.0': '#f65e3b',
    '128.0': '#edcf72',
    '256.0': '#edcc61',
    '512.0': '#edc850',
    '1024.0': '#edc53f',
    '2048.0': '#edc22e',
    'beyond': '#3c3a32'
}
CELL_COLOR_DICT = {
        '2.0': '#776e65',
        '4.0': '#776e65',
        '8.0': '#f9f6f2',
        '16.0': '#f9f6f2',
        '32.0': '#f9f6f2',
        '64.0': '#f9f6f2',
        '128.0': '#f9f6f2',
        '256.0': '#f9f6f2',
        '512.0': '#f9f6f2',
        '1024.0': '#f9f6f2',
        '2048.0': '#f9f6f2',
        'beyond': '#f9f6f2'
}

FONT = ('Verdana', 24, 'bold')
UP_KEYS = ('w', 'W', 'Up')
LEFT_KEYS = ('a', 'A', 'Left')
DOWN_KEYS = ('s', 'S', 'Down')
RIGHT_KEYS = ('d', 'D', 'Right')

class Grid:

    def __init__(self, n, prints=False):
        self.prints = prints
        self.size = n
        self.grid = np.zeros((n, n))
        self.current_score = 0

        self.root = tk.Tk()
        if sys.platform == 'win32':
            self.root.iconbitmap('2048.ico')
        self.root.title('2048')
        self.root.resizable(False, False)
        self.background = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        self.cell_labels = []
        for i in range(self.size):
            row_labels = []
            for j in range(self.size):
                label = tk.Label(self.background, text='',
                                 bg=EMPTY_CELL_COLOR,
                                 justify=tk.CENTER, font=FONT,
                                 width=4, height=2)
                label.grid(row=i, column=j, padx=10, pady=10)
                row_labels.append(label)
            self.cell_labels.append(row_labels)
        self.background.pack(side=tk.TOP)

        self.over = False
        self.won = False
        self.keep_playing = False

    def game_loop(self) -> None:
        self.set_random_cells(2)
        self.paint()
        self.root.bind('<Key>', self.key_handler)
        self.root.mainloop()

    def key_handler(self, event):
        if self.is_game_terminated():
            return

        key_value = event.keysym
        print('{} key pressed'.format(key_value))
        if key_value in UP_KEYS:
            before = self.roll_up()
            if (before != self.grid).any(): self.set_random_cells(1)
        elif key_value in LEFT_KEYS:
            before = self.roll_left()
            if (before != self.grid).any(): self.set_random_cells(1)
        elif key_value in DOWN_KEYS:
            before = self.roll_down()
            if (before != self.grid).any(): self.set_random_cells(1)
        elif key_value in RIGHT_KEYS:
            before = self.roll_right()
            if (before != self.grid).any(): self.set_random_cells(1)
        else:
            pass

        self.paint()
        print('Score: {}'.format(self.current_score))
        if self.found_2048():
            self.you_win()
            if not self.keep_playing:
                return

        self.paint()
        if not self.can_move():
            self.over = True
            self.game_over()

    def you_win(self):
        if not self.won:
            self.won = True
            print('You Win!')
            if messagebox.askyesno('2048', 'You Win!\n'
                                       'Are you going to continue the 2048 game?'):
                self.keep_playing = True

    def game_over(self):
        print('Game over!')
        messagebox.showinfo('2048', 'Oops!\n'
                                    'Game over!')

    def is_game_terminated(self):
        return self.over or (self.won and (not self.keep_playing))

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
                self.current_score += row[index]
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

    def can_move(self):
        return self.has_empty_cells() or self.can_merge()

    def has_empty_cells(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return True
        return False

    def can_merge(self):
        for i in range(self.size):
            for j in range(self.size - 1):
                if self.grid[i][j] == self.grid[i][j + 1]:
                    return True
        for j in range(self.size):
            for i in range(self.size - 1):
                if self.grid[i][j] == self.grid[i + 1][j]:
                    return True
        return False    

    def found_2048(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] >= 2048:
                    return True
        return False

    def set_random_cells(self, nb_cells) -> None:    
        for _ in range(nb_cells):
            index_row = np.random.randint(0, self.grid.shape[0])
            index_column = np.random.randint(0, self.grid.shape[1])
            if self.grid[index_row, index_column] == 0:
                random_value = np.random.randint(0, 10)
                self.grid[index_row, index_column] = 2 if random_value <= 8 else 4
            else: 
                self.set_random_cells(1)

    '''The GUI view class of the 2048 game showing via tkinter.'''

    def paint(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    self.cell_labels[i][j].configure(
                         text='',
                         bg=EMPTY_CELL_COLOR)
                else:
                    cell_text = str(self.grid[i][j])
                    if self.grid[i][j] > 2048:
                        bg_color = CELL_BACKGROUND_COLOR_DICT.get('beyond')
                        fg_color = CELL_COLOR_DICT.get('beyond')
                    else:
                        bg_color = CELL_BACKGROUND_COLOR_DICT.get(cell_text)
                        fg_color = CELL_COLOR_DICT.get(cell_text)
                    self.cell_labels[i][j].configure(
                        text=cell_text,
                        bg=bg_color, fg=fg_color)



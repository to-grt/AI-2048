from Test import Test
from Grid import Grid
import time
import numpy as np
import os

testeur = Test()
del testeur

input("Press any key to continue...\n>> ")


clear = lambda: os.system('cls')
command = ""
game = Grid(4,4)
game.set_random_cells(2)

while not game.is_game_over() and not game.is_win() and command != "exit":

    clear()
    print("----------------------\n\n",game, "\n\n")
    command = input("What do you want to do?\n>> ")
    match command:
        case "up":
            before = game.roll_up()
            if (before != game.grid).any(): game.set_random_cells(1)
        case "down":
            before = game.roll_down()
            if (before != game.grid).any(): game.set_random_cells(1)
        case "left":
            before = game.roll_left()
            if (before != game.grid).any(): game.set_random_cells(1)
        case "right":
            before = game.roll_right()
            if (before != game.grid).any(): game.set_random_cells(1)
        case "exit": pass
        case other: input("Command not recognized, press ay key to continue...\n>> ")
    
    if game.is_game_over():
        clear()
        print("----------------------\n\n",game, "\n\n")
        print("You have lost the game, the higher cell you reached was: ", np.max(game.grid))
        input("Press any key to continue...\n>> ")
    
    if game.is_win():
        clear()
        print("----------------------\n\n",game, "\n\n")
        print("You won the game !! Good job")
        input("Press any key to continue...\n>> ")
    
    if command == "exit":
        clear()
        print("----------------------\n\n",game, "\n\n")
        print("You decided to exit the game, we hope to see you soon")
        input("Press any key to continue...\n>> ")
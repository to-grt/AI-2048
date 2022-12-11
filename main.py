from Test import Test
from Grid import Grid
import time
import numpy as np

testeur = Test()
del testeur

game = Grid(4,4)
model = np.array([[0,0,0,0],
                  [0,0,0,0],
                  [0,0,0,0],
                  [0,0,0,0]])
game.set(model)

print(game)
print(game.is_game_over())
print(game.is_win())

model = np.array([[5000,0,0,0],
                  [0,0,0,5000],
                  [0,0,5000,0],
                  [0,5000,0,0]])
game.set(model)

print(game)
print(game.is_game_over())
print(game.is_win())

model = np.array([[1,1,1,1],
                  [1,1,1,1],
                  [1,1,1,1],
                  [1,1,1,1]])
game.set(model)

print(game)
print(game.is_game_over())
print(game.is_win())
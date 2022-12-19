from Test import Test
from State import State
import numpy as np

game = State()
game.set(np.array([[0,0,0,0], [0,0,1,0], [0,1,0,0], [0,0,0,0]]))
print(game.get_successors())
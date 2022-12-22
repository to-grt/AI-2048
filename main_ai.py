from State import State
import numpy as np

game = State()
state = game.set_random_cells(np.array([[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]), 2)

game.ai_loop(state)


 
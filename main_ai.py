from State import State
import numpy as np

game = State()
state = np.array([[0,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16]])

game.game_loop(state)



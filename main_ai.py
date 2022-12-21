from State import State
import numpy as np

def game_loop():
    pass

game = State()
state = np.array([[0,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16]])
"""
esp = game.get_esperances(state)
print("esperances: ", esp)
"""

game.game_loop(state)



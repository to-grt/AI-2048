from State import State
import numpy as np

game = State()
state = np.array([[0,0,0,0], [0,0,1,0], [0,1,0,0], [0,0,0,0]])
esp = game.get_esperances(state)
print("esperances: ", esp)

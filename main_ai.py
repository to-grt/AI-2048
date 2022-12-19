from State import State
import numpy as np

game = State()
state = np.array([[0,0,0,0], [0,0,1,0], [0,1,0,0], [0,0,0,0]])
successors = game.get_successors(state)

for index, successor in enumerate(successors):
    print("child n°:", index, "    score: ", game.policies(successor))

print("final_res = ", game.esperance_successors(successors))

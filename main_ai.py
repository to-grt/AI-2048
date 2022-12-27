from State import State
import numpy as np


"""
game = State()
state = game.set_random_cells(np.array([[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]), 2)
#state = game.set_random_cells(np.array([[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]]), 2)

best_result = [0, (0,0,0,0)]
results = np.zeros(shape=(30,))
coefs = [0.5, 1, 1.5]

for c_0 in coefs:
    for c_1 in coefs:
        for c_2 in coefs:
            for c_3 in coefs:
                coefficients = (c_0, c_1, c_2, c_3)
                print("coefficients: ", coefficients)
                if c_0 == c_1 and c_0 == c_2 and c_0 == c_3:
                    print("    skip")
                    continue
                for index in range(results.shape[0]):
                    results[index] = game.ai_loop(np.array(state), coefficients)
                    print("    iteration number", index+1, " is done, result: ", results[index])
                print('results: ', results)
                mean = np.mean(results)
                print("mean of results: ", mean)
                if mean > best_result[0]:
                    best_result = [mean, coefficients]
                    print("new best result")
"""



game = State(prints=True)
state = game.set_random_cells(np.array([[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]), 2)

game.ai_loop(state)
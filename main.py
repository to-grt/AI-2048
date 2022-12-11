from Test import Test
from Grid import Grid
import time
import numpy as np

testeur = Test()
del testeur

game = Grid(4,4,2)
model = np.array([[0,0,0,0],
                  [0,0,0,0],
                  [0,0,0,0],
                  [0,0,0,0]])

start = time.time()
for _ in range(10000):
    game.reset()
    game.set(model)
    game.set_random_cells_1(1)
end = time.time()
print(end - start)

start = time.time()  
for _ in range(10000):
    game.reset()
    game.set(model)
    game.set_random_cells_2(1)
end = time.time()
print(end - start)

start = time.time()  
for _ in range(10000):
    game.reset()
    game.set(model)
    game.set_random_cells_3(1)
end = time.time()
print(end - start)
from Test import Test
from Grid import Grid

testeur = Test()
del testeur

input("Press any key to continue...\n>> ")

game = Grid(4,4)
game.game_loop()
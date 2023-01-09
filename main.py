from Grid import Grid

quit_input = {"quit", "exit", "q", "Q", "Quit", "exit"}
keyboard_input = {"AZERTY", "azerty", "QWERTY", "qwerty"}
global_input = ""

while global_input not in quit_input:
    global_input = input("""Select your keyboard input style :
    (azerty or qwerty)\n""")
    if global_input in keyboard_input:
        game = Grid(4, global_input)
        game.game_loop()
    if global_input in quit_input:
        print("See you soon !")
    else:
        print("""Select a correct input""")

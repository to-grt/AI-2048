import numpy as np
from Grid import Grid


class Test:

    def __init__(self) -> None:
        self.test_set()
        self.test_simpl()
        self.test_roll_down()
        self.test_roll_up()
        self.test_roll_left()
        self.test_roll_right()
        print("\n\nend of the tests - good to go\n------------------\n\n")

    def test_set(self) -> None:
        print("----------------------\ngrid.set tests:\n")

        grid = Grid(4,4,2)
        model = np.array([[0,1,2,3],
                          [4,5,6,7],
                          [8,9,10,11],
                          [12,13,14,15]])
        grid.set(model)
        assert (grid.grid == np.array([[0,1,2,3], [4,5,6,7], [8,9,10,11], [12,13,14,15]])).all(), ">> test 1: FAILED"
        print(">> test 1: SUCCESS")

        grid = Grid(6,6,25)
        model = np.array([[0,1,2,3,0,0],
                          [4,5,6,7,0,0],
                          [8,9,10,11,0,0],
                          [12,13,14,15,0,0],
                          [0,0,0,0,0,0],
                          [0,0,0,0,0,0]])
        grid.set(model)
        assert (grid.grid == np.array([[0,1,2,3,0,0], [4,5,6,7,0,0], [8,9,10,11,0,0], [12,13,14,15,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0]])).all(), ">> test 2: FAILED"
        print(">> test 2: SUCCESS")


    def test_roll_left(self) -> None:
        print("----------------------\nroll_left tests:\n")

        grid = Grid(4,4,2)
        model = np.array([[0,0,0,100],
                          [0,2,2,0],
                          [2,0,0,2],
                          [2,0,0,0]])
        grid.set(model)
        grid.roll_left()
        assert (grid.grid == np.array([[100,0,0,0], [4,0,0,0], [4,0,0,0], [2,0,0,0]])).all(), ">> test 1: FAILED"
        print(">> test 1: SUCCESS")

        model = np.array([[100,0,100,100],
                          [2,2,2,2],
                          [0,0,500,500],
                          [0,0,0,0]])
        grid.set(model)
        grid.roll_left()
        assert (grid.grid == np.array([[200,100,0,0], [4,4,0,0], [1000,0,0,0], [0,0,0,0]])).all(), ">> test 2: FAILED"
        print(">> test 2: SUCCESS")


    def test_roll_right(self) -> None:
        print("----------------------\nroll_right tests:\n")

        grid = Grid(4,4,2)
        model = np.array([[0,0,0,100],
                          [0,2,2,0],
                          [2,0,0,2],
                          [2,0,0,0]])
        grid.set(model)
        grid.roll_right()
        assert (grid.grid == np.array([[0,0,0,100], [0,0,0,4], [0,0,0,4], [0,0,0,2]])).all(), ">> test 1: FAILED"
        print(">> test 1: SUCCESS")

        model = np.array([[100,0,100,100],
                          [2,2,2,2],
                          [0,0,500,500],
                          [0,0,0,0]])
        grid.set(model)
        grid.roll_right()
        assert (grid.grid == np.array([[0,0,100,200], [0,0,4,4], [0,0,0,1000], [0,0,0,0]])).all(), ">> test 2: FAILED"
        print(">> test 2: SUCCESS")

    def test_roll_up(self) -> None:
        print("----------------------\nroll_up tests:\n")

        grid = Grid(4,4,2)
        model = np.array([[0,0,0,100],
                          [0,2,2,0],
                          [2,0,0,2],
                          [2,0,0,0]])
        grid.set(model)
        grid.roll_up()
        assert (grid.grid == np.array([[4,2,2,100], [0,0,0,2], [0,0,0,0], [0,0,0,0]])).all(), ">> test 1: FAILED"
        print(">> test 1: SUCCESS")

        model = np.array([[100,0,100,100],
                          [2,2,2,2],
                          [0,0,500,500],
                          [0,0,0,0]])
        grid.set(model)
        grid.roll_up()
        assert (grid.grid == np.array([[100,2,100,100], [2,0,2,2], [0,0,500,500], [0,0,0,0]])).all(), ">> test 2: FAILED"
        print(">> test 2: SUCCESS")


    def test_roll_down(self) -> None:
        print("----------------------\nroll_down tests:\n")

        grid = Grid(4,4,2)
        model = np.array([[0,0,0,100],
                          [0,2,2,0],
                          [2,0,0,2],
                          [2,0,0,0]])
        grid.set(model)
        grid.roll_down()
        assert (grid.grid == np.array([[0,0,0,0], [0,0,0,0], [0,0,0,100], [4,2,2,2]])).all(), ">> test 1: FAILED"
        print(">> test 1: SUCCESS")

        model = np.array([[100,0,100,100],
                          [2,2,2,2],
                          [0,0,500,500],
                          [0,0,0,0]])
        grid.set(model)
        grid.roll_down()
        assert (grid.grid == np.array([[0,0,0,0], [0,0,100,100], [100,0,2,2], [2,2,500,500]])).all(), ">> test 2: FAILED"
        print(">> test 2: SUCCESS")


    def test_simpl(self) -> None:
        print("----------------------\nperform_simplification tests:\n")

        shape = (6, 6)
        grid = Grid(height=shape[0], width=shape[1], nb_cells=5)

        initial_array = [0,0,0,0,0]
        expected_result = [0,0,0,0,0]
        assert (grid.perform_simplification(np.array(initial_array)) == expected_result).all(), ">> test 1: FAILED"
        print(">> test 1: SUCCESS")
        
        initial_array = [1,1,1,1]
        expected_result = [2,2,0,0]
        assert (grid.perform_simplification(np.array(initial_array)) == expected_result).all(), ">> test 2: FAILED"
        print(">> test 2: SUCCESS")
        
        initial_array = [0,1,0,0,1]
        expected_result = [2,0,0,0,0]
        assert (grid.perform_simplification(np.array(initial_array)) == expected_result).all(), ">> test 3: FAILED"
        print(">> test 3: SUCCESS")
        
        initial_array = [16,16,16,0,16]
        expected_result = [32,32,0,0,0]
        assert (grid.perform_simplification(np.array(initial_array)) == expected_result).all(), ">> test 4: FAILED"
        print(">> test 4: SUCCESS")
        
        initial_array = [1,2,3,4,6]
        expected_result = [1,2,3,4,6]
        assert (grid.perform_simplification(np.array(initial_array)) == expected_result).all(), ">> test 5: FAILED"
        print(">> test 5: SUCCESS")

        initial_array = [4096,4096,4096,4096,4096]
        expected_result = [8192,8192,4096,0,0]
        assert (grid.perform_simplification(np.array(initial_array)) == expected_result).all(), ">> test 6: FAILED"
        print(">> test 6: SUCCESS")
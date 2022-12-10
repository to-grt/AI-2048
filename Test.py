import numpy as np
from Grid import Grid


class Test:

    def test_simpl(self):

        print("----------------------\nperform_simplification tests:\n")

        shape = (6, 6)
        grid = Grid(height=shape[0], width=shape[1], prints=False, nb_cells=5)

        initial_array = [0,0,0,0,0]
        expected_result = [0,0,0,0,0]
        assert (grid.perform_simplification(np.array(initial_array)) == expected_result).any(), ">> test 1: FAILED"
        print(">> test 1: SUCCESS")
        
        initial_array = [1,1,1,1]
        expected_result = [2,2,0,0]
        assert (grid.perform_simplification(np.array(initial_array)) == expected_result).any(), ">> test 2: FAILED"
        print(">> test 2: SUCCESS")
        
        initial_array = [0,1,0,0,1]
        expected_result = [2,0,0,0,0]
        assert (grid.perform_simplification(np.array(initial_array)) == expected_result).any(), ">> test 3: FAILED"
        print(">> test 3: SUCCESS")
        
        initial_array = [16,16,16,0,16]
        expected_result = [32,32,0,0,0]
        assert (grid.perform_simplification(np.array(initial_array)) == expected_result).any(), ">> test 4: FAILED"
        print(">> test 4: SUCCESS")
        
        initial_array = [1,2,3,4,6]
        expected_result = [1,2,3,4,6]
        assert (grid.perform_simplification(np.array(initial_array)) == expected_result).any(), ">> test 5: FAILED"
        print(">> test 5: SUCCESS")
        
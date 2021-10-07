from algorithm.planner.utils.angles import Angle

# Test
# x,y lies in [0, 20]
class TestSet:

    # Test - side by side obstacle
    # obstacles = [[6,6,Angle.NINETY_DEG], 
    # [7,6,Angle.NINETY_DEG], 
    # [7,15,Angle.TWO_SEVENTY_DEG],
    # [3,11,Angle.ZERO_DEG]]

    # obstacles = [ 
    # [7,6,Angle.NINETY_DEG], 
    # [7,14,Angle.TWO_SEVENTY_DEG]]

    # Test - obstacle facing each other
    # obstacles = [[6,6,Angle.NINETY_DEG], 
    # [6,12,Angle.TWO_SEVENTY_DEG]]

    # Test - single obstacle for checking turning radius
    # obstacles = [[7,6,Angle.ONE_EIGHTY_DEG]]


    # Test - obstacle staggered
    # obstacles = [[6,6,Angle.NINETY_DEG], 
    # [7,7,Angle.NINETY_DEG]]

    # Test - more obstacles staggered
    # obstacles = [[6,6,Angle.NINETY_DEG], 
    # [7,7,Angle.NINETY_DEG],
    # [8,8, Angle.NINETY_DEG],
    # [9,9, Angle.NINETY_DEG],
    # [10,10, Angle.NINETY_DEG]]

    # Test 0.1
    obstacles = [[2,12,Angle.NINETY_DEG],
    [6,6,Angle.TWO_SEVENTY_DEG],
    [11,11, Angle.NINETY_DEG],
    [18,18, Angle.TWO_SEVENTY_DEG],
    [15,2,Angle.ONE_EIGHTY_DEG]]

    # Test 0.15
    # obstacles = [[2,12,Angle.NINETY_DEG],
    # [6,6,Angle.NINETY_DEG],
    # [8,13, Angle.NINETY_DEG],
    # [19,16, Angle.TWO_SEVENTY_DEG],
    # [19,0, Angle.ONE_EIGHTY_DEG]]
 
    # Test 0.2 - test invalid
    # obstacles = [[2,12,Angle.NINETY_DEG],
    # [7,3,Angle.NINETY_DEG],
    # [10,19, Angle.TWO_SEVENTY_DEG],
    # [17,17,Angle.ZERO_DEG],
    # [5,7, Angle.ONE_EIGHTY_DEG],
    # [4,18,Angle.ZERO_DEG]]

    # Test 1
    # obstacles = [[16, 15, Angle.ONE_EIGHTY_DEG],
    # [10, 8, Angle.ZERO_DEG],
    # [9, 17, Angle.TWO_SEVENTY_DEG],
    # [9, 12, Angle.ONE_EIGHTY_DEG],
    # [10, 4, Angle.ZERO_DEG]]

    # Test 2
    # obstacles = [[2, 10, Angle.TWO_SEVENTY_DEG],
    # [2, 17, Angle.ZERO_DEG],
    # [9, 17, Angle.TWO_SEVENTY_DEG],
    # [9, 12, Angle.ONE_EIGHTY_DEG],
    # [19, 5, Angle.ONE_EIGHTY_DEG]]


    # Test 3
    # obstacles = [[5, 7, Angle.TWO_SEVENTY_DEG],
    # [10, 14, Angle.TWO_SEVENTY_DEG],
    # [15, 11, Angle.ZERO_DEG],
    # [5, 11, Angle.NINETY_DEG],
    # [10, 11, Angle.NINETY_DEG]]


    # Test 4
    # obstacles = [[10,0,Angle.ONE_EIGHTY_DEG],
    # [10,5,Angle.ONE_EIGHTY_DEG],
    # [10,10,Angle.ONE_EIGHTY_DEG],
    # [10,15,Angle.ONE_EIGHTY_DEG],
    # [10,20,Angle.ONE_EIGHTY_DEG]]


    # Test 5
    # obstacles = [[16, 15, Angle.ONE_EIGHTY_DEG],
    # [9, 8, Angle.ZERO_DEG],
    # [9, 15, Angle.TWO_SEVENTY_DEG],
    # [17, 12, Angle.ONE_EIGHTY_DEG],
    # [14, 16, Angle.ZERO_DEG]]

    # Test 6
    # obstacles = [[10,0,Angle.ZERO_DEG],
    # [10,5,Angle.ONE_EIGHTY_DEG],
    # [10,10,Angle.ZERO_DEG],
    # [10,15,Angle.ONE_EIGHTY_DEG],
    # [10,20,Angle.ZERO_DEG]]

    # Test 7
    # obstacles = [[5,10,Angle.ZERO_DEG],
    # [5,12,Angle.ONE_EIGHTY_DEG],
    # [6,12,Angle.NINETY_DEG],
    # [9,14,Angle.NINETY_DEG],
    # [12,7,Angle.NINETY_DEG]]

    # Test 8
    # obstacles = [[5,10,Angle.ZERO_DEG],
    # [5,12,Angle.ONE_EIGHTY_DEG],
    # [6,12,Angle.NINETY_DEG],
    # [9,14,Angle.NINETY_DEG],
    # [12,7,Angle.NINETY_DEG],
    # [18,18,Angle.ONE_EIGHTY_DEG],
    # [18, 13, Angle.ONE_EIGHTY_DEG],
    # [0,19,Angle.ONE_EIGHTY_DEG]]

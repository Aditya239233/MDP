from utils.angles import Angle

# Test
# x,y lies in [0, 20]
class TestSet:

    # Test 1
    obstacles = [[16, 15, Angle.ONE_EIGHTY_DEG],
    [10, 8, Angle.ZERO_DEG],
    [9, 17, Angle.TWO_SEVENTY_DEG],
    [9, 12, Angle.ONE_EIGHTY_DEG],
    [10, 4, Angle.ZERO_DEG]]

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
    # obstacles = [[10,4,Angle.ONE_EIGHTY_DEG],
    # [10,8,Angle.ONE_EIGHTY_DEG],
    # [10,12,Angle.ONE_EIGHTY_DEG],
    # [10,15,Angle.ONE_EIGHTY_DEG],
    # [10,18,Angle.ONE_EIGHTY_DEG]]


    # Test 5
    # obstacles = [[16, 15, Angle.ONE_EIGHTY_DEG],
    # [9, 8, Angle.ZERO_DEG],
    # [9, 15, Angle.TWO_SEVENTY_DEG],
    # [17, 12, Angle.ONE_EIGHTY_DEG],
    # [14, 16, Angle.ZERO_DEG]]

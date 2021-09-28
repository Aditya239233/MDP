from algorithm.planner.utils.angles import Angle
from algorithm.planner.utils.arena_utils import Arena_C

class Car_C:
    RF = 5.0  # [m] distance from rear wheel to vehicle front end of vehicle
    ACTUAL_RF = 3.6
    RB = 1.5  # [m] distance from rear wheel to vehicle back end of vehicle
    ACTUAL_RB = 0.4
    
    ACTUAL_CAR_LENGTH = ACTUAL_RB + ACTUAL_RF
    W = 4.0  # [m] width of vehicle (For more allowance?)
    WD = 4.0  # [m] distance between left-right wheels (3.5)
    WB = 3.0  # [m] Wheel base
    TR = 0.4  # [m] Tyre radius
    TW = 0.4  # [m] Tyre width
    MAX_STEER = 0.625  # [rad] maximum steering angle

    TOL_SPACE = 6.0  # camera space


    START_POS = 1, 1, Angle.NINETY_DEG # Default starting pos    

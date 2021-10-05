from algorithm.planner.utils.angles import Angle
from algorithm.planner.utils.arena_utils import Arena_C

class Car_C:
    RF = 4.5  # [m] distance from rear wheel to vehicle front end of vehicle (5.0)
    ACTUAL_RF = 3.6
    RB = 2.0  # [m] distance from rear wheel to vehicle back end of vehicle (1.5)
    ACTUAL_RB = 0.6
    
    ACTUAL_CAR_LENGTH = ACTUAL_RB + ACTUAL_RF
    W = 5.0  # [m] width of vehicle (For more allowance?)
    WD = 3.0  # [m] distance between left-right wheels (3.5)
    WB = 2.8  # [m] Wheel base (3.0)
    TR = 0.6  # [m] Tyre radius (3.0cm)
    TW = 0.5  # [m] Tyre width (2.6cm)
    MAX_STEER = 0.6  # [rad] maximum steering angle

    TOL_SPACE = 7.6  # camera space - 38 cm from face to back axle

    START_POS = 1, 1, Angle.NINETY_DEG # Default starting pos    

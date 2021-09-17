import numpy as np
import math


class Angle:
    ZERO_DEG = np.deg2rad(0.0)
    NINETY_DEG = np.deg2rad(90.0)
    ONE_EIGHTY_DEG = np.deg2rad(180.0)
    TWO_SEVENTY_DEG = np.deg2rad(270.0)
    THREE_SIXTY_DEG = 2 * ONE_EIGHTY_DEG

# Scale of 1 : 0.2

class C:  # Parameter config
    PI = math.pi

    XY_RESO = 0.5  # [m] (1.0)
    YAW_RESO = np.deg2rad(15.0)  # [rad] (15deg)
    MOVE_STEP = 0.5   # [m] path interporate resolution (0.5)
    N_STEER = 20.0  # steer command number
    COLLISION_CHECK_STEP = 5  # skip number for collision check
    # EXTEND_BOUND = 1  # collision check range extended

    GEAR_COST = 1.0  # switch back penalty cost
    BACKWARD_COST = 1.0  # backward penalty cost (5.0)
    STEER_CHANGE_COST = 10.0  # steer angle change penalty cost (5.0)
    STEER_ANGLE_COST = 100.0  # steer angle penalty cost (1.0)
    H_COST = 1.0  # Heuristic cost penalty cost (15.0)

    RF = 5.0  # [m] distance from rear wheel to vehicle front end of vehicle
    ACTUAL_RF = 3.6
    RB = 1.5  # [m] distance from rear wheel to vehicle back end of vehicle
    ACTUAL_RB = 0.4
    W = 4.0  # [m] width of vehicle (For more allowance?)
    WD = 4.0  # [m] distance between left-right wheels (3.5)
    WB = 3.0  # [m] Wheel base
    TR = 0.4  # [m] Tyre radius
    TW = 0.4  # [m] Tyre width
    MAX_STEER = 0.6  # [rad] maximum steering angle

    #CAR_START_POS = (30.0, 27.5, Angle.NINETY_DEG) 
    CAR_START_POS = (3.0, 2.0, Angle.NINETY_DEG)
    ACTUAL_CAR_LENGTH = 4.0
    X, Y = 40, 40
    OBS_LENGTH = 2
    TOL_SPACE = 4.5 + ACTUAL_CAR_LENGTH/2  # camera space

def increment_id(tag):
    if tag == "error":
        filename = "errorarena"
    elif tag == "valid":
        filename = "validarena"
    elif tag == "gif":
        filename = "gif"


    file = open(f"./results/id/{filename}.txt","r")
    id_line = file.readline()
    file.close()

    curr_id = int(id_line.strip())
    file = open(f"./results/id/{filename}.txt","w")
    file.write(f"{curr_id+1}")
    file.close()
    
    return curr_id
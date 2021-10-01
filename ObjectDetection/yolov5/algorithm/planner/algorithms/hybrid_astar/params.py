import numpy as np
import math

# Scale of 1 : 0.2

class C:  # Parameter config for algorithm
    PI = math.pi

    XY_RESO = 0.5 # [m] (1.0)/(0.5)
    YAW_RESO = np.deg2rad(1.0)  # [rad] (15deg)
    MOVE_STEP = 0.05   # [m] path interporate resolution (0.1) - for better instruction generation due to more granular coors
    N_STEER = 1.0  # steer command number
    COLLISION_CHECK_STEP = 5  # skip number for collision check
    # EXTEND_BOUND = 1  # collision check range extended

    GEAR_COST = 1.0  # switch back penalty cost
    BACKWARD_COST = 1.0  # backward penalty cost (5.0)
    STEER_CHANGE_COST = 10.0  # steer angle change penalty cost (5.0)
    STEER_ANGLE_COST = 100.0  # steer angle penalty cost (1.0)
    H_COST = 1.0  # Heuristic cost penalty cost (15.0)
from algorithm.planner.utils.angles import Angle
from algorithm.planner.utils.arena_utils import Arena_C
import math

def get_angle_from_direction(direction):
    if direction == "N":
        return Angle.NINETY_DEG
    elif direction == "S":
        return Angle.TWO_SEVENTY_DEG
    elif direction == "W":
        return Angle.ONE_EIGHTY_DEG
    elif direction == "E":
        return Angle.ZERO_DEG

# only handles the 90n deg, n= [0,1,2,3]
def get_direction_from_angle(angle):
    if math.isclose(angle, Angle.ZERO_DEG):
        return "E"
    elif math.isclose(angle, Angle.NINETY_DEG):
        return "N"
    elif math.isclose(angle, Angle.ONE_EIGHTY_DEG):
        return "W"
    elif math.isclose(angle, Angle.TWO_SEVENTY_DEG):
        return "S"
    else:
        return "Invalid"

def convert_val_to_sim(val):
    return (val * Arena_C.SCALE) + Arena_C.OFFSET

def convert_sim_to_val(sim):
    return (sim - Arena_C.OFFSET) / Arena_C.SCALE
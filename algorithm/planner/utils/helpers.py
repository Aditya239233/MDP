from .angles import Angle
from utils.arena_utils import Arena_C

def get_angle_from_direction(direction):
    if direction == "N":
        return Angle.NINETY_DEG
    elif direction == "S":
        return Angle.TWO_SEVENTY_DEG
    elif direction == "E":
        return Angle.ONE_EIGHTY_DEG
    elif direction == "W":
        return Angle.ZERO_DEG

from algorithm.planner.utils.helpers import convert_sim_to_val
import math

from numpy import add
from algorithm.planner.entity.path import Path

SPEED = 0.01 #unit/ms
ROT_TIME = 891.2676813 #ms/rad
TWO_PI = 2 * math.pi

# Check the longest sequence for:
# 1. Rotation - rotation has a different motion from straight-line
# 2. Straight line motion
# wXXXX - move forward for XXXXms
# dXXXX - move backward for XXXXms
# afXXXX - turn left forward for XXXXms
# arXXXX - turn left reverse for XXXXms
# dfXXXX - turn right forward for XXXXms
# drXXXX - turn right reverse for XXXXms

# for i in range(len(path.x)):
#     print(f"{path.x[i]}, {path.y[i]}, {path.direction[i]}, {path.yaw[i]}, {path.steer[i]}")

def is_turning(steer):
    return not math.isclose(abs(steer), 0)

def calculate_dist(straight):
    dy = straight[-1][1] - straight[0][1]
    dx = straight[-1][0] - straight[0][0]

    return math.sqrt(dx*dx + dy*dy)

def same_sign(x, y):
    return x * y > 0

def calculate_turning_time(start_angle, end_angle, steer):
    if not same_sign(start_angle, end_angle):
        end_angle -= 2 * math.pi

    return int(abs(end_angle-start_angle) * ROT_TIME)

def get_car_motion(direction, steer):

    motion = ""

    if direction == 1:
        motion = "w"
        if steer < 0:
            motion = "af"
        elif steer > 0:
            motion = "df"

    elif direction == -1:
        motion = "s"
        if steer < 0:
            motion = "ar"
        elif steer > 0:
            motion = "dr"
    
    return motion


def get_angle(motion, section):
    if motion == "df" or motion == "ar": # in clockwise direction - angle should decrease
        start_angle = prev_angle = section[0][3]
        for i in range(1, len(section)):
            curr_angle = section[i][3]
            if curr_angle - prev_angle > math.pi:  # more relaxed checking - only detects entrance of 1st/4th quadrant
                curr_angle -= TWO_PI

            prev_angle = curr_angle

        end_angle = curr_angle

    elif motion == "dr" or motion == "af": # in anticlockwise direction - angle should increase
        start_angle = prev_angle = section[0][3]
        for i in range(1, len(section)):
            curr_angle = section[i][3]
            if curr_angle - prev_angle < -math.pi:
                curr_angle += TWO_PI

            prev_angle = curr_angle

        end_angle = curr_angle


    return abs(end_angle - start_angle)


def get_instruction(section):
    direction = section[0][2]
    steer = section[0][4]
    motion = get_car_motion(direction, steer)

    if motion == "w" or motion == "s":
        dist = calculate_dist(section)
        dt = dist / SPEED
        return f"{motion}{dt :04.0f}"
    else:
        angle = get_angle(motion, section)
        dt = angle * ROT_TIME
        return f"{motion}{dt :04.0f}"

# Some yaw are negative, so convert those positive
def get_base_angle(angle):
    if angle >= 0 and angle < TWO_PI:
        return angle
    
    while angle >= TWO_PI:
        angle -= TWO_PI
    
    while angle < 0:
        angle += TWO_PI
    
    return angle


def check_and_fix_anomalies(path):
    # Sometimes, the sign of steer will be wrong - can detect through a window of size 3 on the yaw value

    for i in range(0, len(path.x)-1):
        path.yaw[i] = get_base_angle(path.yaw[i])


    # # if the yaw is changing, then steer should be non-zero
    for i in range(1, len(path.x)):
        curr_yaw = path.yaw[i]
        last_yaw = path.yaw[i-1]
        if not math.isclose(curr_yaw, last_yaw):
            if path.direction[i] > 0:
                if curr_yaw < last_yaw:
                    path.steer[i] = 0.625
                else:
                    path.steer[i] = -0.625
            else:
                if curr_yaw < last_yaw:
                    path.steer[i] = -0.625
                else:
                    path.steer[i] = 0.625

    # check for anomalies in steer (-ve +ve -ve or +ve -ve +ve)
    for i in range(1, len(path.x)-1):
        if same_sign(path.steer[i-1], path.steer[i+1]) and not same_sign(path.steer[i], path.steer[i+1]):
            path.steer[i] *= -1


def translate(path):

    pos_after_instruction = []
    instructions = []
    curr_section = []

    check_and_fix_anomalies(path)


    x, y, direction, yaw, steer = path.x[0], path.y[0], path.direction[0], path.yaw[0], path.steer[0]
    prev_motion = get_car_motion(direction, steer)
    curr_section.append((x, y, direction, yaw, steer))

    for i in range(1, len(path.x)):
        curr_x, curr_y, curr_direction, curr_yaw, curr_steer = path.x[i], path.y[i], path.direction[i], path.yaw[i], path.steer[i]
        val = (curr_x, curr_y, curr_direction, curr_yaw, curr_steer)
        
        curr_motion = get_car_motion(curr_direction, curr_steer)

        if curr_motion != prev_motion:
            curr_section.append(val)
            curr_instruction = get_instruction(curr_section)
            instructions.append(curr_instruction)

            pos_after_instruction.append((curr_x, curr_y, curr_yaw))

            curr_section = [val]
        else:
            curr_section.append(val)
        
        prev_motion = curr_motion
    
    if curr_section:
        curr_instruction = get_instruction(curr_section)
        instructions.append(curr_instruction)
        pos_after_instruction.append((curr_x, curr_y, curr_yaw))
    

    return instructions, pos_after_instruction

def process_android_coor(coors):
    new_list = []

    for coor in coors:
        x, y, yaw = coor
        x = convert_sim_to_val(x)
        y = convert_sim_to_val(y)
        new_list.append((x, y, yaw))

    return new_list

def translate_tour(tour, tour_seq):
    list_of_instructions = []
    list_of_coor = []
    tour_seq = tour_seq[1:]  # remove the starting pos - labelled as -1
    i = 0

    for path in tour:
        instructions, android_coor = translate(path)
        android_coor = process_android_coor(android_coor)

        instructions.append(f"C{tour_seq[i]}")  # car stop and do image recognition

        list_of_instructions.append(instructions)
        list_of_coor.append(android_coor)

        i += 1

    return list_of_instructions, list_of_coor




# UNUSED
# detect a trend of negative to positive values
# def neg_to_pos(section):
#     pos = False

#     # check if first part is negative
#     if not (section[0][3] < 0):
#         return False
    
#     # find the part with positive values
#     for i in range(1, len(section)):
#         if section[i][3] >= 0:
#             pos = True
#             break
    
#     return pos

# # detect a trend of positive to negative values
# def pos_to_neg(section):
#     neg = False

#     # check if first part is positive
#     if not (section[0][3] >= 0):
#         return False
    
#     # find the part with negative values
#     for i in range(1, len(section)):
#         if section[i][3] < 0:
#             neg = True
#             break
    
#     return neg

# # detect a trend of positive to negative to positive values
# def pos_to_neg_to_pos(section):
#     pos = False
#     neg_index = 1

#     if not (section[0][3] >= 0):
#         return False
    
#     while neg_index < len(section) and section[neg_index][3] >= 0:
#         neg_index += 1
    
#     if neg_index == len(section):
#         return False
    
#     for i in range(neg_index, len(section)):
#         if section[i][3] >= 0:
#             pos = True
#             break
    
#     return pos

# # detect a trend of negative to positive to negative values
# def neg_to_pos_to_neg(section):
#     neg = False
#     pos_index = 1

#     if not (section[0][3] < 0):
#         return False
    
#     while pos_index < len(section) and section[pos_index][3] < 0:
#         pos_index += 1
    
#     if pos_index == len(section):
#         return False
    
#     for i in range(pos_index, len(section)):
#         if section[i][3] < 0:
#             neg = True
#             break
    
#     return neg


# def get_angle(section):
#     steer = section[0][4]
#     start_angle = section[0][3]
#     end_angle = section[-1][3]

#     motion = get_car_motion(section[0][2], section[0][4])
    
#     if motion == "df" or motion == "ar": # in clockwise direction
#         if neg_to_pos(section) or pos_to_neg_to_pos(section):
#             end_angle = section[-1][3] - TWO_PI

#     elif motion == "dr" or motion == "af": # in anticlockwise direction
#         if pos_to_neg(section) or neg_to_pos_to_neg(section):
#             end_angle = section[-1][3] + TWO_PI

#     return abs(end_angle - start_angle)
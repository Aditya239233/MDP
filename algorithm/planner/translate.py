import pickle
import math
from HybridAstarPlanner.hybrid_astar import Path
from HybridAstarPlanner.utils import Angle, C

SPEED = 0.01 #unit/ms
ROT_TIME = 2132.676237 #ms/rad

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
        
# different aspects of motion
# Car can move straight but starting to turn (steer > 0) = not on turning motion but is turning
# Car turning = on turning motion

# Detect if the steering angle changes from 0 (starts to turn), or if there is a change in sign (change in steer dir)

def translate(path, start_x, start_y, first_angle):

    instructions = []

    on_turning_motion = is_turning(path.steer[0]) # check if car is already turning from the start
    straight_path = [(start_x, start_y)] # append start pos just for init, will not be used if car is alr turning
    start_angle = prev_angle = first_angle
    end_angle = 0

    left_turning = path.steer[0] <= 0
    reverse_moving = False


    for i in range(len(path.x)):
        
        # smoothen the yaw values
        if abs(path.yaw[i] - prev_angle) > Angle.NINETY_DEG:
            if path.yaw[i] < 0:
                path.yaw[i] += 2 * math.pi
            else:
                path.yaw[i] -= 2 * math.pi

        prev_angle = path.yaw[i]

        reverse_moving = path.direction[i] < 0
        sign = 'r' if reverse_moving else 'f'

        # check for anomalies in steer (-ve +ve -ve)
        if i > 0 and i < len(path.x)-1:
            if same_sign(path.steer[i-1], path.steer[i+1]) and not same_sign(path.steer[i], path.steer[i+1]):
                path.steer[i] *= -1


        # border bet straight line and turning motion
        if not on_turning_motion:
            straight_path.append((path.x[i], path.y[i]))
        
            if is_turning(path.steer[i]):
                on_turning_motion = True

                left_turning = path.steer[i] < 0  # if negative, means car is turning left
                start_angle = path.yaw[i]

                dist = calculate_dist(straight_path)
                t = dist/SPEED

                if reverse_moving:
                    instructions.append(f"s{t :04.0f}")
                else:
                    instructions.append(f"w{t :04.0f}")

                straight_path = []
        else:
            # if |steer| > 0 => still turning => update angle of car
            if is_turning(path.steer[i]):
                end_angle = path.yaw[i]

                # if car is still turning, check if steer direction changed
                curr_left_turning = path.steer[i] < 0

                # if steer direction changed, start new turning movement
                if (left_turning and not curr_left_turning) or (not left_turning and curr_left_turning):
                    t = int(abs(end_angle-start_angle) * ROT_TIME)

                    if left_turning:
                        print(f"a{sign}{t :04.0f}")
                    else:
                        print(f"d{sign}{t :04.0f}")

                    start_angle = path.yaw[i]
                    left_turning = curr_left_turning

            else: # car started to move in straight line
                on_turning_motion = False
                end_angle = path.yaw[i]
                
                t = int(abs(end_angle-start_angle) * ROT_TIME)

                if left_turning:
                    instructions.append(f"a{sign}{t :04.0f}")
                else:
                    instructions.append(f"d{sign}{t :04.0f}")

                straight_path.append((path.x[i], path.y[i]))


    # at the end of motion

    if on_turning_motion:
        on_turning_motion = False
            
        t = int(abs(end_angle-start_angle) * ROT_TIME)


        if left_turning:
            instructions.append(f"a{sign}{t :04.0f}")
        else:
            instructions.append(f"d{sign}{t :04}")
    else:
        dist = calculate_dist(straight_path)
        t = dist/SPEED

        # sometimes if t is very small, we can ignore the last bit of forward/backward motion
        if t >= 70:
            if reverse_moving:
                instructions.append(f"s{t :04.0f}")
            else:
                instructions.append(f"w{t :04.0f}")

    if path.yaw[-1] < 0:
        path.yaw[-1] += 2 * math.pi

    return path.x[-1], path.y[-1], path.yaw[-1], instructions


def translate_tour(tour):
    list_of_instructions = []
    next_x, next_y, next_angle = C.CAR_START_POS

    for path in tour:
        print(path.steer)
        next_x, next_y, next_angle, instructions = translate(path, next_x, next_y, next_angle)
        instructions.append("C5000")  # car stop and do image recognition
        list_of_instructions.extend(instructions)

    return list_of_instructions
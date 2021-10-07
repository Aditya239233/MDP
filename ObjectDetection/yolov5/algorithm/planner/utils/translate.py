from algorithm.planner.utils.helpers import convert_sim_to_val
from algorithm.planner.utils.angles import Angle
import math
import re

from numpy import add
from algorithm.planner.entity.path import Path

SPEED = 0.01 #unit/ms (50cm/s)
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
	# print(motion)
	# print(section)
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

def add_rotation_offset(motion, time):
	# if motion == "af":
	# 	if time <= 499:
	# 		time += 20
	# 	elif time <= 699:
	# 		time += 10
	# 	elif time <=1000:
	# 		time += 5
	
	# elif motion == "ar":
	# 	if time <= 300:
	# 		time += 30
	# 	elif time <= 699:
	# 		time += 20
	# 	elif time <=1000:
	# 		time += 10

	# elif motion == "df":
	# 	if time <= 499:
	# 		time += 40
	# 	elif time <= 699:
	# 		time += 20
	# 	elif time <=1000:
	# 		time += 10
	
	# elif motion == "dr":
	# 	if time <= 499:
	# 		time += 35
	# 	elif time <= 699:
	# 		time += 20
	# 	elif time <=1000:
	# 		time += 10

	# OUTDOOR
	if motion == "af":
		if time <= 499:
			time += 42
		elif time <= 699:
			time += 12
		elif time <=1000:
			time += 10
	
	elif motion == "ar":
		if time <= 100:
			time += 35
		elif time <= 200:
			time += 30
		if time <= 499:
			time += 30
		elif time <= 700:
			time += 10
		elif time <=1000:
			time += 5

	elif motion == "df":
		if time <= 499:
			time += 22
		elif time <= 699:
			time += 15
		elif time <=1000:
			time += 10
	
	elif motion == "dr":
		if time <= 499:
			time += 23
		elif time <= 699:
			time += 12
		elif time <=1000:
			time += 7

	return time

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
		dt = add_rotation_offset(motion, dt)
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

def in_fourth_quadrant(angle):
	return angle >= Angle.TWO_SEVENTY_DEG and angle < Angle.THREE_SIXTY_DEG

def in_first_quadrant(angle):
	return angle >= Angle.ZERO_DEG and angle < Angle.NINETY_DEG

# see if curr is increased from last
# need to check for edge case -> when yaw crosses the 0 rad mark
def increasing(curr, last):
	if in_fourth_quadrant(last) and in_first_quadrant(curr):
		return True
	if in_first_quadrant(last) and in_fourth_quadrant(curr):
		return False
	return curr > last

def check_and_fix_anomalies(path):
	# Sometimes, the sign of steer will be wrong - can detect through a window of size 3 on the yaw value

	for i in range(0, len(path.x)-1):
		path.yaw[i] = get_base_angle(path.yaw[i])

	# # if the yaw is changing, then steer should be non-zero - and only check for zero steer
	for i in range(1, len(path.x)):
		curr_yaw = path.yaw[i]
		last_yaw = path.yaw[i-1]
		curr_steer = path.steer[i]
		if math.isclose(curr_steer, 0) and not math.isclose(curr_yaw, last_yaw):
			if path.direction[i] > 0:
				if increasing(curr_yaw, last_yaw):
					path.steer[i] = -0.7
				else:
					path.steer[i] = 0.7
			else:
				if increasing(curr_yaw, last_yaw):
					path.steer[i] = 0.7
				else:
					path.steer[i] = -0.7

	# check for change of yaw at the start
	start_yaw = path.yaw[0]
	next_yaw = path.yaw[1]

	if not math.isclose(start_yaw, next_yaw):
		if path.direction[0] > 0:
			if increasing(next_yaw, start_yaw):
				path.steer[0] = -0.6
			else:
				path.steer[0] = 0.6
		else:
			if increasing(next_yaw, start_yaw):
				path.steer[0] = 0.6
			else:
				path.steer[0] = -0.6


	# check for anomalies in steer (-ve +ve -ve or +ve -ve +ve)
	for i in range(1, len(path.x)-1):
		if same_sign(path.steer[i-1], path.steer[i+1]) and not same_sign(path.steer[i], path.steer[i+1]):
			path.steer[i] *= -1

def add_instruction(ins_list, pos_list, ins, pos):
	if int(ins[-4:]) == 0:
		return
	
	ins_list.append(ins)
	pos_list.append(pos)

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
			next_coor = (curr_x, curr_y, curr_yaw)
			add_instruction(instructions, pos_after_instruction, curr_instruction, next_coor)

			curr_section = [val]
		else:
			curr_section.append(val)
		
		prev_motion = curr_motion
	
	if curr_section:
		curr_instruction = get_instruction(curr_section)
		next_coor = (curr_x, curr_y, curr_yaw)
		add_instruction(instructions, pos_after_instruction, curr_instruction, next_coor)

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
	
	coor_string = android_coor_to_string(list_of_coor, list_of_instructions)

	return list_of_instructions, coor_string


def android_coor_to_string(list_of_coor, instructions):
	list_of_path_str = []

	i = j = 0

	for i in range(len(list_of_coor)):
		path = list_of_coor[i]
		path_coor = []

		for j in range(len(path)):
			instruction = instructions[i][j]
			x = path[j][0]
			y = path[j][1]
			yaw = path[j][2]

			to_append = f"({instruction},{x :.3f},{y :.3f},{yaw :.3f})"
			path_coor.append(to_append)
		
		path_str = ",".join(path_coor)
		list_of_path_str.append(path_str)

	results = "|".join(list_of_path_str)
			
	return results


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
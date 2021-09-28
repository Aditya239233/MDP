from algorithm.planner.utils.angles import Angle
from algorithm.planner.utils.arena_utils import Arena_C
from algorithm.planner.utils.car_utils import Car_C
from algorithm.planner.algorithms.hybrid_astar.core.hybrid_astar import hybrid_astar_planning
from algorithm.planner.algorithms.hybrid_astar.params import C

import math
import numpy as np
from itertools import permutations

# Given the obstacles, set the car's position in front of the obstacles as waypoints
# Then, these waypoints are treated as nodes of the path graph
def generate_waypoints(start_pos, obstacles, sideways=False):
    waypoints = {-1: start_pos} #start_pos - (x, y, direction)

    for obstacle in obstacles:
        x1 = obstacle.x
        y1 = obstacle.y
        face = obstacle.face
        obs_id = obstacle.img_id

        if not sideways:
            if face == Angle.ZERO_DEG: # E
                w_x = x1 + Arena_C.OBS_LENGTH + Car_C.TOL_SPACE
                w_y = y1 + Arena_C.OBS_LENGTH // 2
                w_face = Angle.ONE_EIGHTY_DEG

            elif face == Angle.ONE_EIGHTY_DEG: # W
                w_x = x1 - Car_C.TOL_SPACE
                w_y = y1 + Arena_C.OBS_LENGTH // 2
                w_face = Angle.ZERO_DEG

            elif face == Angle.NINETY_DEG: # N
                w_x = x1 + Arena_C.OBS_LENGTH // 2
                w_y = y1 + Arena_C.OBS_LENGTH + Car_C.TOL_SPACE
                w_face = Angle.TWO_SEVENTY_DEG

            elif face == Angle.TWO_SEVENTY_DEG: # S
                w_x = x1 + Arena_C.OBS_LENGTH // 2
                w_y = y1 - Car_C.TOL_SPACE
                w_face = Angle.NINETY_DEG
        else:
            if face == Angle.ZERO_DEG: # E
                w_x = x1 + Arena_C.OBS_LENGTH + Car_C.TOL_SPACE
                w_y = y1 + Arena_C.OBS_LENGTH // 2 + (Car_C.ACTUAL_CAR_LENGTH // 2 - Car_C.ACTUAL_RB)
                w_face = Angle.TWO_SEVENTY_DEG

            elif face == Angle.NINETY_DEG: # N
                w_x = x1 + Arena_C.OBS_LENGTH // 2 - (Car_C.ACTUAL_CAR_LENGTH // 2 - Car_C.ACTUAL_RB)
                w_y = y1 + Arena_C.OBS_LENGTH + Car_C.TOL_SPACE
                w_face = Angle.ZERO_DEG

            elif face == Angle.TWO_SEVENTY_DEG: # S
                w_x = x1 + Arena_C.OBS_LENGTH // 2 + (Car_C.ACTUAL_CAR_LENGTH // 2 - Car_C.ACTUAL_RB)
                w_y = y1 - Car_C.TOL_SPACE
                w_face = Angle.ONE_EIGHTY_DEG

            elif face == Angle.ONE_EIGHTY_DEG: # W
                w_x = x1 - Car_C.TOL_SPACE
                w_y = y1 + Arena_C.OBS_LENGTH // 2 - (Car_C.ACTUAL_CAR_LENGTH // 2 - Car_C.ACTUAL_RB)
                w_face = Angle.NINETY_DEG
        
        waypoints[obs_id] = (w_x, w_y, w_face)
        print(waypoints[obs_id])

    return waypoints


# Given the path, returns its distance
def find_path_distance(ox, oy):
    length = len(ox)
    path_distance = 0

    for i in range(length-1):
        dx = ox[i+1] - ox[i]
        dy = oy[i+1] - oy[i]
        path_distance += math.sqrt(dx*dx + dy*dy)

    return path_distance


# Returns the distance vector for the arena waypoints (including start position)
# This is used to find the Hamiltonian path
def get_dist_bet_waypoints(waypoint_dict, ox, oy):
    waypoint_labels = list(waypoint_dict.keys())
    num_nodes = len(waypoint_labels)
    dist_vector = np.zeros((num_nodes, num_nodes))

    for i in range(num_nodes-1):
        for dest_lbl in waypoint_labels[i+1:]:
            src_lbl = int(waypoint_labels[i])
            dest_lbl = int(dest_lbl)

            sx, sy, syaw0 = waypoint_dict[src_lbl]
            gx, gy, gyaw0 = waypoint_dict[dest_lbl]

            path = hybrid_astar_planning(sx, sy, syaw0, gx, gy, gyaw0, ox, oy, C.XY_RESO, C.YAW_RESO)

            if path == None:
                print(f"Finding dist bet. waypoints: Path is not found for\n {sx}, {sy}, {gx}, {gy}")
                dist = -1
            else:
                dist = find_path_distance(path.x, path.y)

            # assuming label is an integer
            dist_vector[src_lbl][dest_lbl] = dist
            dist_vector[dest_lbl][src_lbl] = dist

    return dist_vector


def get_dist_of_tour(path, dist_vector):
    total_dist = 0

    for i in range(len(path)-1):
        src = path[i]
        dest = path[i+1]

        path_dist = dist_vector[src][dest]

        if path_dist != -1:
            total_dist += path_dist
        else: # path does not exist
            total_dist += math.inf
    
    return total_dist


# Since there are only 6 waypoints (inc start position),
# we can use brute-force to find the Hamiltonian path
# For n > 10, we need to implement a polynomial approximation algorithm instead
def get_shortest_tour(waypoint_dict, dist_vector):
    node_lbl = list(waypoint_dict.keys())
    node_lbl.remove(-1) # -1 is source

    all_permutations = permutations(node_lbl)
    min_tour = []
    min_dist = math.inf

    # brute force all possible paths
    for arr in all_permutations:
        tour = [-1]
        tour.extend(arr)
        dist = get_dist_of_tour(tour, dist_vector)

        # if any path in the tour does not exist, then the dist will be >= inf
        # and the following if statement will not be executed
        if dist < min_dist:
            min_tour = tour
            min_dist = dist
        
    #     print(f"{path}: {dist}")

    # print()
    # print(f"{min_path} has the shortest distance of {min_dist}")

    # get the path in terms of waypoints (currently it is still in labels)
    waypoints = []
    for node in min_tour:
        waypoints.append(waypoint_dict[node])

    return waypoints, min_tour
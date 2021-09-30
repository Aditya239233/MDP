from algorithm.planner.utils.angles import Angle
from algorithm.planner.utils.arena_utils import Arena_C
from algorithm.planner.utils.car_utils import Car_C
from algorithm.planner.algorithms.hybrid_astar.core.hybrid_astar import hybrid_astar_planning
from algorithm.planner.algorithms.hybrid_astar.params import C

import math
import numpy as np
from itertools import permutations

START_NODE_LBL = 99

# Given the obstacles, set the car's position in front of the obstacles as waypoints
# Then, these waypoints are treated as nodes of the path graph
def generate_waypoints(start_pos, obstacles, sideways=False):
    waypoints = {START_NODE_LBL: start_pos} #start_pos - (x, y, direction)

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
    waypoint_to_dist_index = {}

    i = 0
    for waypoint_lbl in waypoint_labels:
        waypoint_to_dist_index[waypoint_lbl] = i
        i += 1

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

            src_index =  waypoint_to_dist_index[src_lbl]
            dest_index = waypoint_to_dist_index[dest_lbl]

            # assuming label is an integer
            dist_vector[src_index][dest_index] = dist
            dist_vector[dest_index][src_index] = dist

    return dist_vector, waypoint_to_dist_index


def get_dist_of_tour(path, dist_vector, waypoint_index_dict):
    total_dist = 0

    for i in range(len(path)-1):
        src_lbl = path[i]
        dest_lbl = path[i+1]

        src_index = waypoint_index_dict[src_lbl]
        dest_index = waypoint_index_dict[dest_lbl]

        path_dist = dist_vector[src_index][dest_index]

        if path_dist != -1:
            total_dist += path_dist
        else: # path does not exist
            total_dist += math.inf
    
    return total_dist


# Since there are only 6 waypoints (inc start position),
# we can use brute-force to find the Hamiltonian path
# For n > 10, we need to implement a polynomial approximation algorithm instead
def get_shortest_tour(waypoint_dict, dist_vector, waypoint_index_dict):

    # Use brute force if there are 5 obstacles or fewer
    if len(dist_vector) <= 6:
        print("Using exhaustive search")
        node_lbl = list(waypoint_dict.keys())
        node_lbl.remove(START_NODE_LBL)

        all_permutations = permutations(node_lbl)
        min_tour = []
        min_dist = math.inf

        # brute force all possible paths, fix start node as first
        for arr in all_permutations:
            tour = [START_NODE_LBL]
            tour.extend(arr)
            dist = get_dist_of_tour(tour, dist_vector, waypoint_index_dict)

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

    # Or else, use a simple greedy algorithm to find shortest tour
    print("Using Greedy")
    node_lbls = list(waypoint_dict.keys())

    tour = [START_NODE_LBL]
    num_of_nodes = len(node_lbls)
    visited = [False] * num_of_nodes
    visited[waypoint_index_dict[START_NODE_LBL]] = True

    # Find next nearest neighbor
    for i in range(1, num_of_nodes):
        curr_node = tour[-1] # last node
        nearest_unvisited_node = find_nearest(curr_node, dist_vector, visited, waypoint_index_dict)
        tour.append(nearest_unvisited_node)
    
    waypoints = []
    for node in tour:
        waypoints.append(waypoint_dict[node])

    return waypoints, tour

# Returns the label of the nearest unvisited node
def find_nearest(curr_node, dist_vector, visited, waypoint_index_dict):
    curr_node_index = waypoint_index_dict[curr_node]
    all_dist_to_curr = dist_vector[curr_node_index]

    min_dist = min_node_index = math.inf

    for i in range(len(all_dist_to_curr)):
        dist = all_dist_to_curr[i]
        if i != curr_node_index and not visited[i] and dist < min_dist:
            min_dist = dist
            min_node_index = i
    
    visited[min_node_index] = True
    return list(waypoint_index_dict.keys())[list(waypoint_index_dict.values()).index(min_node_index)]

import math
from typing import Dict

from algorithm.planner.algorithms.hybrid_astar.core import graph
from algorithm.planner.algorithms.hybrid_astar.core import reeds_shepp as rs
from algorithm.planner.utils.arena_utils import Arena_C
from algorithm.planner.utils.car_utils import Car_C
from algorithm.planner.algorithms.hybrid_astar.params import C
from algorithm.planner.algorithms.hybrid_astar.core.hybrid_astar import hybrid_astar_planning
from algorithm.planner.entity.arena import Arena
from algorithm.planner.utils.helpers import get_key_from_dict
from typing import List

def remove_point_from_dist_vector(dist_vector, index_to_remove):

    dist_vector.pop(index_to_remove)

    for distances in dist_vector:
        distances.pop(index_to_remove) # remove the column too
    
    return index_to_remove


def remove_obstacle(dist_vector:List, waypoints:Dict, waypoint_index_dict:Dict):

    distances = [sum(dist_vector[i]) for i in range(len(dist_vector))]
    invalid_dist = min(distances)
    invalid_dist_index = distances.index(invalid_dist)

    obs_label_to_remove = get_key_from_dict(waypoint_index_dict, invalid_dist_index)
    waypoint_index_dict.pop(obs_label_to_remove)
    waypoints.pop(obs_label_to_remove)

    # need to update the waypoint_index_dict
    # all index values more than index_removed will decrement by 1
    index_removed = remove_point_from_dist_vector(dist_vector, invalid_dist_index)
    for key in waypoint_index_dict.keys():
        index = waypoint_index_dict[key]
        if index > index_removed:
            waypoint_index_dict[key] -= 1


# Given the obstacles, returns list of paths (from point A to B to C to ...) (a Hamiltonian path)
# The parameters of the car (inc start position) are defined in utils.C
def solve(arena: Arena):

    pathFound = False

    arena.process()

    obstacles = arena.get_obstacles()
    print("Obstacles obtained")
    print(obstacles, "\n")

    ox, oy, _, _ = arena.design_obstacles()
    print("Obstacle drawn")

    waypoint_dict = graph.generate_waypoints(arena.get_start_pos(), obstacles, sideways=False)
    print("Waypoints generated")

    try:
        dist_vector, waypoint_index_dict = graph.get_dist_bet_waypoints(waypoint_dict, ox, oy)
        print("Distance vector found")
    except Exception as e:
        print("Distance vector cannot be found")
        raise
    

    while not pathFound:

        tour, tour_sequence = graph.get_shortest_tour(waypoint_dict, dist_vector, waypoint_index_dict)

        # No waypoints means no valid tour found
        # Then remove the obstacle that causes no path to be found
        # The removed obstacle will be included in the arena to avoid collision with bot
        if tour == None or len(tour) == 0:
            print("No shortest tour found")
            remove_obstacle(dist_vector, waypoint_dict, waypoint_index_dict)
        else:
            print("Shortest tour found")
            pathFound = True
    

    # Given an ordered list of waypoints, find the route
    paths = []

    # get the tour
    for i in range(len(tour)-1):
        sx, sy, syaw0 = tour[i]
        gx, gy, gyaw0 = tour[i+1]

        # This can be avoided by storing the paths in memory.
        # However, num_of_paths takes O(n^2) memory, so I recomputed them instead
        path = hybrid_astar_planning(sx, sy, syaw0, gx, gy, gyaw0,
                                 ox, oy, C.XY_RESO, C.YAW_RESO)

        if not path:
            raise Exception(f"{tour[i]} and {tour[i+1]} don't have a path!")

        paths.append(path)

    # calculate steer value
    for path in paths:
        
        n = len(path.x)
        for k in range(n):
            if k < n - 2:
                dy = (path.yaw[k + 1] - path.yaw[k]) / C.MOVE_STEP
                steer = rs.pi_2_pi(math.atan(-Car_C.WB * dy / path.direction[k]))
            else:
                steer = 0
            
            path.steer.append(steer)

    obs_index = 1
    # Add the waypoint to the path end and
    # Add starting point to the path start
    for path in paths:
        # Start
        w_x = tour[obs_index-1][0]
        w_y = tour[obs_index-1][1]
        w_yaw = tour[obs_index-1][2]
        direction = path.direction[0]
        steer = path.steer[0]

        path.x = [w_x] + path.x
        path.y = [w_y] + path.y
        path.yaw = [w_yaw] + path.yaw
        path.direction = [direction] + path.direction
        path.steer = [steer] + path.steer

        # End
        w_x = tour[obs_index][0]
        w_y = tour[obs_index][1]
        w_yaw = tour[obs_index][2]
        direction = path.direction[-1]
        steer = path.steer[-1]

        path.x.append(w_x)
        path.y.append(w_y)
        path.yaw.append(w_yaw)
        path.direction.append(direction)
        path.steer.append(steer)

        obs_index += 1

    print("Tour returned")
    return paths, tour_sequence

import math

from .core import graph
from .core import reeds_shepp as rs
from utils.arena_utils import Arena_C
from utils.car_utils import Car_C
from .params import C
from .core.hybrid_astar import hybrid_astar_planning
from entity.arena import Arena



# Given the obstacles, returns list of paths (from point A to B to C to ...) (a Hamiltonian path)
# The parameters of the car (inc start position) are defined in utils.C
def solve(arena: Arena):

    arena.process()

    obstacles = arena.get_obstacles()
    print("Obstacles obtained")
    print(obstacles, "\n")

    ox, oy, _, _ = arena.design_obstacles()
    print("Obstacle drawn")

    waypoint_dict = graph.generate_waypoints(arena.get_start_pos(), obstacles)
    print("Waypoints generated")

    try:
        dist_vector = graph.get_dist_bet_waypoints(waypoint_dict, ox, oy)
        print("Distance vector found")
    except Exception as e:
        print("Distance vector cannot be found")
        raise

    tour, tour_sequence = graph.get_shortest_tour(waypoint_dict, dist_vector)

    # if no waypoints == no valid tour found
    if len(tour) == 0:
        print("No shortest tour found")
        raise
    else:
        print("Shortest tour found")
    

    # Given an ordered list of waypoints, find the route
    paths = []

    # get the tour
    for i in range(len(tour)-1):
        sx, sy, syaw0 = tour[i]
        gx, gy, gyaw0 = tour[i+1]
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

    print("Tour returned")
    return paths, tour_sequence

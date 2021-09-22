import numpy as np
import math
import imageio
import matplotlib.pyplot as plt
import os
import time
import pickle
import CurvesGenerator.reeds_shepp as rs

from collections import defaultdict
from .utils import C, Angle, increment_id
from .draw import Arrow
from itertools import permutations
from .hybrid_astar import hybrid_astar_planning


# Draw the car on the plt simulator
def draw_car(x, y, yaw, steer, color='black'):
    car = np.array([[-C.RB, -C.RB, C.RF, C.RF, -C.RB, C.ACTUAL_RF, C.ACTUAL_RF, -C.ACTUAL_RB, -C.ACTUAL_RB],
                    [C.W / 2, -C.W / 2, -C.W / 2, C.W / 2, C.W / 2, C.W/2, -C.W/2, -C.W/2, C.W/2]])

    wheel = np.array([[-C.TR, -C.TR, C.TR, C.TR, -C.TR],
                      [C.TW / 4, -C.TW / 4, -C.TW / 4, C.TW / 4, C.TW / 4]])

    rlWheel = wheel.copy()
    rrWheel = wheel.copy()
    frWheel = wheel.copy()
    flWheel = wheel.copy()

    Rot1 = np.array([[math.cos(yaw), -math.sin(yaw)],
                     [math.sin(yaw), math.cos(yaw)]])

    Rot2 = np.array([[math.cos(steer), math.sin(steer)],
                     [-math.sin(steer), math.cos(steer)]])

    frWheel = np.dot(Rot2, frWheel)
    flWheel = np.dot(Rot2, flWheel)

    frWheel += np.array([[C.WB], [-C.WD / 2]])
    flWheel += np.array([[C.WB], [C.WD / 2]])
    rrWheel[1, :] -= C.WD / 2
    rlWheel[1, :] += C.WD / 2

    frWheel = np.dot(Rot1, frWheel)
    flWheel = np.dot(Rot1, flWheel)

    rrWheel = np.dot(Rot1, rrWheel)
    rlWheel = np.dot(Rot1, rlWheel)
    car = np.dot(Rot1, car)

    frWheel += np.array([[x], [y]])
    flWheel += np.array([[x], [y]])
    rrWheel += np.array([[x], [y]])
    rlWheel += np.array([[x], [y]])
    car += np.array([[x], [y]])

    plt.plot(car[0, :], car[1, :], color)
    plt.plot(frWheel[0, :], frWheel[1, :], color)
    plt.plot(rrWheel[0, :], rrWheel[1, :], color)
    plt.plot(flWheel[0, :], flWheel[1, :], color)
    plt.plot(rlWheel[0, :], rlWheel[1, :], color)
    Arrow(x, y, yaw, C.WB * 0.8, color)


# The obstacles are defined using lists of values (ox - list of x-coordinates, etc)

# Helper func: Add obstacle bot-left, top-right corners and face to the obstacle coors (ox, oy, ...)
# Passes the return lists as parameters to avoid copying
def add_obstacles(x1, y1, x2, y2, face, ox, oy, ox_face, oy_face):

    # SOUTH FACE
    for i in range(x1, x2+1):
        ox.append(i)
        oy.append(y1)
    if face == Angle.TWO_SEVENTY_DEG:
        for i in range(x1, x2+1):
            ox_face.append(i)
            oy_face.append(y1)
    
    # EAST FACE
    for i in range(y1, y2+1):
        ox.append(x2)
        oy.append(i)
    if face == Angle.ZERO_DEG:
        for i in range(y1, y2+1):
            ox_face.append(x2)
            oy_face.append(i)
    
    # NORTH FACE
    
    for i in range(x1, x2+1):
        ox.append(i)
        oy.append(y2)
    if face == Angle.NINETY_DEG:
        for i in range(x1, x2+1):
            ox_face.append(i)
            oy_face.append(y2)

    # WEST FACE
    for i in range(y1, y2+1):
        ox.append(x1)
        oy.append(i)
    if face == Angle.ONE_EIGHTY_DEG:
        for i in range(y1, y2+1):
            ox_face.append(x1)
            oy_face.append(i)
    
# Helper func: Define the bounding box for the arena as a huge rectangular obstacle
# Passes the return lists as parameters to avoid copying
def draw_arena_box(x, y, ox, oy):
    for i in range(x):
        ox.append(i)
        oy.append(0)
    for i in range(x):
        ox.append(i)
        oy.append(y - 1)
    for i in range(y):
        ox.append(0)
        oy.append(i)
    for i in range(y):
        ox.append(x - 1)
        oy.append(i)


# Adds the arena + obstacles
# Returns their coordinates lists
def design_obstacles(x, y, obstacles):
    ox, oy = [], []
    ox_face, oy_face = [], [] # for showing obstacle face

    draw_arena_box(x+1, y+1, ox, oy)

    for obstacle in obstacles:
        obs_x1 = obstacle[0]
        obs_y1 = obstacle[1]
        obs_x2 = int(obs_x1 + C.OBS_LENGTH) - 1
        obs_y2 = int(obs_y1 + C.OBS_LENGTH) - 1
        face = obstacle[2]

        add_obstacles(obs_x1,obs_y1, obs_x2,obs_y2, face, ox,oy, ox_face,oy_face)

    return ox, oy, ox_face, oy_face

# Given the obstacles, set the car's position in front of the obstacles as waypoints
# Then, these waypoints are treated as nodes of the path graph
def generate_waypoints(start_pos, obstacles):
    waypoints = {0: start_pos}
    i = 1

    for obstacle in obstacles:
        x1, y1, face = obstacle

        if face == Angle.ZERO_DEG:
            w_x = x1 + C.OBS_LENGTH + C.TOL_SPACE
            w_y = y1 + C.OBS_LENGTH // 2
            w_face = Angle.ONE_EIGHTY_DEG

        elif face == Angle.ONE_EIGHTY_DEG:
            w_x = x1 - C.TOL_SPACE
            w_y = y1 + C.OBS_LENGTH // 2
            w_face = Angle.ZERO_DEG

        elif face == Angle.NINETY_DEG:
            w_x = x1 + C.OBS_LENGTH // 2
            w_y = y1 + C.OBS_LENGTH + C.TOL_SPACE
            w_face = Angle.TWO_SEVENTY_DEG

        elif face == Angle.TWO_SEVENTY_DEG:
            w_x = x1 + C.OBS_LENGTH // 2
            w_y = y1 - C.TOL_SPACE
            w_face = Angle.NINETY_DEG
    
        waypoints[i] = (w_x, w_y, w_face)
        i += 1

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
    node_lbl.remove(0) # 0 is source

    all_permutations = permutations(node_lbl)
    min_tour = []
    min_dist = math.inf

    # brute force all possible paths
    for arr in all_permutations:
        tour = [0]
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

    return waypoints


def translate_val_to_sim(obstacles):
    new_obstacles = []
    for obs in obstacles:
        new_x = obs[0] + C.OFFSET_X
        new_y = obs[1] + C.OFFSET_Y
        new_obstacles.append((new_x, new_y, obs[2]))

    return new_obstacles

# Given the obstacles, returns list of paths (from point A to B to C to ...) (a Hamiltonian path)
# The parameters of the car (inc start position) are defined in utils.C
def solve(obstacles):

    obstacles = translate_val_to_sim(obstacles)
    
    ox, oy, ox_face, oy_face = design_obstacles(C.X, C.Y, obstacles)
    waypoint_dict = generate_waypoints(C.CAR_START_POS, obstacles)

    try:
        dist_vector = get_dist_bet_waypoints(waypoint_dict, ox, oy)
        print("Distance vector found")
    except Exception as e:
        raise

    tour = get_shortest_tour(waypoint_dict, dist_vector)

    # if no waypoints == no valid tour found
    if len(tour) == 0:
        raise Exception("No tour found")
    else:
        print("Shortest tour found")
    

    # Given a list of ordered waypoints, find the route
    paths = []

    # get the tour
    for i in range(len(tour)-1):
        sx, sy, syaw0 = tour[i]
        gx, gy, gyaw0 = tour[i+1]
        path = hybrid_astar_planning(sx, sy, syaw0, gx, gy, gyaw0,
                                 ox, oy, C.XY_RESO, C.YAW_RESO)

        if not path:
            raise Exception(f"{tour[i]} and {tour[i+1]} don't have a path!") # Should this ever be reached?

        paths.append(path)

    # calculate steer value
    for path in paths:

        n = len(path.x)
        for k in range(n):
            if k < n - 2:
                dy = (path.yaw[k + 1] - path.yaw[k]) / C.MOVE_STEP
                steer = rs.pi_2_pi(math.atan(-C.WB * dy / path.direction[k]))
            else:
                steer = 0
            
            path.steer.append(steer)

    print("Tour returned")
    return paths


# Given the paths and the obstacles (arena + car start pos is defined in utils),
# either show plt simulation or save as gif
def simulate(tour, obstacles, 
             save_gif=False, gif_name=None, keep_files=False):

    if gif_name == None:
        id = increment_id("gif")
        gif_name = f"./results/gif/{id}.gif"


    obstacles = translate_val_to_sim(obstacles)
    ox, oy, ox_face, oy_face = design_obstacles(C.X, C.Y, obstacles)

    print("Simulation started")
    start_time = time.time()

    x = []
    y = []
    yaw = []
    direction = []

    for path in tour:
        x.extend(path.x)
        y.extend(path.y)
        yaw.extend(path.yaw)
        direction.extend(path.direction)


        # extend the duration to simulate taking pictures
        last_x = [path.x[-1]] * 10
        last_y = [path.y[-1]] * 10
        last_yaw = [path.yaw[-1]] * 10
        last_direction = [path.direction[-1]] * 10

        x.extend(last_x)
        y.extend(last_y)
        yaw.extend(last_yaw)
        direction.extend(last_direction)
    

    filenames = []
    for k in range(len(x)):
        plt.cla()

        # plot obstacles

        plt.plot(ox, oy, "sk")
        plt.plot(ox_face, oy_face, "sy")

        # Plot carpark
        p1, p2, p3 = [0+C.OFFSET_X,6+C.OFFSET_Y], [6+C.OFFSET_X,6+C.OFFSET_Y], [6+C.OFFSET_X,0+C.OFFSET_Y]
        plt.plot(p1, p2, p2, p3)

        plt.plot(x, y, linewidth=1.5, color='r')

        if k < len(x) - 2:
            dy = (yaw[k + 1] - yaw[k]) / C.MOVE_STEP
            steer = rs.pi_2_pi(math.atan(-C.WB * dy / direction[k]))
        else:
            steer = 0.0

        draw_car(x[k], y[k], yaw[k], steer)
        plt.title("Hybrid A*")
        plt.axis("equal")
        plt.grid(b=True)

        if save_gif:
            filename = f"./results/temp/{k}.png"
            filenames.append(filename)
            plt.savefig(filename)
            plt.close()
        else:
            plt.pause(0.0001)
        

    if not save_gif:
        plt.show()
    else:
        with imageio.get_writer(gif_name, mode='I') as writer:
            for filename in filenames:
                image = imageio.imread(filename)
                writer.append_data(image)
            
        # Remove files
        if not keep_files:
            for filename in filenames:
                os.remove(filename)

    end_time = time.time()
    print(f"Done! Took {end_time-start_time} seconds")

def save_valid_obstacles(obstacles, id):
    with open("./results/valid_arena/arena.txt", "a") as f:
        s = []
        for obs in obstacles:
            face = obs[2]

            if face == Angle.ZERO_DEG:
                face = "Angle.ZERO_DEG"
            elif face == Angle.NINETY_DEG:
                face = "Angle.NINETY_DEG"
            elif face == Angle.ONE_EIGHTY_DEG:
                face = "Angle.ONE_EIGHTY_DEG"
            elif face == Angle.TWO_SEVENTY_DEG:
                face = "Angle.TWO_SEVENTY_DEG"
            s.append(f"({obs[0]}, {obs[1]}, {face})")
        
        f.write(f"{id}\n")
        f.write(",\n".join(s))
        f.write("\n\n")

# Save the arena image
# Used when there is no path found (error), and we want to see which obstacle combinations lead to this error
def save_arena_img(obstacles, error=False):

    obstacles = translate_val_to_sim(obstacles)
    ox, oy, ox_face, oy_face = design_obstacles(C.X, C.Y, obstacles)
    plt.plot(ox, oy, "sk")
    plt.plot(ox_face, oy_face, "sy")
    p1, p2, p3 = [0+C.OFFSET_X,6+C.OFFSET_Y], [6+C.OFFSET_X,6+C.OFFSET_Y], [6+C.OFFSET_X,0+C.OFFSET_Y]
    plt.plot(p1, p2, p2, p3)
    plt.title("Path not found")
    plt.axis("equal")
    plt.grid(b=True)

    if error:
        id = increment_id("error")
        filename = f"./results/error_arena/{id}.png"
    else:
        id = increment_id("valid")
        save_valid_obstacles(obstacles, id)
        filename = f"./results/valid_arena/{id}.png"

    plt.savefig(filename)
    plt.close()

    return id


def save_tour_to_pickle(paths, id):

    pickle.dump(paths, open(f"./results/valid_paths/tour{id}.pkl", "wb"))
    print(f"Tour saved as tour{id}.pkl\n")

import numpy as np
import math
import imageio
import matplotlib.pyplot as plt
import os
import time
import CurvesGenerator.reeds_shepp as rs

from .utils import C, Angle
from .draw import Arrow
from itertools import permutations
from .hybrid_astar import hybrid_astar_planning



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


def find_path_distance(ox, oy):
    length = len(ox)
    path_distance = 0

    for i in range(length-1):
        dx = ox[i+1] - ox[i]
        dy = oy[i+1] - oy[i]
        path_distance += math.sqrt(dx*dx + dy*dy)

    return path_distance


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
            print(sx, sy, gx, gy)
            path = hybrid_astar_planning(sx, sy, syaw0, gx, gy, gyaw0,
                                    ox, oy, C.XY_RESO, C.YAW_RESO)

            if path == None:
                print(f"Finding dist bet. waypoints: Path is not found for\n {sx}, {sy}, {gx}, {gy}")
                dist = 9999
            else:
                dist = find_path_distance(path.x, path.y)

            # assuming label is an integer
            dist_vector[src_lbl][dest_lbl] = dist
            dist_vector[dest_lbl][src_lbl] = dist

    return dist_vector


def get_dist_of_path(path, dist_vector):
    dist = 0

    for i in range(len(path)-1):
        src = path[i]
        dest = path[i+1]
        dist += dist_vector[src][dest]
    
    return dist


def get_shortest_tour(waypoint_dict, dist_vector):
    node_lbl = list(waypoint_dict.keys())
    node_lbl.remove(0) # 0 is source

    all_permutations = permutations(node_lbl)
    min_path = []
    min_dist = math.inf

    # brute force all possible paths
    for arr in all_permutations:
        path = [0]
        path.extend(arr)
        dist = get_dist_of_path(path, dist_vector)
        if dist < min_dist:
            min_path = path
            min_dist = dist
        
    #     print(f"{path}: {dist}")

    # print()
    # print(f"{min_path} has the shortest distance of {min_dist}")

    # get the path in terms of waypoints (currently it is still in labels)
    waypoints = []
    for node in min_path:
        waypoints.append(waypoint_dict[node])

    return waypoints


def solve(obstacles):
    ox, oy, ox_face, oy_face = design_obstacles(C.X, C.Y, obstacles)
    waypoint_dict = generate_waypoints(C.CAR_START_POS, obstacles)

    try:
        dist_vector = get_dist_bet_waypoints(waypoint_dict, ox, oy)
    except Exception as e:
        plt.plot(ox, oy, "sk")
        plt.plot(ox_face, oy_face, "sy")
        draw_car(3.0, 3.0, Angle.NINETY_DEG, 0)
        plt.grid(b=True)
        plt.show()
        raise

    tour = get_shortest_tour(waypoint_dict, dist_vector)
    

    # Given a list of ordered waypoints, find the route
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

    return paths


def simulate(list_of_paths, obstacles, no_gui=False, save_gif=False, gif_name="./gif/mygif.gif", keep_files=False):
    print("Simulation started")
    start_time = time.time()

    ox, oy, ox_face, oy_face = design_obstacles(C.X, C.Y, obstacles)

    x = []
    y = []
    yaw = []
    direction = []

    for path in list_of_paths:
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
        p1, p2, p3 = [0,12], [12,12], [12,0]
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
            filename = f"./gif/{k}.png"
            filenames.append(filename)
            plt.savefig(filename)
            plt.close()
        else:
            plt.pause(0.0001)
        

    if not no_gui:
        plt.show()

    with imageio.get_writer(gif_name, mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
        
    # Remove files
    if not keep_files:
        for filename in set(filenames):
            os.remove(filename)

    end_time = time.time()
    print(f"Done! Took {end_time-start_time} seconds")


def save_arena_img(obstacles, id=0):
    ox, oy, ox_face, oy_face = design_obstacles(C.X, C.Y, obstacles)
    plt.plot(ox, oy, "sk")
    plt.plot(ox_face, oy_face, "sy")
    p1, p2, p3 = [0,12], [12,12], [12,0]
    plt.plot(p1, p2, p2, p3)
    plt.title("Hybrid A*")
    plt.axis("equal")
    plt.grid(b=True)

    filename = f"./error_arena/{id}.png"
    plt.savefig(filename)
    plt.close()
"""
Hybrid A*
@author: Huiming Zhou
"""

import os
import sys
import math
import heapq
from heapdict import heapdict
from itertools import permutations
import time
import numpy as np
import scipy.spatial.kdtree as kd
from .angles import Angle

sys.path.append(os.path.dirname(os.path.abspath(__file__)) +
                "/../../planner/")

import HybridAstarPlanner.astar as astar
import CurvesGenerator.reeds_shepp as rs

CAR_START_POS = (3.0, 3.0, Angle.NINETY_DEG)
X, Y = 40, 40
OBS_LENGTH = 2
TOL_SPACE = 4

class C:  # Parameter config
    PI = math.pi

    XY_RESO = 1.0  # [m]
    YAW_RESO = np.deg2rad(15.0)  # [rad]
    MOVE_STEP = 0.5  # [m] path interporate resolution
    N_STEER = 20.0  # steer command number
    COLLISION_CHECK_STEP = 5  # skip number for collision check
    EXTEND_BOUND = 1  # collision check range extended

    GEAR_COST = 100.0  # switch back penalty cost
    BACKWARD_COST = 5.0  # backward penalty cost (5.0)
    STEER_CHANGE_COST = 500.0  # steer angle change penalty cost (5.0)
    STEER_ANGLE_COST = 100.0  # steer angle penalty cost (1.0)
    H_COST = 15.0  # Heuristic cost penalty cost

    RF = 2.5  # [m] distance from rear to vehicle front end of vehicle
    RB = 0.5  # [m] distance from rear to vehicle back end of vehicle
    W = 3.0  # [m] width of vehicle (For more allowance)
    WD = 1.8  # [m] distance between left-right wheels
    WB = 1.5  # [m] Wheel base
    TR = 0.5  # [m] Tyre radius
    TW = 1  # [m] Tyre width
    MAX_STEER = 0.6  # [rad] maximum steering angle


class Node:
    def __init__(self, xind, yind, yawind, direction, x, y,
                 yaw, directions, steer, cost, pind):
        self.xind = xind
        self.yind = yind
        self.yawind = yawind
        self.direction = direction
        self.x = x
        self.y = y
        self.yaw = yaw
        self.directions = directions
        self.steer = steer
        self.cost = cost
        self.pind = pind


class Para:
    def __init__(self, minx, miny, minyaw, maxx, maxy, maxyaw,
                 xw, yw, yaww, xyreso, yawreso, ox, oy, kdtree):
        self.minx = minx
        self.miny = miny
        self.minyaw = minyaw
        self.maxx = maxx
        self.maxy = maxy
        self.maxyaw = maxyaw
        self.xw = xw
        self.yw = yw
        self.yaww = yaww
        self.xyreso = xyreso
        self.yawreso = yawreso
        self.ox = ox
        self.oy = oy
        self.kdtree = kdtree


class Path:
    def __init__(self, x, y, yaw, direction, cost):
        self.x = x
        self.y = y
        self.yaw = yaw
        self.direction = direction
        self.cost = cost


class QueuePrior:
    def __init__(self):
        self.queue = heapdict()

    def empty(self):
        return len(self.queue) == 0  # if Q is empty

    def put(self, item, priority):
        self.queue[item] = priority  # push 

    def get(self):
        return self.queue.popitem()[0]  # pop out element with smallest priority


def hybrid_astar_planning(sx, sy, syaw, gx, gy, gyaw, ox, oy, xyreso, yawreso):
    sxr, syr = round(sx / xyreso), round(sy / xyreso)
    gxr, gyr = round(gx / xyreso), round(gy / xyreso)
    syawr = round(rs.pi_2_pi(syaw) / yawreso)
    gyawr = round(rs.pi_2_pi(gyaw) / yawreso)

    nstart = Node(sxr, syr, syawr, 1, [sx], [sy], [syaw], [1], 0.0, 0.0, -1)
    ngoal = Node(gxr, gyr, gyawr, 1, [gx], [gy], [gyaw], [1], 0.0, 0.0, -1)

    kdtree = kd.KDTree([[x, y] for x, y in zip(ox, oy)])
    P = calc_parameters(ox, oy, xyreso, yawreso, kdtree)

    hmap = astar.calc_holonomic_heuristic_with_obstacle(ngoal, P.ox, P.oy, P.xyreso, 1.0)
    steer_set, direc_set = calc_motion_set()
    open_set, closed_set = {calc_index(nstart, P): nstart}, {}

    qp = QueuePrior()
    qp.put(calc_index(nstart, P), calc_hybrid_cost(nstart, hmap, P))

    while True:
        if not open_set:
            return None

        ind = qp.get()
        n_curr = open_set[ind]
        closed_set[ind] = n_curr
        open_set.pop(ind)

        update, fpath = update_node_with_analystic_expantion(n_curr, ngoal, P)

        if update:
            fnode = fpath
            break

        for i in range(len(steer_set)):
            node = calc_next_node(n_curr, ind, steer_set[i], direc_set[i], P)

            if not node:
                continue

            node_ind = calc_index(node, P)

            if node_ind in closed_set:
                continue

            if node_ind not in open_set:
                open_set[node_ind] = node
                qp.put(node_ind, calc_hybrid_cost(node, hmap, P))
            else:
                if open_set[node_ind].cost > node.cost:
                    open_set[node_ind] = node
                    qp.put(node_ind, calc_hybrid_cost(node, hmap, P))

    return extract_path(closed_set, fnode, nstart)


def extract_path(closed, ngoal, nstart):
    rx, ry, ryaw, direc = [], [], [], []
    cost = 0.0
    node = ngoal

    while True:
        rx += node.x[::-1]
        ry += node.y[::-1]
        ryaw += node.yaw[::-1]
        direc += node.directions[::-1]
        cost += node.cost

        if is_same_grid(node, nstart):
            break

        node = closed[node.pind]

    rx = rx[::-1]
    ry = ry[::-1]
    ryaw = ryaw[::-1]
    direc = direc[::-1]

    direc[0] = direc[1]
    path = Path(rx, ry, ryaw, direc, cost)

    return path


def calc_next_node(n_curr, c_id, u, d, P):
    step = C.XY_RESO * 2

    nlist = math.ceil(step / C.MOVE_STEP)
    xlist = [n_curr.x[-1] + d * C.MOVE_STEP * math.cos(n_curr.yaw[-1])]
    ylist = [n_curr.y[-1] + d * C.MOVE_STEP * math.sin(n_curr.yaw[-1])]
    yawlist = [rs.pi_2_pi(n_curr.yaw[-1] + d * C.MOVE_STEP / C.WB * math.tan(u))]

    for i in range(nlist - 1):
        xlist.append(xlist[i] + d * C.MOVE_STEP * math.cos(yawlist[i]))
        ylist.append(ylist[i] + d * C.MOVE_STEP * math.sin(yawlist[i]))
        yawlist.append(rs.pi_2_pi(yawlist[i] + d * C.MOVE_STEP / C.WB * math.tan(u)))

    xind = round(xlist[-1] / P.xyreso)
    yind = round(ylist[-1] / P.xyreso)
    yawind = round(yawlist[-1] / P.yawreso)

    if not is_index_ok(xind, yind, xlist, ylist, yawlist, P):
        return None

    cost = 0.0

    if d > 0:
        direction = 1
        cost += abs(step)
    else:
        direction = -1
        cost += abs(step) * C.BACKWARD_COST

    if direction != n_curr.direction:  # switch back penalty
        cost += C.GEAR_COST

    cost += C.STEER_ANGLE_COST * abs(u)  # steer angle penalyty
    cost += C.STEER_CHANGE_COST * abs(n_curr.steer - u)  # steer change penalty
    cost = n_curr.cost + cost

    directions = [direction for _ in range(len(xlist))]

    node = Node(xind, yind, yawind, direction, xlist, ylist,
                yawlist, directions, u, cost, c_id)

    return node


def is_index_ok(xind, yind, xlist, ylist, yawlist, P):
    if xind <= P.minx or \
            xind >= P.maxx or \
            yind <= P.miny or \
            yind >= P.maxy:
        return False

    ind = range(0, len(xlist), C.COLLISION_CHECK_STEP)

    nodex = [xlist[k] for k in ind]
    nodey = [ylist[k] for k in ind]
    nodeyaw = [yawlist[k] for k in ind]

    if is_collision(nodex, nodey, nodeyaw, P):
        return False

    return True


def update_node_with_analystic_expantion(n_curr, ngoal, P):
    path = analystic_expantion(n_curr, ngoal, P)  # rs path: n -> ngoal

    if not path:
        return False, None

    fx = path.x[1:-1]
    fy = path.y[1:-1]
    fyaw = path.yaw[1:-1]
    fd = path.directions[1:-1]

    fcost = n_curr.cost + calc_rs_path_cost(path)
    fpind = calc_index(n_curr, P)
    fsteer = 0.0

    fpath = Node(n_curr.xind, n_curr.yind, n_curr.yawind, n_curr.direction,
                 fx, fy, fyaw, fd, fsteer, fcost, fpind)

    return True, fpath


def analystic_expantion(node, ngoal, P):
    sx, sy, syaw = node.x[-1], node.y[-1], node.yaw[-1]
    gx, gy, gyaw = ngoal.x[-1], ngoal.y[-1], ngoal.yaw[-1]

    maxc = math.tan(C.MAX_STEER) / C.WB
    paths = rs.calc_all_paths(sx, sy, syaw, gx, gy, gyaw, maxc, step_size=C.MOVE_STEP)

    if not paths:
        return None

    pq = QueuePrior()
    for path in paths:
        pq.put(path, calc_rs_path_cost(path))

    while not pq.empty():
        path = pq.get()
        ind = range(0, len(path.x), C.COLLISION_CHECK_STEP)

        pathx = [path.x[k] for k in ind]
        pathy = [path.y[k] for k in ind]
        pathyaw = [path.yaw[k] for k in ind]

        if not is_collision(pathx, pathy, pathyaw, P):
            return path

    return None


def is_collision(x, y, yaw, P):
    for ix, iy, iyaw in zip(x, y, yaw):
        d = 1
        dl = (C.RF - C.RB) / 2.0
        r = (C.RF + C.RB) / 2.0 + d

        cx = ix + dl * math.cos(iyaw)
        cy = iy + dl * math.sin(iyaw)

        ids = P.kdtree.query_ball_point([cx, cy], r)

        if not ids:
            continue

        for i in ids:
            xo = P.ox[i] - cx
            yo = P.oy[i] - cy
            dx = xo * math.cos(iyaw) + yo * math.sin(iyaw)
            dy = -xo * math.sin(iyaw) + yo * math.cos(iyaw)

            if abs(dx) < r and abs(dy) < C.W / 2 + d:
                return True

    return False


def calc_rs_path_cost(rspath):
    cost = 0.0

    for lr in rspath.lengths:
        if lr >= 0:
            cost += 1
        else:
            cost += abs(lr) * C.BACKWARD_COST

    for i in range(len(rspath.lengths) - 1):
        if rspath.lengths[i] * rspath.lengths[i + 1] < 0.0:
            cost += C.GEAR_COST

    for ctype in rspath.ctypes:
        if ctype != "S":
            cost += C.STEER_ANGLE_COST * abs(C.MAX_STEER)

    nctypes = len(rspath.ctypes)
    ulist = [0.0 for _ in range(nctypes)]

    for i in range(nctypes):
        if rspath.ctypes[i] == "R":
            ulist[i] = -C.MAX_STEER
        elif rspath.ctypes[i] == "WB":
            ulist[i] = C.MAX_STEER

    for i in range(nctypes - 1):
        cost += C.STEER_CHANGE_COST * abs(ulist[i + 1] - ulist[i])

    return cost


def calc_hybrid_cost(node, hmap, P):
    cost = node.cost + \
           C.H_COST * hmap[node.xind - P.minx][node.yind - P.miny]

    return cost


def calc_motion_set():
    s = np.arange(C.MAX_STEER / C.N_STEER,
                  C.MAX_STEER, C.MAX_STEER / C.N_STEER)

    steer = list(s) + [0.0] + list(-s)
    direc = [1.0 for _ in range(len(steer))] + [-1.0 for _ in range(len(steer))]
    steer = steer + steer

    return steer, direc


def is_same_grid(node1, node2):
    if node1.xind != node2.xind or \
            node1.yind != node2.yind or \
            node1.yawind != node2.yawind:
        return False

    return True


def calc_index(node, P):
    ind = (node.yawind - P.minyaw) * P.xw * P.yw + \
          (node.yind - P.miny) * P.xw + \
          (node.xind - P.minx)

    return ind


def calc_parameters(ox, oy, xyreso, yawreso, kdtree):
    minx = round(min(ox) / xyreso)
    miny = round(min(oy) / xyreso)
    maxx = round(max(ox) / xyreso)
    maxy = round(max(oy) / xyreso)

    xw, yw = maxx - minx, maxy - miny

    minyaw = round(-C.PI / yawreso) - 1
    maxyaw = round(C.PI / yawreso)
    yaww = maxyaw - minyaw

    return Para(minx, miny, minyaw, maxx, maxy, maxyaw,
                xw, yw, yaww, xyreso, yawreso, ox, oy, kdtree)



def add_obstacles(x1, y1, x2, y2, face, ox, oy, ox_face, oy_face):

    # SOUTH FACE
    for i in range(x1, x2):
        ox.append(i)
        oy.append(y1)

    if face == Angle.TWO_SEVENTY_DEG:
        for i in range(x1, x2+1):
            ox_face.append(i)
            oy_face.append(y1)
    
    # EAST FACE
    for i in range(y1, y2):
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
    for i in range(y1, y2):
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
    ox_face, oy_face = [], []

    draw_arena_box(x+1, y+1, ox, oy)

    for obstacle in obstacles:
        obs_x1 = obstacle[0]
        obs_y1 = obstacle[1]
        obs_x2 = obs_x1 + OBS_LENGTH
        obs_y2 = obs_y1 + OBS_LENGTH
        face = obstacle[2]

        p1 = (obs_x1, obs_y1)
        p2 = (obs_x2, obs_y1)
        p3 = (obs_x2, obs_y2)
        p4 = (obs_x1, obs_y2)

        add_obstacles(obs_x1,obs_y1, obs_x2,obs_y2, face, ox,oy, ox_face,oy_face)

    return ox, oy, ox_face, oy_face


def generate_waypoints(start_pos, obstacles):
    waypoints = {0: start_pos}
    i = 1

    for obstacle in obstacles:
        x1, y1, face = obstacle

        if face == Angle.ZERO_DEG:
            w_x = x1 + OBS_LENGTH + TOL_SPACE
            w_y = y1 + OBS_LENGTH // 2
            w_face = Angle.ONE_EIGHTY_DEG

        elif face == Angle.ONE_EIGHTY_DEG:
            w_x = x1 - TOL_SPACE
            w_y = y1 + OBS_LENGTH // 2
            w_face = Angle.ZERO_DEG

        elif face == Angle.NINETY_DEG:
            w_x = x1 + OBS_LENGTH // 2
            w_y = y1 + OBS_LENGTH + TOL_SPACE
            w_face = Angle.TWO_SEVENTY_DEG

        elif face == Angle.TWO_SEVENTY_DEG:
            w_x = x1 + OBS_LENGTH // 2
            w_y = y1 - TOL_SPACE
            w_face = Angle.NINETY_DEG
            
        # w_face = face + ONE_EIGHTY_DEG

        # if w_face >= (THREE_SIXTY_DEG - 0.1):
        #     w_face -= THREE_SIXTY_DEG
    
        waypoints[i] = (w_x, w_y, w_face)
        i += 1

    return waypoints


def find_distance(ox, oy):
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
            path = hybrid_astar_planning(sx, sy, syaw0, gx, gy, gyaw0,
                                    ox, oy, C.XY_RESO, C.YAW_RESO)

            dist = find_distance(path.x, path.y)

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
        
        #print(f"{path}: {dist}")

    #print(f"{min_path} has the shortest distance of {min_dist}")

    # get the path in terms of waypoints (currently it is still in labels)
    waypoints = []
    for node in min_path:
        waypoints.append(waypoint_dict[node])

    return waypoints

def solve(obstacles):
    ox, oy, ox_face, oy_face = design_obstacles(X, Y, obstacles)
    waypoint_dict = generate_waypoints(CAR_START_POS, obstacles)
    dist_vector = get_dist_bet_waypoints(waypoint_dict, ox, oy)
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
            print(f"{tour[i]} and {tour[i+1]} don't have a path!")
            return

        paths.append(path)

    return paths

import matplotlib.pyplot as plt
import math
from typing import List
import imageio
import os

from algorithm.planner.algorithms.hybrid_astar.core import reeds_shepp as rs
from algorithm.planner.algorithms.hybrid_astar.draw.draw import draw_car
from algorithm.planner.results.results_handler import increment_id
from algorithm.planner.entity.arena import Arena
from algorithm.planner.entity.path import Path

from algorithm.planner.utils.car_utils import Car_C
from algorithm.planner.algorithms.hybrid_astar.params import C

# Given the paths and the obstacles (arena + car start pos is defined in utils),
# either show plt simulation or save as gif
def simulate(tour: List[Path], arena:Arena, 
             save_gif=False, gif_name=None, keep_files=False):

    if gif_name == None:
        id = increment_id("gif")
        gif_name = f"./results/gif/{id}.gif"

    ox, oy, ox_face, oy_face = arena.design_obstacles()

    print("Simulation started")

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
        last_x = [path.x[-1]] * 5
        last_y = [path.y[-1]] * 5
        last_yaw = [path.yaw[-1]] * 5
        last_direction = [path.direction[-1]] * 5

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
        plt.plot(x, y, linewidth=1.5, color='r')

        if k < len(x) - 2:
            dy = (yaw[k + 1] - yaw[k]) / C.MOVE_STEP
            steer = rs.pi_2_pi(math.atan(-Car_C.WB * dy / direction[k]))
        else:
            steer = 0.0

        draw_car(x[k], y[k], yaw[k], steer)
        plt.title("Hybrid A*")
        plt.axis("equal")
        plt.grid(b=True)

        if save_gif:
            filename = f"./{k}.png"
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

    print("Simulation saved")

# Save the arena image
# Used when there is no path found (error), and we want to see which obstacle combinations lead to this error
def save_arena_img(arena: Arena, error=False):

    ox, oy, ox_face, oy_face = arena.design_obstacles()

    car_x, car_y, car_direction = arena.get_start_pos()
    draw_car(car_x, car_y, car_direction, 0)
    plt.plot(ox, oy, "sk")
    plt.plot(ox_face, oy_face, "sy")
    plt.title("Arena")
    plt.axis("equal")
    plt.grid(b=True)

    if error:
        id = increment_id("error")
        filename = f"./results/error_arena/{id}.png"
    else:
        id = increment_id("valid")
        filename = f"./results/valid_arena/{id}.png"

    plt.savefig(filename)
    plt.close()

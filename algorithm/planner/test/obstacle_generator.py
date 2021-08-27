from HybridAstarPlanner.angles import Angle
import random

X, Y = 40, 40

def make_obstacle(X, Y):
    pass


def is_valid_obstacle(obstacle, list_of_obstacles):
    return True



def generate_obstacles(num_of_obstacles):
    obstacles = []
    i = 0

    while i < num_of_obstacles:
        obstacle = make_obstacle(X, Y)

        if not is_valid_obstacle(obstacle, obstacles):
            continue
        else:
            i += 1

    return obstacles

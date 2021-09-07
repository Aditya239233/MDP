from HybridAstarPlanner.utils import Angle
import random

X, Y = 40, 40

def make_obstacle(X, Y):
    pass


def is_valid_obstacle(obstacle, list_of_obstacles):
    return True



def generate_obstacles(num_of_obstacles):

    import random
    i = random.randint(0,2)
    obstacles = [[(10, 14, Angle.TWO_SEVENTY_DEG),
                 (20, 20, Angle.ONE_EIGHTY_DEG),
                 (30, 30, Angle.ONE_EIGHTY_DEG),
                 (36, 34, Angle.TWO_SEVENTY_DEG),
                 (8, 30, Angle.TWO_SEVENTY_DEG)],

                [(14, 14, Angle.ONE_EIGHTY_DEG),
                 (20, 20, Angle.ONE_EIGHTY_DEG),
                 (30, 30, Angle.TWO_SEVENTY_DEG),
                 (36, 34, Angle.TWO_SEVENTY_DEG),
                 (8, 20, Angle.TWO_SEVENTY_DEG)],

                 [(10, 14, Angle.ZERO_DEG),
                 (20, 20, Angle.ZERO_DEG),
                 (10, 30, Angle.ONE_EIGHTY_DEG),
                 (36, 34, Angle.ONE_EIGHTY_DEG),
                 (8, 30, Angle.TWO_SEVENTY_DEG)],
                ]
    return obstacles[i]

    obstacles = []
    i = 0

    while i < num_of_obstacles:
        obstacle = make_obstacle(X, Y)

        if not is_valid_obstacle(obstacle, obstacles):
            continue
        else:
            i += 1

    return obstacles

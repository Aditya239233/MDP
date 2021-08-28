from HybridAstarPlanner.solver import save_arena_img, solve, simulate, save_arena_img
from HybridAstarPlanner.utils import Angle
from test.planner_test import PlannerTest

import traceback

def get_obstacles():
    import random
    i = random.randint(0,2)
    obstacles = [[(10, 14, Angle.TWO_SEVENTY_DEG),
                 (20, 20, Angle.ONE_EIGHTY_DEG),
                 (30, 30, Angle.ONE_EIGHTY_DEG),
                 (36, 34, Angle.TWO_SEVENTY_DEG),
                 (8, 30, Angle.TWO_SEVENTY_DEG)],

                [(35, 14, Angle.ONE_EIGHTY_DEG),
                 (20, 25, Angle.ONE_EIGHTY_DEG),
                 (30, 34, Angle.TWO_SEVENTY_DEG),
                 (36, 34, Angle.TWO_SEVENTY_DEG),
                 (8, 35, Angle.TWO_SEVENTY_DEG),
                 #(6, 20, Angle.TWO_SEVENTY_DEG)
                 ],

                 [(10, 14, Angle.ZERO_DEG),
                 (20, 20, Angle.ZERO_DEG),
                 (10, 30, Angle.ZERO_DEG),
                 (36, 34, Angle.ONE_EIGHTY_DEG),
                 (8, 30, Angle.TWO_SEVENTY_DEG)],
                ]

    
    return obstacles[2]


def run():
    obstacles = get_obstacles()

    try:
        paths = solve(obstacles)
        print(paths[0].x)
    except Exception as e:
        print(e)

def run_tests():

    pt = PlannerTest(num_tests=3)
    pt.start()
    
    results = pt.get_results()
    print(f"Errors: {results}")

obstacles = get_obstacles()
try:
    paths = solve(obstacles)
    simulate(paths, obstacles, keep_files=True, save_gif=True)
    # simulate(paths, obstacles)
except Exception as e:
    traceback.print_exc()
    print(e)
    save_arena_img(obstacles)
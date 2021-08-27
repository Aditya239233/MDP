from HybridAstarPlanner.hybrid_astar import solve, simulate, Path
from HybridAstarPlanner.angles import Angle
from test.planner_test import PlannerTest

def get_obstacles():
    obstacles = [(10, 14, Angle.TWO_SEVENTY_DEG),
                 (20, 20, Angle.ONE_EIGHTY_DEG),
                 (30, 30, Angle.ONE_EIGHTY_DEG),
                 (36, 34, Angle.TWO_SEVENTY_DEG),
                 (8, 30, Angle.TWO_SEVENTY_DEG)
                ]
    
    return obstacles


def run():
    obstacles = get_obstacles()

    try:
        paths = solve(obstacles)
        print(paths[0].x)
    except Exception as e:
        print(e)

def run_tests():

    pt = PlannerTest(num_tests=1e3)
    pt.start()
    
    pt.get_results()


#run()

obstacles = get_obstacles()
paths = solve(obstacles)
simulate(paths, obstacles, save_gif=True)
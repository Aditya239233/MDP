from HybridAstarPlanner.hybrid_astar import solve, Path
from HybridAstarPlanner.angles import Angle

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
    paths = solve(obstacles)

    print(paths[0].x)

run()
from .obstacle_generator import generate_obstacles
from HybridAstarPlanner.solver import solve, simulate

class PlannerTest:

    def __init__(self, num_tests=1e3):
        self.num_tests = num_tests

    def start(self, num_obstacles=5):
        self.errors_in_planner = 0

        for i in range(self.num_tests):
            obstacles = generate_obstacles(num_obstacles)
            filename = f'./gif/{i}.gif'

            try:
                paths = solve(obstacles)
                simulate(paths, obstacles, no_gui=True, save_gif=True, gif_name=filename)
            except Exception as e:
                print(e)
                self.errors_in_planner += 1
    
    def get_results(self):

        if self.errors_in_planner == None:
            return -1
        else:
            return self.errors_in_planner
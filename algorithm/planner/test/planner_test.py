from matplotlib.pyplot import draw
from .obstacle_generator import generate_obstacles
from HybridAstarPlanner.solver import solve, save_arena_img, simulate

class PlannerTest:

    def __init__(self, num_tests=1e3):
        self.num_tests = num_tests

    def start(self, num_obstacles=5):
        self.errors_in_planner = 0

        for i in range(self.num_tests):
            print(f"On {i}")
            obstacles = generate_obstacles(num_obstacles)
            print("Obstacles generated")

            try:
                paths = solve(obstacles)
                print(f"{i} solved")
                save_arena_img(obstacles, error=False)
                # simulate(paths, obstacles, save_gif=True)
            except Exception as e:
                print(e)
                save_arena_img(obstacles, error=True)
                self.errors_in_planner += 1

        print(f"Number of errors: {self.errors_in_planner}")
    
    def get_results(self):

        if self.errors_in_planner == None:
            return -1
        else:
            return self.errors_in_planner

    def test_custom(self, obstacles):
        try:
            paths = solve(obstacles)
            simulate(paths, obstacles, save_gif=True, gif_name="./results/gif/custom.gif")
        except Exception as e:
            print(e)
            save_arena_img(obstacles, error=True)

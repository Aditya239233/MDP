from translate import translate_tour
from HybridAstarPlanner.solver import solve
from HybridAstarPlanner.utils import Angle
from test.planner_test import PlannerTest

import pickle
class Planner:
    
    def __init__(self):
        self.job_id = 0
        self.obstacles = None
        self.cache = {} # store previous results

    def set_obstacles(self, obstacles):
        self.obstacles = obstacles
    
    def run_job(self):
        if self.obstacles == None:
            raise Exception("Obstacles not defined")
        else:
            try:
                paths = solve(self.obstacles)
            except Exception as e:
                print(f"Job {self.job_id} has no results.")
                paths = None
            finally:
                self.cache[self.job_id] = paths
                self.job_id += 1
                self.obstacles = None

                return self.job_id-1  # return previous job id

    def get_instructions(self, job_id):

        tour = self.cache[job_id]

        if tour != None:
            return translate_tour(tour)
        else:
            return None

obstacle = [(32, 31, Angle.TWO_SEVENTY_DEG),
(18, 16, Angle.ONE_EIGHTY_DEG),
(9, 33, Angle.ZERO_DEG),
(17, 24, Angle.ZERO_DEG),
(28, 21, Angle.TWO_SEVENTY_DEG)]

# Example
p = Planner()
p.set_obstacles(obstacle)
job_id = p.run_job()
intructions = p.get_instructions(job_id)
print(intructions)

# from HybridAstarPlanner.solver import simulate
# simulate(p.get_job(0), obstacle, save_gif=True, gif_name="./results/gif/fourth.gif")


# for short testing (not used in production)
#obstacles = [[(10, 14, Angle.TWO_SEVENTY_DEG),
                #  (20, 20, Angle.ONE_EIGHTY_DEG),
                #  (30, 30, Angle.ONE_EIGHTY_DEG),
                #  (36, 34, Angle.TWO_SEVENTY_DEG),
                #  (8, 30, Angle.TWO_SEVENTY_DEG)],

                # [(35, 14, Angle.ONE_EIGHTY_DEG),
                #  (20, 25, Angle.ONE_EIGHTY_DEG),
                #  (30, 34, Angle.TWO_SEVENTY_DEG),
                #  (36, 34, Angle.TWO_SEVENTY_DEG),
                #  (8, 35, Angle.TWO_SEVENTY_DEG),
                #  #(6, 20, Angle.TWO_SEVENTY_DEG)
                #  ],

                #  [(10, 14, Angle.ZERO_DEG),
                #  (20, 20, Angle.ZERO_DEG),
                #  (10, 30, Angle.ZERO_DEG),
                #  (36, 34, Angle.ONE_EIGHTY_DEG),
                #  (8, 30, Angle.TWO_SEVENTY_DEG)],
                # ]

# obstacle = [(32, 31, Angle.TWO_SEVENTY_DEG),
# (18, 16, Angle.ONE_EIGHTY_DEG),
# (9, 33, Angle.ZERO_DEG),
# (17, 24, Angle.ZERO_DEG),
# (28, 21, Angle.TWO_SEVENTY_DEG)]



# # Test Example
# pt = PlannerTest(num_tests=2)
# # pt.start()
# pt.test_custom(obstacle)

# tour = pickle.load(open("./results/valid_paths/tour0.pkl", "rb"))
# from HybridAstarPlanner.solver import simulate
# simulate(tour, obstacle, save_gif=True, gif_name="./results/gif/tour0.gif")

# # for path in tour:
# #     for i in range(len(path.x)):
# #         print(f"{path.x[i] :.3f}, {path.y[i] :.3f}, {path.direction[i]}, {path.yaw[i] :.3f}, {path.steer[i] :.3f}")

# #     print("\n\n")
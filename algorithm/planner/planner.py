from HybridAstarPlanner.solver import solve
from HybridAstarPlanner.utils import Angle

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

    def get_job(self, job_id):
        return self.cache[job_id]
    


# for short testing (not used in production)
def get_obstacles():
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

# Example
p = Planner()
obs = get_obstacles()
p.set_obstacles(obs)
p.run_job()

from HybridAstarPlanner.solver import simulate
simulate(p.get_job(0), obs, save_gif=True)
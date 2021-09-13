from translate import translate_tour
from HybridAstarPlanner.solver import solve
from HybridAstarPlanner.utils import Angle
from test.planner_test import PlannerTest
from flask import *
import json, time, ast

app = Flask(__name__)

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

    def get_job(self, job_id):
        return self.cache[job_id]
    def get_path(self, job_id):
        path = []
        for i in self.cache[job_id]:
            for j in range(len(i.x)):
                lst = []
                lst.append(i.x[j])
                lst.append(i.y[j])
                lst.append(i.yaw[j]) 
                path.append(lst)
            path.append([-1,-1,-1])
                
        return path


# api function
@app.route('/get-path/', methods=['GET'])
def get_path_coor():
    obstacles = str(request.args.get('obstacles')) #/get-path/?obstacles=[10,20,etc]
    obstacles = ast.literal_eval(obstacles)
    print(obstacles)

    angleDict = {
        'N': Angle.NINETY_DEG,
        'E': Angle.ZERO_DEG,
        'S': Angle.TWO_SEVENTY_DEG,
        'W': Angle.ONE_EIGHTY_DEG
    }

    for i in range(len(obstacles)):
        curr = obstacles[i]
        print(curr)
        obstacles[i] = (curr[0], curr[1],angleDict[curr[2]] )
        
    print(obstacles)
    p = Planner()
    # obs = get_obstacles()
    p.set_obstacles(obstacles)
    p.run_job()
    data = {'status': "success", "data": p.get_path(0)}
    json_dump = json.dumps(data)
    return Response(json_dump, mimetype='application/json; charset=utf-8')

if __name__ == '__main__':
    app.run(port=3000)


# obstacle = [(32, 31, Angle.TWO_SEVENTY_DEG),
# (18, 16, Angle.ONE_EIGHTY_DEG),
# (9, 33, Angle.ZERO_DEG),
# (17, 24, Angle.ZERO_DEG),
# (28, 21, Angle.TWO_SEVENTY_DEG)]

# # Example
# p = Planner()
# p.set_obstacles(obstacle)
# job_id = p.run_job()
# intructions = p.get_instructions(job_id)
# print(intructions)

# tour = p.get_job(0)
# # from HybridAstarPlanner.solver import simulate
# # simulate(p.get_job(0), obstacle, save_gif=True, gif_name="./results/gif/fourth.gif")
# for path in tour:
#     for i in range(len(path.x)):
#         print(f"{path.x[i] :.3f}, {path.y[i] :.3f}, {path.direction[i]}, {path.yaw[i] :.3f}, {path.steer[i] :.3f}")

#     print("\n\n")






















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
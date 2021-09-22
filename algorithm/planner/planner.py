from translate import translate_tour
from HybridAstarPlanner.solver import solve
from HybridAstarPlanner.utils import Angle
from test.planner_test import PlannerTest
from flask import *
import json, time, ast
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

app = Flask(__name__)
planner = Planner()

# api function
@app.route('/get-path/', methods=['GET'])
def get_path_coor():
    obstacles = str(request.args.get('obstacles')) #/get-path/?obstacles=[10,20,etc]
    obstacles = ast.literal_eval(obstacles)

    angleDict = {
        'N': Angle.NINETY_DEG,
        'E': Angle.ZERO_DEG,
        'S': Angle.TWO_SEVENTY_DEG,
        'W': Angle.ONE_EIGHTY_DEG
    }

    for i in range(len(obstacles)):
        curr = obstacles[i]
        obstacles[i] = (curr[0], curr[1],angleDict[curr[2]] )
        
    print(obstacles)
    # obs = get_obstacles()
    planner.set_obstacles(obstacles)
    curr_job_id = planner.run_job()
    data = {'status': "success", "data": planner.get_path(curr_job_id), "id": curr_job_id}
    json_dump = json.dumps(data)
    return Response(json_dump, mimetype='application/json; charset=utf-8')

@app.route('/get-instructions/', methods=['GET'])
def get_instructions():
    job_id = str(request.args.get("id"))  #/get-path/?id=1

    if not job_id.isdigit():
        return Response(status=404)
    else:
        job_id = int(job_id)

    instructions = planner.get_instructions(job_id)

    if instructions != None:
        json_dump = json.dumps(instructions)
        return Response(json_dump, mimetype='application/json; charset=utf-8')
    else:
        return Response(status=404)


if __name__ == "__main__":
    app.run(port=3000)
from utils.helpers import get_angle_from_direction
from planner import Planner
from flask import *
import json, ast

app = Flask(__name__)
planner = Planner()

# api function
@app.route('/get-path/', methods=['GET'])
def get_path_coor():
    list_of_obstacles = str(request.args.get('obstacles')) #/get-path/?obstacles=[[10,20,'N'], [etc]]
    list_of_obstacles = ast.literal_eval(list_of_obstacles)
    obstacles = []

    for obstacle in list_of_obstacles:
        x, y, face = obstacle
        face = get_angle_from_direction(face)

        obstacles.append((x, y, face))

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
from flask import Flask, jsonify, request
from flask_restful import reqparse, Resource, Api
from random import randint
from path_planner import PathPlanner
import _thread

app = Flask(__name__)
api = Api(app)

path_planner = PathPlanner()
_thread.start_new_thread(path_planner.start, ())

class Job(Resource):
    def get(self):
        curr_id = path_planner.get_id()
        curr_id = str(curr_id)
        return {'job-id': curr_id}, 200

class Planner(Resource):
    def post(self):
        data = request.get_json()
        new_id = path_planner.add_job(data)
        new_id = str(new_id)
        return {'job-id': new_id}, 200

class Cache(Resource):
    def get(self, id):
        res = {}
        id = int(id)
        actions = path_planner.get_cache(id)
        if actions != None:
            res['done'] = "true"
        print(actions)
        res['actions'] = actions
        return res, 200

class Arena(Resource):
    def get(self):
        data = path_planner.get_arena()
        return {'arena': data}, 200

api.add_resource(Job, '/')
api.add_resource(Planner, '/planner')
api.add_resource(Cache, '/job/<string:id>')
api.add_resource(Arena, '/arena')

if __name__ == "__main__":
    app.run(debug=True)
from algorithm.planner.utils.helpers import get_direction_from_angle
from typing import List
from algorithm.planner.testset import TestSet
from algorithm.planner.algorithms.hybrid_astar.solver import solve
from algorithm.planner.utils.translate import translate_tour
from algorithm.planner.entity.obstacle import Obstacle
from algorithm.planner.entity.arena import Arena
from algorithm.planner.utils.car_utils import Car_C
from algorithm.planner.algorithms.hybrid_astar.simulate import simulate

# Planner class for the Flask server
# Does not support string-to-pos translation
# Takes in a list of obstacles (in tuples) - no obs id is needed
class Planner:
    
    def __init__(self):
        self.job_id = 0
        self.arena = None
        self.cache = {} # store previous results

    def set_arena(self, arena):
        self.arena = arena

    def init_arena(self, obstacles, start_pos=None):
        if start_pos == None:
            start_pos = Car_C.START_POS

        obstacles = self.convert_obstacles(obstacles)
        
        self.arena = Arena()
        self.arena.set_obstacles(obstacles)
        self.arena.set_start_pos(start_pos)

        return self.arena
    
    def run_job(self):
        if self.arena == None:
            raise Exception("Arena not defined")
        else:
            try:
                paths, tour_seq = solve(self.arena)
            except Exception as e:
                print(f"Job {self.job_id} has no results.")
                paths = tour_seq = None
            finally:
                self.cache[self.job_id] = (paths, tour_seq)
                self.job_id += 1
                self.obstacles = None

                return self.job_id-1  # return previous job id

    def get_instructions(self, job_id):

        tour, tour_seq = self.cache[job_id]
        if tour != None:
            instructions, _ = translate_tour(tour, tour_seq)
            return instructions
        else:
            return None

    def get_tour_from_job(self, job_id):
        return self.cache[job_id][0]

    def get_path(self, job_id):
        path = []

        for path in self.cache[job_id][0]:
            for i in range(len(path.x)):
                x = path.x[i]
                y = path.y[i]
                yaw = path.yaw[i]

                path.append([x, y, yaw])

            path.append([-1,-1,-1])
                
        return path

    # Convert list of obstacles defined in TestSet into list of Obstacle objects to use in Arena
    def convert_obstacles(self, obstacles):
        img_id = 0 # image id
        arr = []

        for obstacle in obstacles:
            x, y, face_angle = obstacle
            obs = Obstacle(x, y, face_angle, img_id)
            arr.append(obs)

            img_id += 1

        return arr


# Example
if __name__ == "__main__":

    def print_instructions(instructions):
        if instructions == None:
            return

        for i in instructions:
            print(i)
    
    def print_real_obs_coor(obstacles: List[List]):
        scale = 10
        for obs in obstacles:
            x = obs[0] * scale
            y = obs[1] * scale
            direction = get_direction_from_angle(obs[2])
            print(f"({x}, {y}, {direction})")

    p = Planner()
    obstacles = TestSet.obstacles
    print_real_obs_coor(obstacles)

    arena = p.init_arena(obstacles)
    job_id = p.run_job()
    
    tour = p.get_tour_from_job(job_id)
    # for path in tour:
    #     for i in range(len(path.x)):
    #         print(f"{path.x[i] :.3f}, {path.y[i] :.3f}, {path.direction[i]}, {path.yaw[i] :.3f}, {path.steer[i] :.3f}")
    #     print("\n\n")
            
    instructions = p.get_instructions(job_id)
    print_instructions(instructions)

    #simulate(tour, arena, save_gif=True, gif_name="./apollo2.gif")


    

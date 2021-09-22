from testset import TestSet
from algorithms.hybrid_astar.solver import solve
from utils.translate import translate_tour
from entity.obstacle import Obstacle
from entity.arena import Arena
from utils.car_utils import Car_C
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
        for i in instructions:
            print(i)

    p = Planner()
    obstacles = TestSet.obstacles
    arena = p.init_arena(obstacles)
    job_id = p.run_job()
    instructions = p.get_instructions(job_id)
    print_instructions(instructions)

    tour = p.get_tour_from_job(job_id)
    from algorithms.hybrid_astar.simulate import simulate
    simulate(tour, arena, save_gif=True, gif_name="./results/gif/apollo1.gif")
    # for path in tour:
    #     for i in range(len(path.x)):
    #         print(f"{path.x[i] :.3f}, {path.y[i] :.3f}, {path.direction[i]}, {path.yaw[i] :.3f}, {path.steer[i] :.3f}")

    #     print("\n\n")
# For testing/running the algorithm
from algorithm.planner.utils.translate import translate_tour
from algorithm.planner.utils.helpers import get_angle_from_direction
from algorithm.planner.utils.arena_utils import Arena_C

from algorithm.planner.entity.arena import Arena
from algorithm.planner.entity.obstacle import Obstacle
from algorithm.planner.algorithms.hybrid_astar.solver import solve
from algorithm.planner.algorithms.hybrid_astar.simulate import simulate

# For running Task 1.
# This class is designed to run only once
class Runner:
    def __init__(self, data_str):
        car_start_pos, obstacles = self.process(data_str)
        self.arena = Arena()

        self.arena.set_obstacles(obstacles)
        self.arena.set_start_pos(car_start_pos)
        
        from algorithms.hybrid_astar.simulate import save_arena_img
        save_arena_img(self.arena, error=True)

    
    def run(self, to_simulate=False):
        tour, tour_sequence = solve(self.arena)

        if to_simulate:
            simulate(tour, self.arena, save_gif=True, gif_name="./results/gif/runner.gif")

        instructions, android_data = translate_tour(tour, tour_sequence)
        return instructions, android_data

    
    def process(self, data_str):
        split_str = data_str.split(";")
        obstacles = []

        for data in split_str:
            param = data.split(",")

            if param[0].upper() == "ROBOT":
                robot_x = int(param[1])
                robot_y = int(param[2])
                direction = get_angle_from_direction(param[3])

                start_pos = (robot_x, robot_y, direction)

            elif param[0].upper() == "OBSTACLE":
                obs_id = int(param[1])
                obs_x = int(param[2])
                obs_y = int(param[3])
                obs_direction = get_angle_from_direction(param[4])
                obs = Obstacle(obs_x, obs_y, obs_direction, obs_id)
                obstacles.append(obs)

        return start_pos, obstacles


if __name__ == "__main__":
    data_str = "ROBOT,1,1,N;OBSTACLE,1,11,10,W;OBSTACLE,2,0,5,N;OBSTACLE,3,6,18,S"
    runner = Runner(data_str)
    instructions, android_coor = runner.run(to_simulate=False)
    print(instructions)
    print(android_coor)
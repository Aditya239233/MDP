from planner import Planner
from HybridAstarPlanner.utils import Angle, C
from HybridAstarPlanner import solver

# Test
obstacles = [[32, 31, Angle.ONE_EIGHTY_DEG],
[18, 16, Angle.ZERO_DEG],
[9, 33, Angle.TWO_SEVENTY_DEG],
[17, 24, Angle.ONE_EIGHTY_DEG],
[28, 21, Angle.NINETY_DEG]]

#Test 2
# obstacles = [[10,14,Angle.TWO_SEVENTY_DEG],[20,14,Angle.TWO_SEVENTY_DEG],
# [30, 22,Angle.ZERO_DEG],[10,22,Angle.NINETY_DEG],[20,22,Angle.NINETY_DEG]]



#Test 4
# obstacles = [[10,8,Angle.ONE_EIGHTY_DEG],[10,16,Angle.ONE_EIGHTY_DEG],[10, 24,Angle.ONE_EIGHTY_DEG],
# [10,30,Angle.ONE_EIGHTY_DEG],[10,36,Angle.ONE_EIGHTY_DEG]]

# Test 5
# obstacles = [[32, 31, Angle.ONE_EIGHTY_DEG],
# [18, 16, Angle.ZERO_DEG],
# [9, 33, Angle.TWO_SEVENTY_DEG],
# [17, 24, Angle.ONE_EIGHTY_DEG],
# [28, 16, Angle.ZERO_DEG]]

def translate_val_to_sim(obstacles):
    for obs in obstacles:
        obs[0] += C.OFFSET_X
        obs[1] += C.OFFSET_Y

def translate_val_to_real(obstacles):
    real = []
    for obs in obstacles:
        t = []
        t.append(obs[0] * 5)
        t.append(obs[1] * 5)
        t.append(obs[2])
    
        real.append(t)

    return real

translate_val_to_sim(obstacles)

# Example
p = Planner()
p.set_obstacles(obstacles)
job_id = p.run_job()
intructions = p.get_instructions(job_id)
print(intructions)

tour = p.get_job(0)
from HybridAstarPlanner.solver import simulate
simulate(tour, obstacles, save_gif=True, gif_name="./results/gif/test.gif")
for path in tour:
    for i in range(len(path.x)):
        print(f"{path.x[i] :.3f}, {path.y[i] :.3f}, {path.direction[i]}, {path.yaw[i] :.3f}, {path.steer[i] :.3f}")

    print("\n\n")
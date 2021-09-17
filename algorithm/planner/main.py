from planner import Planner
from HybridAstarPlanner.utils import Angle

obstacle = [(32, 31, Angle.ONE_EIGHTY_DEG),
(18, 16, Angle.ZERO_DEG),
(9, 33, Angle.TWO_SEVENTY_DEG),
(17, 24, Angle.ONE_EIGHTY_DEG),
(28, 21, Angle.NINETY_DEG)]

# Example
p = Planner()
p.set_obstacles(obstacle)
job_id = p.run_job()
intructions = p.get_instructions(job_id)
print(intructions)

tour = p.get_job(0)
# from HybridAstarPlanner.solver import simulate
# simulate(p.get_job(0), obstacle, save_gif=True, gif_name="./results/gif/test.gif")
# for path in tour:
#     for i in range(len(path.x)):
#         print(f"{path.x[i] :.3f}, {path.y[i] :.3f}, {path.direction[i]}, {path.yaw[i] :.3f}, {path.steer[i] :.3f}")

#     print("\n\n")
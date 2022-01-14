from HybridAstarPlanner.utils import Angle
import random, math

# Assumption:
# Arena size: 40x40
# Obstacle is a square of 2x2
# Obstacle left corner can only be placed at (2n, 2n)
# No obstacle in left corner (6x6) as it is carpark
# Follows conventional coordinate system
# Positive x-direction is 0 degree

X, Y = 40, 40
size = 2

# if obstacle is on the arena border, then face generation is more troublesome
# else it will just be a simple rng
def generate_face(ox, oy):
    
    available_faces = set([Angle.ZERO_DEG,
                          Angle.NINETY_DEG,
                          Angle.ONE_EIGHTY_DEG,
                          Angle.TWO_SEVENTY_DEG])

    if ox <= 10: # near left border
        available_faces.remove(Angle.ONE_EIGHTY_DEG)

    if ox >= X-10: # near right border
        available_faces.remove(Angle.ZERO_DEG)
    
    if oy >= Y-10: # near top border
        available_faces.remove(Angle.NINETY_DEG)

    if oy <= 10: # near bottom border
        available_faces.remove(Angle.TWO_SEVENTY_DEG)
    

    faces = list(available_faces)
    face_index = random.randint(0, len(faces)-1) # randomly choose a face from available options

    return faces[face_index]


def make_obstacle(X, Y):

    ox = oy = 0

    # if ox and oy are in carpark, then keep trying
    ox = random.randint(8, X-size-4)
    oy = random.randint(8, Y-size-4)

    face = generate_face(ox, oy)

    return (ox, oy, face)

# For now, assume true. 
# Need to check proximity for other obstacles
def is_valid_obstacle(obstacle, list_of_obstacles):
    
    def is_near(o1, o2):

        MIN_DIST = 6  

        o1_x, o1_y = o1[0], o1[1]
        o2_x, o2_y = o2[0], o2[1]

        x2 = (o1_x - o2_x)**2
        y2 = (o1_y - o2_y)**2

        dist = math.sqrt(x2 + y2)

        if dist <= MIN_DIST:
            return True
        else:
            return False

    def face_each_other(o1, o2):
        return False

    for obs in list_of_obstacles:
        if obstacle == obs:
            continue

        if is_near(obstacle, obs):
            return False
        
        if face_each_other(obstacle, obs):
            return False

    return True


def generate_obstacles(num_of_obstacles):
    obstacles = []
    i = 0

    while i < num_of_obstacles:
        obstacle = make_obstacle(X, Y)

        if not is_valid_obstacle(obstacle, obstacles):
            continue
        else:
            obstacles.append(obstacle)
            i += 1

    return obstacles

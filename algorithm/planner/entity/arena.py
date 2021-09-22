from typing import List
from entity.obstacle import Obstacle
from utils.angles import Angle
from utils.arena_utils import Arena_C
from .obstacle import Obstacle

# Package all the information about the arena in a class
# The parameters (e.g size, etc) are in the utils folder

class Arena:

    def __init__(self):
        self.processed = False

    def set_obstacles(self, obstacles: List[Obstacle]):
        self.obstacles = obstacles

    def get_obstacles(self):
        return self.obstacles

    def set_start_pos(self, start_pos):
        self.start_pos = start_pos

    def get_start_pos(self):
        return self.start_pos

    # important to run this to make sure obstacles and robot start pos are adjusted from real to simulator values
    def process(self):
        if self.obstacles == None or self.processed:
            return

        for obs in self.obstacles:
            obs.translate_val_to_sim()
        
        s_x, s_y, direction = self.start_pos
        s_x += Arena_C.OFFSET_X
        s_y += Arena_C.OFFSET_Y

        self.start_pos = (s_x, s_y, direction)
        self.processed = True


    # The obstacles are defined using lists of values (ox - list of x-coordinates, etc)

    # Adds the arena + obstacles
    # Returns their coordinates lists
    def design_obstacles(self):
        self.process()

        x = Arena_C.X
        y = Arena_C.Y

        ox, oy = [], []
        ox_face, oy_face = [], [] # for showing obstacle face

        self._draw_arena_box(x+1, y+1, ox, oy)

        for obstacle in self.obstacles:
            obs_x1 = obstacle.x
            obs_y1 = obstacle.y
            obs_x2 = int(obs_x1 + Arena_C.OBS_LENGTH) - 1
            obs_y2 = int(obs_y1 + Arena_C.OBS_LENGTH) - 1
            face = obstacle.face

            self._add_obstacles(obs_x1,obs_y1, obs_x2,obs_y2, face, ox,oy, ox_face,oy_face)

        return ox, oy, ox_face, oy_face

    # Helper func: Add obstacle bot-left, top-right corners and face to the obstacle coors (ox, oy, ...)
    # Passes the return lists as parameters to avoid copying
    def _add_obstacles(self, x1, y1, x2, y2, face, ox: List, oy: List, ox_face: List, oy_face: List):

        # SOUTH FACE
        for i in range(x1, x2+1):
            ox.append(i)
            oy.append(y1)
        if face == Angle.TWO_SEVENTY_DEG:
            for i in range(x1, x2+1):
                ox_face.append(i)
                oy_face.append(y1)
        
        # EAST FACE
        for i in range(y1, y2+1):
            ox.append(x2)
            oy.append(i)
        if face == Angle.ZERO_DEG:
            for i in range(y1, y2+1):
                ox_face.append(x2)
                oy_face.append(i)
        
        # NORTH FACE
        
        for i in range(x1, x2+1):
            ox.append(i)
            oy.append(y2)
        if face == Angle.NINETY_DEG:
            for i in range(x1, x2+1):
                ox_face.append(i)
                oy_face.append(y2)

        # WEST FACE
        for i in range(y1, y2+1):
            ox.append(x1)
            oy.append(i)
        if face == Angle.ONE_EIGHTY_DEG:
            for i in range(y1, y2+1):
                ox_face.append(x1)
                oy_face.append(i)
        
    # Helper func: Define the bounding box for the arena as a huge rectangular obstacle
    # Passes the return lists as parameters to avoid copying
    def _draw_arena_box(self, x, y, ox: List, oy: List):
        for i in range(x):
            ox.append(i)
            oy.append(0)
        for i in range(x):
            ox.append(i)
            oy.append(y - 1)
        for i in range(y):
            ox.append(0)
            oy.append(i)
        for i in range(y):
            ox.append(x - 1)
            oy.append(i)
from utils.angles import Angle
from utils.arena_utils import Arena_C

class Obstacle:

    # face is an Angle value
    def __init__(self, x, y, face, id=0):
        self.x = x
        self.y = y
        self.face = face
        self.img_id = id

    def translate_val_to_sim(self):
        self.x += Arena_C.OFFSET_X
        self.y += Arena_C.OFFSET_Y

    
    def __str__(self):
        return f"({self.x}, {self.y}, {self.face}, {self.img_id})\n"

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.face}, {self.img_id})\n"
from algorithm.planner.utils.helpers import convert_val_to_sim

class Obstacle:

    # face is an Angle value
    def __init__(self, x, y, face, id=0):
        self.x = x
        self.y = y
        self.face = face
        self.img_id = id

    def translate_val_to_sim(self):
        self.x = convert_val_to_sim(self.x)
        self.y = convert_val_to_sim(self.y)

    
    def __str__(self):
        return f"({self.x}, {self.y}, {self.face}, {self.img_id})\n"

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.face}, {self.img_id})\n"
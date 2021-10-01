class Path:
    def __init__(self, x, y, yaw, direction, cost):
        self.x = x
        self.y = y
        self.yaw = yaw
        self.direction = direction
        self.cost = cost
        self.steer = []

    def __repr__(self):
        s = "path "
        for i in range(len(self.x)):
            s += str((self.x[i], self.y[i], self.yaw[i], self.direction[i], self.steer[i]))
            s += "\n"

        return s
from config import FIELD_WIDTH, FIELD_HEIGHT
class WorldState:
    def __init__(self):
        self.self_pose = (0.0, 0.0, 0.0)  # x, y, theta
        self.ball_position = None          # x, y
        self.teammates = []               # [(x, y, theta), ...]
        self.opponents = []               # [(x, y, theta), ...]
        self.has_ball = False
        self.goal_position = (FIELD_WIDTH, FIELD_HEIGHT / 2)
        self.time = 0

from pygame import Vector2
import random

MAX_RADIUS = 30

class Poid:
    def __init__(self):
        self._pos = Vector2(random.randint(0, 600), random.randint(0, 600))
        self.radius = random.randint(5, MAX_RADIUS)

    def get_pos(self):
        return Vector2(self._pos)

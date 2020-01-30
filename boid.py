from pygame import Vector2
import random

MAX_VEL = 2
MAX_MASS = 5

class Boid:
    def __init__(self):
        self._pos = Vector2(random.randint(0, 600), random.randint(0, 600))
        self._vel = Vector2(random.uniform(0.1, 1) * MAX_VEL * random.choice([-1, 1]),
                            random.uniform(0.1, 1) * MAX_VEL * random.choice([-1, 1]))
    def add_force(self, v):
        self._vel.update(self._vel.x + v.x, self._vel.y + v.y)

    def get_vel(self):
        return Vector2(self._vel)

    def get_pos(self):
        return Vector2(self._pos)

    def get_col(self):
        return 50 + int(205 * self._vel.magnitude() / MAX_VEL), 96, 178

    def move(self):
        if self._vel.magnitude() > MAX_VEL:
            self._vel.scale_to_length(MAX_VEL)

        self._pos.update(self._pos.x + self._vel.x, self._pos.y + self._vel.y)
        x = self._pos[0]
        y = self._pos[1]
        if x < 0:
            self._pos.update(600, y)
        if x > 600:
            self._pos.update(0, y)
        if y < 0:
            self._pos.update(x, 600)
        if y > 600:
            self._pos.update(x, 0)
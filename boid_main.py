import pygame
from pygame import Vector2
import sys
import math
from t_opers import add, subtract
from boid import Boid
from poid import Poid
pygame.init()
screen_width = 600
screen_height = 600

screen = pygame.display.set_mode([screen_width, screen_height])
clock = pygame.time.Clock()

boids = [Boid() for _ in range(50)]
poids = [Poid() for _ in range(0)]

RADIUS = 50
MAX_NUDGE = 0.25

#FIX AVERAGES VS SUMMATION PROBLEM. I.E. if i have more neighbors my alignment vector will have a larger magnitude

def draw_boid(b):
    nosehead = [b.get_pos().x, b.get_pos().y]
    v = b.get_vel()
    v.scale_to_length(7)
    p1 = add(nosehead, v.rotate(135))
    p2 = add(nosehead, v.rotate(-135))
    pygame.draw.polygon(screen, b.get_col(), [add(nosehead, v), p1, p2])

def draw_poid(p):
    pos = p.get_pos()
    pygame.draw.circle(screen, (255, 200, 78), (int(pos.x), int(pos.y)), p.radius)

def apply_forces(b):
    fleeing = False
    for p in poids:
        if b.get_pos().distance_to(p.get_pos()) <= RADIUS + p.radius:
            flee(b, p)
            fleeing = True
    if not fleeing:
        for other in boids:
            if other is not b:
                if b.get_pos().distance_to(other.get_pos()) <= RADIUS:
                    if can_see(b, other):
                        seperation(b, other)
                        alignment(b, other)
                        cohesion(b, other)



def seperation(b, other):
    mag = 0.1 * MAX_NUDGE * math.pow(2 * (RADIUS - (b.get_pos().distance_to(other.get_pos()))) / RADIUS, 2)
    nudge = Vector2(subtract(b.get_pos(), other.get_pos())).normalize()
    nudge.scale_to_length(mag)
    b.add_force(nudge)

def alignment(b, other):
    mag = MAX_NUDGE * (RADIUS - (b.get_pos().distance_to(other.get_pos()))) / RADIUS
    nudge = other.get_vel().normalize()
    nudge.scale_to_length(mag)
    b.add_force(nudge)

def cohesion(b, other):
    mag = 0.1 * MAX_NUDGE * math.pow((b.get_pos().distance_to(other.get_pos())) / RADIUS, 2)
    nudge = Vector2(subtract(other.get_pos(), b.get_pos())).normalize()
    nudge.scale_to_length(mag)
    b.add_force(nudge)

def can_see(b, other):
    x_diff = other.get_pos().x - b.get_pos().x
    y_diff = other.get_pos().y - b.get_pos().y
    facing = Vector2(x_diff, y_diff)
    facing.normalize()
    return math.fabs(b.get_vel().angle_to(facing)) < 130


def flee(b, p):
    mag = MAX_NUDGE * (p.radius + RADIUS - (b.get_pos().distance_to(p.get_pos()))) / (p.radius + RADIUS)
    nudge = Vector2(subtract(b.get_pos(), p.get_pos())).normalize()
    nudge.scale_to_length(mag)
    b.add_force(nudge)

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for p in poids:
        draw_poid(p)

    for b in boids:
        apply_forces(b)
        b.move()
        draw_boid(b)

    pygame.display.update()
    screen.fill((200, 200, 200))

pygame.quit()
sys.exit()

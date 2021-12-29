import pygame
from MovingObject import MovingObject
import math


class SpaceShip(MovingObject):
    def __init__(self, image, bullet_image):
        MovingObject.__init__(self, image)
        self.original_image = image
        self.bullet = bullet_image
        self.offset = 90
        self.last_shoot = pygame.time.get_ticks()
        self.acceleration = 0.3
        self.max_HP = 100
        self.HP = self.max_HP
        self.radius = 20
        self.max_speed = 3

    def move_up(self, offset):
        if abs(self.speedy) < self.max_speed:
            self.speedy += -self.acceleration * math.sin(math.radians(self.rot + offset) % 360)
        if abs(self.speedx) < self.max_speed:
            self.speedx += self.acceleration * math.cos(math.radians(self.rot + offset) % 360)

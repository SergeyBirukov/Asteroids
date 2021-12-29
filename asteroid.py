import pygame
import random
import math
from MovingObject import MovingObject

BLACK = (0, 0, 0)


class Asteroid(MovingObject):
    def __init__(self, image, size, position_x, position_y):
        MovingObject.__init__(self)
        self.type = size
        self.original_image = image
        self.original_image.set_colorkey(BLACK)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = position_x
        self.rect.y = position_y
        self.xPos = 0
        self.yPos = 0
        self.speedx = random.randint(-5+self.type, 5-self.type)
        self.speedy = random.randint(-5+self.type, 5-self.type)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.mask = pygame.mask.from_surface(self.image)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.original_image, self.rot)
            self.rect = self.image.get_rect(
                center=self.image.get_rect(center=(self.rect.centerx, self.rect.centery)).center)


    def update(self):
        self.rotate()
        self.xPos += self.speedx
        self.yPos += self.speedy
        self.rect.x, self.xPos = self.update_position(self.rect.x, self.xPos)
        self.rect.y, self.yPos = self.update_position(self.rect.y, self.yPos)
        self.mask = pygame.mask.from_surface(self.image)



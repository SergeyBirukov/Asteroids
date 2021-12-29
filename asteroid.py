import pygame
import random
from MovingObject import MovingObject

BLACK = (0, 0, 0)


class Asteroid(MovingObject):
    def __init__(self, image, size, position_x, position_y):
        MovingObject.__init__(self, image)
        self.type = size
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = position_x
        self.rect.y = position_y
        self.speedx = random.randint(-5+self.type, 5-self.type)
        self.speedy = random.randint(-5+self.type, 5-self.type)
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.current_image, self.rot)
            self.rect = self.image.get_rect(
                center=self.image.get_rect(center=(self.rect.centerx, self.rect.centery)).center)

    def update(self):
        self.rotate()
        super(Asteroid, self).update()



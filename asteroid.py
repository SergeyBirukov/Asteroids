import pygame
import random
import math

BLACK = (0, 0, 0)


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, image, position_x, position_y):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = image
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = position_x
        self.rect.y = position_y
        self.xPos = 0
        self.yPos = 0
        self.speedy = random.uniform(-5, 5)
        self.speedx = random.uniform(-5, 5)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
        self.mask = pygame.mask.from_surface(self.image)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.image_orig, self.rot)
            self.rect = self.image.get_rect(
                center=self.image.get_rect(center=(self.rect.centerx, self.rect.centery)).center)

    def set_position(self, x, y):
        self.rect.centerx, self.rect.centery = x, y

    def update(self):
        self.rotate()
        self.xPos += self.speedx
        self.yPos += self.speedy
        if self.xPos >= 1:
            part = math.floor(self.xPos)
            self.rect.x += part
            self.xPos -= part
        if self.xPos <= -1:
            part = math.ceil(self.xPos)
            self.rect.x += part
            self.xPos -= part
        if self.yPos >= 1:
            part = math.floor(self.yPos)
            self.rect.y += part
            self.yPos -= part
        if self.yPos <= -1:
            part = math.ceil(self.yPos)
            self.rect.y += part
            self.yPos -= part
        self.mask = pygame.mask.from_surface(self.image)

    def set_position(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y
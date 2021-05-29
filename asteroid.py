import pygame
import random

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
        self.speedy = random.randrange(-8, 8)
        self.speedx = random.randrange(-3, 3)
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

    def set_position(self, x, y):
        self.rect.centerx, self.rect.centery = x, y

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # if self.rect.top > HEIGHT + 10:
        #     self.rect.x = random.randrange(WIDTH - self.rect.width)
        #     self.rect.y = random.randrange(-100, -40)
        #
        # if self.rect.right < -20 or self.rect.left > WIDTH + 20 or self.rect.top > HEIGHT + 10:
        #     self.rect.x = random.randrange(WIDTH - self.rect.width)
        #     self.rect.y = random.randrange(-100, -40)
        #

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
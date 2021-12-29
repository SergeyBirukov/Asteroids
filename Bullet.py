import pygame
import math


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_image, rotation):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = bullet_image
        self.image_orig.set_colorkey((0, 0, 0))
        self.offset = 90
        self.image = pygame.transform.rotate(self.image_orig, rotation)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.speed_const = 10
        self.rot = rotation
        self.life_timer = pygame.time.get_ticks()
        self.life_time = 2000
        self.mask = pygame.mask.from_surface(self.image)

    def set_position(self, x, y):
        self.rect.centerx, self.rect.centery = x, y

    def update(self):
        if pygame.time.get_ticks() - self.life_timer > self.life_time:
            self.kill()
        self.rect.y += -self.speed_const * math.sin(math.radians(self.rot) % 360)
        self.rect.x += self.speed_const * math.cos(math.radians(self.rot) % 360)
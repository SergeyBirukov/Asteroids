import pygame
import random
from os import path

BLACK = (0, 0, 0)


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, img_dir, type=None ):
        pygame.sprite.Sprite.__init__(self)
        self.powerup_images = {"shield": pygame.image.load(path.join(img_dir, "shield.png")).convert(),
                               "gun": pygame.image.load(path.join(img_dir, "bolt.png")).convert(),
                               "live": pygame.image.load(path.join(img_dir, "Heart.png")).convert()}
        if type is None:
            self.type = random.choice(["shield", "gun", "live"])
        else:
            self.type = type
        self.image = self.powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = pos_x
        self.rect.centery = pos_y
        self.life_time = 7000
        self.time = pygame.time.get_ticks()
        self.speedy = 5

    def update(self):
        if pygame.time.get_ticks() - self.time > self.life_time:
            self.kill()

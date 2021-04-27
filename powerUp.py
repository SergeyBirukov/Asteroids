import pygame
import random
from os import path
from main import img_dir

BLACK = (0, 0, 0)


class Pow(pygame.sprite.Sprite):
    def __init__(self, center, pow_type):
        pygame.sprite.Sprite.__init__(self)
        self.type = pow_type
        self.powerup_images = {
            "shield": pygame.image.load(path.join(img_dir, "shield.png")).convert(),
            "gun": pygame.image.load(path.join(img_dir, "bolt.png")).convert()
        }
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self, HEIGHT):
        self.rect.y += self.speedy
        # kill if it moves thr top of the screen
        if self.rect.top > HEIGHT:
            self.kill()

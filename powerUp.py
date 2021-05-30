import pygame
import random
from os import path

BLACK = (0, 0, 0)


class Pow(pygame.sprite.Sprite):
    def __init__(self, center, img_dir):
        pygame.sprite.Sprite.__init__(self)
        self.powerup_images = {}
        self.powerup_images["shield"] = pygame.image.load(path.join(img_dir, "shield.png")).convert()
        self.powerup_images["gun"] = pygame.image.load(path.join(img_dir, "bolt.png")).convert()
        self.powerup_images["live"] = pygame.image.load(path.join(img_dir, "Heart.png")).convert()
        self.type = random.choice(["shield", "gun", "live"])
        self.image = self.powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        # kill if it moves thr top of the screen
        pass

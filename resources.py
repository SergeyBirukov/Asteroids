import pygame
from os import path

WIDTH = 800
HEIGHT = 800


class Resources:
    def __init__(self):
        self.img_dir = path.join(path.dirname(__file__), "img")
        self.sound_dir = path.join(path.dirname(__file__), "sound")
        self.leaderboard_filename = "leaderboard"
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.background = pygame.image.load(
            path.join(self.img_dir, "space_shooter_background.png")).convert()
        self.background_rect = self.background.get_rect()
        self.player_img = pygame.image.load(
            path.join(self.img_dir, "playerShip1_red.png")).convert()
        self.player_mini_img = pygame.transform.scale(self.player_img, (25, 19))
        self.player_mini_img.set_colorkey((0, 0, 0))
        self.player_with_shield_image = self.lazer = pygame.image.load(path.join(self.img_dir, "ship_with_shield.png")).convert()
        self.lazer = pygame.image.load(path.join(self.img_dir, "laserBlue03.png")).convert()
        self.asteroid_big = ["meteorBrown_big1.png", "meteorBrown_big2.png", "meteorBrown_big4.png", "meteorBrown_big3.png"]
        self.asteroid_small = ["meteorBrown_small1.png", "meteorBrown_small2.png"]
        self.asteroid_medium = ["meteorBrown_med1.png", "meteorBrown_med3.png"]
        self.asteroid_big_images = []
        self.asteroid_medium_images = []
        self.asteroid_small_images = []
        for img in self.asteroid_big:
            self.asteroid_big_images.append(
                pygame.image.load(path.join(self.img_dir, img)).convert())
        for img in self.asteroid_medium:
            self.asteroid_medium_images.append(
                pygame.image.load(path.join(self.img_dir, img)).convert())
        for img in self.asteroid_small:
            self.asteroid_small_images.append(
                pygame.image.load(path.join(self.img_dir, img)).convert())
        self.font_name = pygame.font.match_font('arial')

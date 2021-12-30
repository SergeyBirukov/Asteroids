import pygame
from os import path

WIDTH = 1000
HEIGHT = 800


def resource_load(dir, name):
    return pygame.image.load(path.join(dir, name)).convert()


def sound_load(dir, name):
    return pygame.mixer.Sound(path.join(dir, name))


class Resources:
    def __init__(self):
        self.img_dir = path.join(path.dirname(__file__), "img")
        self.sound_dir = path.join(path.dirname(__file__), "sound")
        self.shoot_sound = sound_load(self.sound_dir, "Laser_Shoot.wav")
        self.shoot_sound.set_volume(0.4)
        self.explosion_sound = sound_load(self.sound_dir, "Explosion1.wav")
        self.explosion_sound2 = sound_load(self.sound_dir, "Explosion2.wav")
        self.explosion_sound.set_volume(0.8)
        self.bonus_sound = sound_load(self.sound_dir, "bonus.mp3")
        self.teleport_sound = sound_load(self.sound_dir, "teleport.wav")
        self.teleport_sound.set_volume(2)
        self.leaderboard_filename = "leaderboard"
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.background = resource_load(self.img_dir, "space_shooter_background.png")
        self.background_rect = self.background.get_rect()
        self.player_img = resource_load(self.img_dir, "playerShip1_red.png")
        self.player_mini_img = pygame.transform.scale(self.player_img, (25, 19))
        self.player_mini_img.set_colorkey((0, 0, 0))
        self.player_with_shield_image = self.laser = resource_load(self.img_dir, "ship_with_shield.png")
        self.laser = resource_load(self.img_dir, "laserBlue03.png")
        self.UFO_laser = resource_load(self.img_dir, "laserRed03.png")
        self.ufo_image = resource_load(self.img_dir, "enemyBlack2.png")
        self.asteroid_big = ["meteorBrown_big1.png", "meteorBrown_big2.png", "meteorBrown_big4.png",
                             "meteorBrown_big3.png"]
        self.asteroid_small = ["meteorBrown_small1.png", "meteorBrown_small2.png"]
        self.asteroid_medium = ["meteorBrown_med1.png", "meteorBrown_med3.png"]
        self.asteroid_big_images = []
        self.asteroid_medium_images = []
        self.asteroid_small_images = []
        for img in self.asteroid_big:
            self.asteroid_big_images.append(resource_load(self.img_dir, img))
        for img in self.asteroid_medium:
            self.asteroid_medium_images.append(resource_load(self.img_dir, img))
        for img in self.asteroid_small:
            self.asteroid_small_images.append(resource_load(self.img_dir, img))
        self.font_name = pygame.font.match_font('arial')

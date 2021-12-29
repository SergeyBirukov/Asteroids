# confirmed
import pygame
import math
import random
from SpaceShip import SpaceShip
from Bullet import Bullet

BLACK = (0, 0, 0)


class UFO(SpaceShip):
    def __init__(self, image, bullet_image, width, height):
        SpaceShip.__init__(self, image, bullet_image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.max_HP = 3
        self.HP = self.max_HP
        self.type = "UFO"
        self._choose_spawn_point(width, height)
        self.rect.centerx, self.rect.centery = self.start_position['x'], self.start_position['y']
        self.shoot_delay = 2000

    def _choose_spawn_point(self, width, height):
        start_from_side = bool(random.getrandbits(1))
        start_from_end = bool(random.getrandbits(1))
        random_start_pos = random.uniform(0, height if start_from_side else width)
        if start_from_side:
            self.start_position = {'x': start_from_end * width, 'y': random_start_pos}
            if start_from_end:
                if random_start_pos > height / 2:
                    self.rot = random.uniform(180, 270)
                else:
                    self.rot = random.uniform(90, 180)
            else:
                if random_start_pos > height / 2:
                    self.rot = random.uniform(270, 360)
                else:
                    self.rot = random.uniform(0, 90)
        else:
            self.start_position = {'x': random_start_pos, 'y': start_from_end * height}
            if start_from_end:
                if random_start_pos > width / 2:
                    self.rot = random.uniform(90, 180)
                else:
                    self.rot = random.uniform(0, 90)
            else:
                if random_start_pos > width / 2:
                    self.rot = random.uniform(180, 270)
                else:
                    self.rot = random.uniform(270, 360)

    def shoot(self, moment, player_pos):
        if moment - self.last_shoot > self.shoot_delay:
            dx = player_pos[0] - self.rect.centerx
            dy = player_pos[1] - self.rect.centery
            rads = math.atan2(-dy, dx)
            rads %= 2 * math.pi
            degs = math.degrees(rads)
            self.last_shoot = moment
            return UFOBullet(self.rect.centerx, self.rect.centery, self.bullet, degs)

    def update(self):
        if self.HP <= 0:
            self.kill()
        self.move_up(0)
        super(UFO, self).update()


class UFOBullet(Bullet):
    def __init__(self, x, y, bullet_image, rotation):
        Bullet.__init__(self, x, y, bullet_image, rotation)
        self.image = pygame.transform.rotate(self.image_orig, rotation + self.offset)
        self.type = "UFO_bullet"
        self.speed_const = 12
        self.radius = 20

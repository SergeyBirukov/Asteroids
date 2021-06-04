#confirmed
import pygame
import math
import random

BLACK = (0, 0, 0)


class UFO(pygame.sprite.Sprite):
    def __init__(self, ufo_image, bullet_image, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.ufo_image = ufo_image
        self.current_image = ufo_image
        self.current_image.set_colorkey(BLACK)
        self.image = self.current_image.copy()
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.HP = 3
        self.type = "UFO"
        self.radius = 20
        self.bullet = bullet_image
        self._choose_spawn_point(width, height)
        self.rect.centerx, self.rect.centery = self.start_position['x'], self.start_position['y']
        self.speed = 3
        self.speedx = 0
        self.speedy = 0
        self.xPos = 0
        self.yPos = 0
        self.acceleration = 0.3
        self.shoot_delay = 3000
        self.last_shoot = pygame.time.get_ticks()
        self.offset = 90
        self.mask = pygame.mask.from_surface(self.image)
        self.rotate()

    def _choose_spawn_point(self, width, height):
        start_from_side = bool(random.getrandbits(1))
        start_from_end = bool(random.getrandbits(1))
        if start_from_side:
            random_start_pos = random.uniform(0, height)
        else:
            random_start_pos = random.uniform(0, width)
        if start_from_side:
            self.start_position = {'x': start_from_end * width, 'y': random_start_pos}
            if start_from_end:
                if random_start_pos > height/2:
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

    def move_up(self):
        if abs(self.speedy) < self.speed:
            self.speedy += -self.acceleration * math.sin(math.radians(self.rot) % 360)
        if abs(self.speedx) < self.speed:
            self.speedx += self.acceleration * math.cos(math.radians(self.rot) % 360)

    def rotate(self):
        pass

    def set_position(self, x, y):
        self.rect.centerx, self.rect.centery = x, y

    def shoot(self, moment, player_pos):
        if moment - self.last_shoot > self.shoot_delay:
            print(player_pos, "and", self.rect.centerx, self.rect.centery)
            dx = player_pos[0] - self.rect.centerx
            dy = player_pos[1] - self.rect.centery
            rads = math.atan2(-dy, dx)
            rads %= 2 * math.pi
            degs = math.degrees(rads)
            print(degs)
            self.last_shoot = moment
            return Bullet(self.rect.centerx, self.rect.centery, self.bullet, degs)

    def update(self):
        if self.HP <= 0:
            self.kill()
        self.move_up()
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


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_image, rotation):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = bullet_image
        self.image_orig.set_colorkey((0, 0, 0))
        self.rot = rotation
        self.offset = 90
        self.image = pygame.transform.rotate(self.image_orig, rotation + self.offset)
        self.rect = self.image.get_rect()
        self.type = "UFO_bullet"
        self.rect.centery = y
        self.rect.centerx = x
        self.radius = 20
        self.speed_const = 7
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

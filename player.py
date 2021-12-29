import pygame
import math
import random
from SpaceShip import SpaceShip
from Bullet import Bullet

BLACK = (0, 0, 0)


class Player(SpaceShip):
    def __init__(self, image, player_with_shield_image, bullet_image, position_x, position_y):
        SpaceShip.__init__(self, image, bullet_image)
        self.player_with_shield_image = player_with_shield_image
        self.start_position = {'x': position_x, 'y': position_y}
        self.rect.centerx, self.rect.centery = self.start_position['x'], self.start_position['y']
        self.type = "Player"
        self.max_speed = 5
        self.rot_speed = 3
        self.max_lives = 3
        self.lives = 3
        self.gun_level = 0
        self.is_shield_on = False
        self.can_shoot = True
        self.hidden = False

        self.shield_timer = pygame.time.get_ticks()
        self.last_update = pygame.time.get_ticks()
        self.hide_timer = pygame.time.get_ticks()
        self.gun_timer = pygame.time.get_ticks()
        self.hyperspace_timer = pygame.time.get_ticks()
        self.shoot_levels = [
            lambda: PlayerBullet(self.rect.centerx, self.rect.centery, self.bullet, self.rot),

            lambda: (PlayerBullet(self.rect.centerx, self.rect.centery, self.bullet, self.rot),
                     PlayerBullet(self.rect.centerx, self.rect.centery, self.bullet, self.rot + 10),
                     PlayerBullet(self.rect.centerx, self.rect.centery, self.bullet, self.rot - 10)),

            lambda: (PlayerBullet(self.rect.centerx, self.rect.centery, self.bullet, self.rot),
                     PlayerBullet(self.rect.centerx, self.rect.centery, self.bullet, self.rot + 10),
                     PlayerBullet(self.rect.centerx, self.rect.centery, self.bullet, self.rot - 10),
                     PlayerBullet(self.rect.centerx, self.rect.centery, self.bullet, self.rot + 20),
                     PlayerBullet(self.rect.centerx, self.rect.centery, self.bullet, self.rot - 20))
        ]

        self.gun_power_up_time = 10000
        self.shoot_delay = 250
        self.hyperspace_delay = 250
        self.shield_time = 5000
        self.hide_time = 100

    def gun_level_up(self):
        self.gun_timer = pygame.time.get_ticks()
        self.gun_level += 1
        self.shoot_delay = 400

    def shoot(self):
        return self.shoot_levels[self.gun_level]()

    def rotate(self, is_left: bool):
        self.rot = (self.rot + self.rot_speed) % 360 if is_left else (self.rot - self.rot_speed) % 360
        self.image = pygame.transform.rotate(self.current_image, self.rot)
        self.rect = self.image.get_rect(center=self.image.get_rect(center=(self.rect.centerx, self.rect.centery)).center)

    def idle(self):
        self.speedx += -0.05 if self.speedx > 0 else 0.05
        self.speedy += -0.05 if self.speedy > 0 else 0.05

    def hide(self):
        self.hidden = True
        self.can_shoot = False
        self.hide_timer = pygame.time.get_ticks()
        self.rect.centerx = self.start_position['x'] - 1000
        self.rect.bottom = self.start_position['y'] - 1000

    def shield_on(self):
        self.is_shield_on = True
        self.shield_timer = pygame.time.get_ticks()
        self.current_image = self.player_with_shield_image
        self.current_image.set_colorkey(BLACK)

    def shield_off(self):
        self.is_shield_on = False
        self.current_image = self.original_image
        self.current_image.set_colorkey(BLACK)

    def respawn(self):
        self.hide()
        self.lives -= 1
        self.gun_level = 0
        self.HP = 100

    def update(self):
        super(Player, self).update()
        if pygame.time.get_ticks() - self.hide_timer > self.hide_time and self.hidden:
            self.hidden = False
            self.can_shoot = True
            self.rect.centerx, self.rect.centery = self.start_position['x'], self.start_position['y']
        if pygame.time.get_ticks() - self.shield_timer > self.shield_time and self.is_shield_on:
            self.shield_off()
        if pygame.time.get_ticks() - self.gun_timer > self.gun_power_up_time and self.gun_level:
            self.gun_level -= 1

    def hyperspace(self):
        if pygame.time.get_ticks() - self.hyperspace_timer > self.hyperspace_delay:
            self.set_position(random.randrange(0, 800), random.randrange(0, 800))
            self.hyperspace_timer = pygame.time.get_ticks()


class PlayerBullet(Bullet):
    def __init__(self, x, y, bullet_image, rotation):
        Bullet.__init__(self, x, y, bullet_image, rotation)
        self.type = "Bullet"

    def update(self):
        if pygame.time.get_ticks() - self.life_timer > self.life_time:
            self.kill()
        self.rect.y += -self.speed_const * math.sin(math.radians(self.rot + self.offset) % 360)
        self.rect.x += self.speed_const * math.cos(math.radians(self.rot + self.offset) % 360)

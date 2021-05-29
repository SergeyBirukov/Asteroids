import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, player_image, bullet_image, position_x, position_y):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = player_image
        self.image_orig.set_colorkey((0, 0, 0))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.radius = 20
        self.bullet = bullet_image
        self.start_position = {'x': position_x, 'y': position_y}
        self.rect.centerx, self.rect.centery = self.start_position['x'], self.start_position['y']
        self.speedx = 0
        self.speedy = 0
        self.speed_constant = 5
        self.shield = 100
        self.shoot_delay = 250
        self.last_shoot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.can_shoot = True
        self.rot = 0
        self.offest = 90
        self.rot_speed = 2
        self.last_hyperspace = pygame.time.get_ticks()
        self.hyperspace_delay = 250
        self.last_update = pygame.time.get_ticks()
        self.mask = pygame.mask.from_surface(self.image)

    def shoot(self):
        return Bullet(self.rect.centerx, self.rect.centery, self.bullet, self.rot)

    def move_up(self):
        self.speedy = -self.speed_constant * math.sin(math.radians(self.rot + self.offest) % 360)
        self.speedx = self.speed_constant * math.cos(math.radians(self.rot + self.offest) % 360)


    def rotate_left(self):
        self.rot = (self.rot + self.rot_speed) % 360
        self.image = pygame.transform.rotate(self.image_orig, self.rot)
        self.rect = self.image.get_rect(center=self.image.get_rect(center=(self.rect.centerx, self.rect.centery)).center)

    def rotate_right(self):
        self.rot = (self.rot - self.rot_speed) % 360
        self.image = pygame.transform.rotate(self.image_orig, self.rot)
        self.rect = self.image.get_rect(center=self.image.get_rect(center=(self.rect.centerx, self.rect.centery)).center)


    def idle(self):
        if self.speedx > 0:
            self.speedx -= 0.1
        if self.speedx < 0:
            self.speedx += 0.1
        if self.speedy > 0:
            self.speedy -= 0.1
        if self.speedy < 0:
            self.speedy += 0.1

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.centerx = self.start_position['x']
        self.rect.bottom = self.start_position['y'] + 200

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def set_position(self, x, y):
        self.rect.centerx, self.rect.centery = x, y

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_image, rotation):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = bullet_image
        self.image_orig.set_colorkey((0, 0, 0))
        self.image = pygame.transform.rotate(self.image_orig, rotation)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.speed_const = 10
        self.rot = rotation
        self.offset = 90
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += -self.speed_const * math.sin(math.radians(self.rot + self.offset) % 360)
        self.rect.x += self.speed_const * math.cos(math.radians(self.rot + self.offset) % 360)
        # kill if it moves thr top of the screen
        if self.rect.bottom < 0:
            self.kill()

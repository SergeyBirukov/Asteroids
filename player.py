import pygame
import math

BLACK = (0, 0, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self, player_image, player_with_shield, bullet_image, position_x, position_y):
        pygame.sprite.Sprite.__init__(self)
        self.player_with_shield_image = player_with_shield
        self.player_image = player_image
        self.current_image = player_image
        self.current_image.set_colorkey(BLACK)
        self.image = self.current_image.copy()
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.type = "Player"
        self.radius = 20
        self.bullet = bullet_image
        self.start_position = {'x': position_x, 'y': position_y}
        self.rect.centerx, self.rect.centery = self.start_position['x'], self.start_position['y']
        self.max_speed = 5
        self.speedx = 0
        self.speedy = 0
        self.xPos = 0
        self.yPos = 0
        self.acceleration = 0.3
        self.HP = 100
        self.shoot_delay = 250
        self.last_shoot = pygame.time.get_ticks()
        self.lives = 3
        self.gun_level = 0
        self.is_shield_on = False
        self.shield_timer = pygame.time.get_ticks()
        self.shield_time = 5000
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.hide_time = 1000
        self.can_shoot = True
        self.rot = 0
        self.offset = 90
        self.rot_speed = 3
        self.last_hyperspace = pygame.time.get_ticks()
        self.hyperspace_delay = 250
        self.last_update = pygame.time.get_ticks()
        self.mask = pygame.mask.from_surface(self.image)

    def gun_level_up(self):
        self.gun_level += 1
        self.shoot_delay = 400

    def shoot(self):
        if self.gun_level == 0:
            return Bullet(self.rect.centerx, self.rect.centery, self.bullet, self.rot)
        if self.gun_level == 1:
            return (Bullet(self.rect.centerx, self.rect.centery, self.bullet, self.rot),
                    Bullet(self.rect.centerx, self.rect.centery, self.bullet, self.rot + 10),
                    Bullet(self.rect.centerx, self.rect.centery, self.bullet, self.rot-10))
        if self.gun_level == 2:
            return (Bullet(self.rect.centerx, self.rect.centery, self.bullet, self.rot),
                    Bullet(self.rect.centerx, self.rect.centery, self.bullet, self.rot + 10),
                    Bullet(self.rect.centerx, self.rect.centery, self.bullet, self.rot-10),
                    Bullet(self.rect.centerx, self.rect.centery, self.bullet, self.rot + 20),
                    Bullet(self.rect.centerx, self.rect.centery, self.bullet, self.rot - 20))

    def move_up(self):
        if abs(self.speedy) < self.max_speed:
            self.speedy += -self.acceleration * math.sin(math.radians(self.rot + self.offset) % 360)
        if abs(self.speedx) < self.max_speed:
            self.speedx += self.acceleration * math.cos(math.radians(self.rot + self.offset) % 360)

    def rotate_left(self):
        self.rot = (self.rot + self.rot_speed) % 360
        self.image = pygame.transform.rotate(self.current_image, self.rot)
        self.rect = self.image.get_rect(center=self.image.get_rect(center=(self.rect.centerx, self.rect.centery)).center)

    def rotate_right(self):
        self.rot = (self.rot - self.rot_speed) % 360
        self.image = pygame.transform.rotate(self.current_image, self.rot)
        self.rect = self.image.get_rect(center=self.image.get_rect(center=(self.rect.centerx, self.rect.centery)).center)

    def idle(self):
        if self.speedx > 0:
            self.speedx -= 0.07
        if self.speedx < 0:
            self.speedx += 0.07
        if self.speedy > 0:
            self.speedy -= 0.07
        if self.speedy < 0:
            self.speedy += 0.07

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.can_shoot = False
        self.hide_timer = pygame.time.get_ticks()
        self.rect.centerx = self.start_position['x']-1000
        self.rect.bottom = self.start_position['y']-1000

    def shield_on(self):
        self.is_shield_on = True
        self.shield_timer = pygame.time.get_ticks()
        self.current_image = self.player_with_shield_image
        self.current_image.set_colorkey(BLACK)

    def shield_off(self):
        self.is_shield_on = False
        self.current_image = self.player_image
        self.current_image.set_colorkey(BLACK)

    def update(self):

        self.xPos += self.speedx
        self.yPos += self.speedy
        if pygame.time.get_ticks() - self.hide_timer > self.hide_time and self.hidden == True:
            self.hidden = False
            self.can_shoot = True
            self.rect.centerx, self.rect.centery = self.start_position['x'], self.start_position['y']
        if pygame.time.get_ticks() - self.shield_timer > self.shield_time:
            self.shield_off()
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

    def set_position(self, x, y):
        self.rect.centerx, self.rect.centery = x, y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_image, rotation):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = bullet_image
        self.image_orig.set_colorkey((0, 0, 0))
        self.image = pygame.transform.rotate(self.image_orig, rotation)
        self.rect = self.image.get_rect()
        self.type = "Bullet"
        self.rect.centery = y
        self.rect.centerx = x
        self.speed_const = 10
        self.rot = rotation
        self.offset = 90
        self.life_timer = pygame.time.get_ticks()
        self.life_time = 2000
        self.mask = pygame.mask.from_surface(self.image)

    def set_position(self, x, y):
        self.rect.centerx, self.rect.centery = x, y

    def update(self):
        if pygame.time.get_ticks() - self.life_timer > self.life_time:
            self.kill()
        self.rect.y += -self.speed_const * math.sin(math.radians(self.rot + self.offset) % 360)
        self.rect.x += self.speed_const * math.cos(math.radians(self.rot + self.offset) % 360)


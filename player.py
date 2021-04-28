import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, player_image, bullet_image, position_x, position_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_image
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.radius = 50
        self.bullet = bullet_image
        self.start_position = {'x': position_x, 'y': position_y}
        self.rect.centerx, self.rect.centery = self.start_position.values()
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shoot = pygame.time.get_ticks()
        self.lives = 3
        self.can_shoot = True

    def shoot(self):
        return Bullet(self.rect.centerx, self.rect.centery, self.bullet)

    def move_up(self):
        self.speedy = -5

    def move_down(self):
        self.speedy = 5

    def move_left(self):
        self.speedx = -5

    def move_right(self):
        self.speedx = 5

    def idle(self):
        if self.speedx > 0:
            self.speedx -= 0.1
        if self.speedx < 0:
            self.speedx += 0.1
        if self.speedy > 0:
            self.speedy -= 0.1
        if self.speedy < 0:
            self.speedy += 0.1

    def respawn(self):
        self.rect.centerx = self.start_position['x']
        self.rect.bottom = self.start_position['y']

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def set_position(self, x, y):
        self.rect.centerx, self.rect.centery = x, y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_image):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves thr top of the screen
        if self.rect.bottom < 0:
            self.kill()

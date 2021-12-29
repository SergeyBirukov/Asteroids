import math
import pygame

BLACK = (0, 0, 0)


class MovingObject(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.current_image = image
        self.current_image.set_colorkey(BLACK)
        self.image = self.current_image.copy()
        self.rect = self.image.get_rect()
        self.xPos = 0
        self.yPos = 0
        self.speedx = 0
        self.speedy = 0
        self.rot = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.xPos += self.speedx
        self.yPos += self.speedy
        self.rect.x, self.xPos = self.update_position(self.rect.x, self.xPos)
        self.rect.y, self.yPos = self.update_position(self.rect.y, self.yPos)
        self.mask = pygame.mask.from_surface(self.image)

    def update_position(self, rect_pos, pos):
        part = math.floor(pos) if pos >= 1 else math.ceil(pos)
        rect_pos += part
        pos -= part
        return rect_pos, pos

    def set_position(self, x, y):
        self.rect.centerx, self.rect.centery = x, y

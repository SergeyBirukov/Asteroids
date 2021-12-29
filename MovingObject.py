import math
import pygame


class MovingObject(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def update_position(self, rect_pos, pos):
        part = math.floor(pos) if pos >= 1 else math.ceil(pos)
        rect_pos += part
        pos -= part
        return rect_pos, pos

    def set_position(self, x, y):
        self.rect.centerx, self.rect.centery = x, y

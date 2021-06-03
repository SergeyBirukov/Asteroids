import pygame
from math import floor

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Interface:
    def draw_text_centered(screen, text, size, x, y, font, color):
        font = pygame.font.Font(font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

    def draw_input(screen, text, size, x, y, font, color):
        font = pygame.font.Font(font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        screen.blit(text_surface, text_rect)

    def draw_lives(screen, x, y, lives, img):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x + 30 * i
            img_rect.y = y
            screen.blit(img, img_rect)

    def draw_shield_bar(screen, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGHT = 100
        BAR_HEIGHT = 10
        fill = (pct / 100) * BAR_LENGHT
        outline_rect = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(screen, GREEN, fill_rect)
        pygame.draw.rect(screen, WHITE, outline_rect, 2)

    class Button:
        def __init__(self, screen, x, y, size_x, size_y, text, font, button_color=(255, 255, 255), text_color=(0, 0, 0)):
            self.text = text
            self.pos_x, self.pos_y = x, y
            self.size_x, self.size_y = size_x, size_y
            self.button_color = button_color
            self.text_color = text_color
            self.screen = screen
            self.font = font
            self.rect = pygame.Rect(self.pos_x, self.pos_y, self.size_x, self.size_y)

        def draw(self):
            pygame.draw.rect(self.screen, self.button_color, self.rect)
            Interface.draw_text_centered(self.screen, self.text, floor(self.size_y * 0.6), (2 * self.pos_x + self.size_x) / 2,
                                         (1.92 * self.pos_y + self.size_y) / 2, self.font, self.text_color)




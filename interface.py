import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Interface:
    def draw_text(screen, text, size, x, y, font):
        font = pygame.font.Font(font, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
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
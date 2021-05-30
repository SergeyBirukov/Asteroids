import pygame
from resources import Resources
from os import path
from interface import Interface
import sys

img_dir = path.join(path.dirname(__file__), "img")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class MainMenu:
    def __init__(self, game):
        self.clock = pygame.time.Clock()
        self.resources = Resources(img_dir)
        self.screen = self.resources.screen
        self.game = game

    def draw_text(screen, text, size, x, y, font):
        font = pygame.font.Font(font, size)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

    def menu(self):
        pygame.init()
        click = False
        while True:
            mx, my = pygame.mouse.get_pos()
            self.screen.fill((0, 0, 0))
            Interface.draw_text(screen=self.screen, text="Asteroids", size=52, x=self.screen.get_width()/2, y=self.screen.get_height()/2-200,
                           font=self.resources.font_name, color=WHITE)

            button1 = pygame.Rect(self.screen.get_width()/2-100, self.screen.get_height()/2, 200, 50)
            button2 = pygame.Rect(self.screen.get_width()/2-100, self.screen.get_height()/2+100, 200, 50)
            pygame.draw.rect(self.screen, (255, 255, 255), button1)
            pygame.draw.rect(self.screen, (255, 255, 255), button2)
            Interface.draw_text(screen=self.screen, text="Play", size=28, x=self.screen.get_width()/2, y=self.screen.get_height()/2+10,
                           font=self.resources.font_name, color=BLACK)
            Interface.draw_text(screen=self.screen, text="Exit", size=28, x=self.screen.get_width() / 2, y=self.screen.get_height() / 2 + 110,
                                font=self.resources.font_name, color=BLACK)
            if button1.collidepoint(mx, my):
                if click:
                    self.game.run()

            if button2.collidepoint(mx, my):
                if click:
                    pygame.quit()
                    sys.exit()

            click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True

            pygame.display.update()
            self.clock.tick(60)
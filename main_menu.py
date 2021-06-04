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
    def __init__(self, game, leaderboard):
        self.clock = pygame.time.Clock()
        self.resources = Resources()
        self.screen = self.resources.screen
        self.game = game
        self.clock = pygame.time.Clock()
        self.leaderboard = leaderboard

    def draw_text(screen, text, size, x, y, font):
        font = pygame.font.Font(font, size)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

    def menu(self):
        pygame.mixer.music.load(self.resources.sound_dir + "music.ogg")
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()
        click = False
        while True:
            mx, my = pygame.mouse.get_pos()
            self.screen.fill((0, 0, 0))
            Interface.draw_text_centered(screen=self.screen, text="Asteroids", size=52, x=self.screen.get_width() / 2, y=self.screen.get_height() / 2 - 200,
                                         font=self.resources.font_name, color=WHITE)
            button1 = Interface.Button(self.screen, self.screen.get_width()/2-100, self.screen.get_height()/2,
                                       200, 50, "Play", self.resources.font_name)
            button2 = Interface.Button(self.screen, self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 + 100,
                                       200, 50, "Leaderboard", self.resources.font_name)
            button3 = Interface.Button(self.screen, self.screen.get_width()/2-100, self.screen.get_height()/2+200,
                                       200, 50, "Exit", self.resources.font_name)

            button1.draw()
            button2.draw()
            button3.draw()
            if button1.rect.collidepoint(mx, my):
                if click:
                    game = self.game(self.resources)
                    game.run()
            if button2.rect.collidepoint(mx, my):
                if click:
                    self.leaderboard.run()

            if button3.rect.collidepoint(mx, my):
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

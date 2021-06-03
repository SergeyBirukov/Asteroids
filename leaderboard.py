import shelve
from resources import Resources
import pygame
from interface import Interface
import sys


class LeaderBoard:
    def __init__(self):
        self.resources = Resources()
        self.width = self.resources.WIDTH
        self.height = self.resources.HEIGHT
        self.filename = self.resources.leaderboard_filename
        self.running = False
        self.clock = pygame.time.Clock()
        self.mx, self.my = pygame.mouse.get_pos()

    def save_score(self, name, score):
        with shelve.open(self.filename) as lb:
            if not name in lb.keys():
                lb[name] = (score,)
            else:
                lb[name] += (score,)

    def get_scores(self, name):
        with shelve.open(self.filename) as lb:
            return lb[name]

    def _process_events(self):
        self.click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click = True

    def run(self):
        self.running = True
        lb = self.get_leaderboard()

        self.resources.screen.fill((0, 0, 0))
        while self.running:
            self.mx, self.my = pygame.mouse.get_pos()
            button1 = Interface.Button(self.resources.screen, self.width / 2 - 100,
                                       self.height-200,
                                       200, 50, "Main menu", self.resources.font_name)
            button1.draw()
            self._process_events()
            if button1.rect.collidepoint(self.mx, self.my):
                if self.click:
                    self.running = False
            Interface.draw_text_centered(self.resources.screen, "Name", 32, self.width * 0.2, self.height * 0.1,
                                         self.resources.font_name, (255, 255, 255))
            Interface.draw_text_centered(self.resources.screen, "Score", 32, self.width * 0.6, self.height * 0.1,
                                         self.resources.font_name, (255, 255, 255))
            for i in range(5):
                if lb == [] or i > len(lb)-1:
                    self.draw_draw_line(i, '', '')
                    continue
                self.draw_draw_line(i, lb[i][0], lb[i][1])
            pygame.display.update()
            self.clock.tick(60)

    def draw_draw_line(self, number, name, score):
        line = pygame.Rect(self.width * 0.15, self.height*0.15 + self.height*0.1*number,
                           self.width * 0.7, 50)
        pygame.draw.rect(self.resources.screen, (255, 255, 255), line)
        Interface.draw_input(self.resources.screen, name, 32,  self.width * 0.16, self.height*0.15 + self.height*0.1*number, self.resources.font_name, (0, 0, 0))
        Interface.draw_input(self.resources.screen, str(score), 32,  self.width * 0.6, self.height*0.15 + self.height*0.1*number, self.resources.font_name, (0, 0, 0))

    def get_leaderboard(self):
        leaderboard = []
        with shelve.open(self.filename) as lb:
            for name in lb.keys():
                for score in lb[name]:
                    leaderboard.append((name, score))
        leaderboard.sort(key=lambda x: (-x[1], x[0]))
        return leaderboard

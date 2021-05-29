from os import path

import random
import pygame
import asteroid
import player
import main

img_dir = path.join(path.dirname(__file__), "img")

class LevelSystem:
    def __init__(self, game, space_ship, width, height):
        self.game = game
        self.player = space_ship
        self.width = width
        self.height = height
        self.levels = [self.prepare_level_one, self.prepare_level_two]
        self.current_level = -1

    def set_next_level(self):
        if self.current_level + 1 == len(self.levels):
            self.current_level = 0
        else:
            self.current_level += 1
        self.levels[self.current_level]()

    def prepare_level_one(self):
        self.game.new_asteroid(random.randrange(self.width), random.randrange(50, 150))
        self.player.set_position(self.width/2, self.height/2)
        for i in range(8):
            self.game.new_asteroid(random.randrange(self.width), random.randrange(50, 150))

    def prepare_level_two(self):
        self.player.set_position(self.width/2, self.height/2)
        for i in range(30):
            self.game.new_asteroid(random.randrange(self.width), random.randrange(50, 150))
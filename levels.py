import random


class LevelSystem:
    def __init__(self, game, space_ship, width, height):
        self.game = game
        self.player = space_ship
        self.width = width
        self.height = height
        self.levels = [self.level_one, self.level_two, self.level_three]
        self.current_level = -1
        self.ufo_start_poses_x = [0, width]
        self.ufo_start_poses_y = [0, height]

    def set_next_level(self):
        if self.current_level + 1 == len(self.levels):
            self.current_level = 2
        else:
            self.current_level += 1
        self.levels[self.current_level]()

    def set_first_level(self):
        self.current_level = 0
        self.level_one()

    def level_one(self):
        self.player.set_position(self.width/2, self.height/2)
        for i in range(2):
            self.game.new_asteroid(random.randrange(self.width), random.randrange(50, 150), 2)
            self.game.new_asteroid(random.randrange(self.width), random.randrange(50, 150), 1)

    def level_two(self):
        self.player.set_position(self.width/2, self.height/2)
        for i in range(4):
            self.game.new_asteroid(random.randrange(self.width), random.randrange(50, 150), 2)
            self.game.new_asteroid(random.randrange(self.width), random.randrange(50, 150), 1)

    def level_three(self):
        self.player.set_position(self.width/2, self.height/2)
        for i in range(6):
            self.game.new_asteroid(random.randrange(self.width), random.randrange(50, 150), 2)
            self.game.new_asteroid(random.randrange(self.width), random.randrange(50, 150), 1)

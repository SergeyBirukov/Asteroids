import random


class LevelSystem:
    def __init__(self, game, space_ship, width, height):
        self.game = game
        self.player = space_ship
        self.width = width
        self.height = height
        self.current_level = -1
        self.max_level = 2
        self.ufo_start_poses_x = [0, width]
        self.ufo_start_poses_y = [0, height]

    def set_next_level(self):
        if self.current_level + 1 > self.max_level:
            self.current_level = self.max_level
        else:
            self.current_level += 1
        self.set_up_level(2+self.current_level*2)

    def set_first_level(self):
        self.current_level = 0
        self.set_up_level(2)

    def set_up_level(self, count):
        for i in range(count):
            self.game.new_asteroid(random.randrange(self.width), random.randrange(50, 150), 2)
            self.game.new_asteroid(random.randrange(self.width), random.randrange(50, 150), 1)

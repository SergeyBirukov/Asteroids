from os import path

import random
import pygame
import asteroid
from player import Player, Bullet
import Levels
from interface import Interface
from resources import Resources

pygame.init()

img_dir = path.join(path.dirname(__file__), "img")
sound_dir = path.join(path.dirname(__file__), "sound")


FPS = 60
score = 0

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Game:
    def __init__(self, resources):
        pygame.mixer.init()
        self.score = 0
        self.resources = resources
        pygame.display.set_caption("Asteroids")
        self.clock = pygame.time.Clock()
        self.all_sprites = all_sprites = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.player = Player(resources.player_img, resources.lazer, resources.WIDTH / 2, resources.HEIGHT - 250)
        self.all_sprites.add(self.player)
        self.lvl_system = Levels.LevelSystem(self, self.player, self.resources.WIDTH, self.resources.HEIGHT)
        self.lvl_system.set_next_level()

    def new_asteroid(self, position_x, position_y):
        a = asteroid.Asteroid(random.choice(self.resources.asteroid_images), position_x, position_y)
        self.all_sprites.add(a)
        self.asteroids.add(a)

    def keep_player_on_screen(self, player):
        if player.rect.x > self.resources.WIDTH + 40:
            player.set_position(-40, player.rect.y)
        if player.rect.x < -100:
            player.set_position(self.resources.WIDTH + 40, player.rect.y)
        if player.rect.y < -100:
            player.set_position(player.rect.x, self.resources.HEIGHT)
        if player.rect.y > self.resources.HEIGHT:
            player.set_position(player.rect.x, 0)

    def keep_asteroid_on_screen(self, this_asteroid):
        if this_asteroid.rect.x > self.resources.WIDTH+30:
            this_asteroid.set_position(0, this_asteroid.rect.y)
        if this_asteroid.rect.x < -30:
            this_asteroid.set_position(self.resources.WIDTH, this_asteroid.rect.y)
        # if this_asteroid.rect.y < 0:
        #     this_asteroid.set_position(player.rect.x, HEIGHT)
        if this_asteroid.rect.y > self.resources.HEIGHT + 30:
            this_asteroid.set_position(this_asteroid.rect.x, -60)

    def process_events(self):
        for event in pygame.event.get():
            # check closing window
            if event.type == pygame.QUIT:
                running = False
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP] or keystate[pygame.K_w]:
            player_moving = True
            self.player.move_up()
        if keystate[pygame.K_DOWN]:
            now = pygame.time.get_ticks()
            if now - self.player.last_hyperspace > self.player.hyperspace_delay:
                self.player.set_position(random.randrange(0, 800), random.randrange(0, 800))
                self.player.last_hyperspace = now
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            player_moving = True
            self.player.rotate_left()
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            player_moving = True
            self.player.rotate_right()
        if keystate[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.player.last_shoot > self.player.shoot_delay:
                bullet = self.player.shoot()
                self.all_sprites.add(bullet)
                self.bullets.add(bullet)
                self.player.last_shoot = now

    def process_hits(self):
        hits = pygame.sprite.groupcollide(self.asteroids, self.bullets, True,
                                          True)
        for hit in hits:
            self.score += 70 - hit.radius

        hits = pygame.sprite.spritecollide(self.player, self.asteroids, True, pygame.sprite.collide_circle)
        for hit in hits:
            self.player.shield -= hit.radius
            game.new_asteroid(random.randrange(self.resources.WIDTH), random.randrange(-150, -50))
            if self.player.shield <= 0:
                self.player.hide()
                self.player.lives -= 1
                self.player.shield = 100

    def draw(self):
        self.resources.screen.fill(BLACK)
        self.resources.screen.blit(self.resources.background, self.resources.background_rect)
        self.all_sprites.draw(self.resources.screen)
        Interface.draw_text(self.resources.screen, "Score: " + str(len(self.asteroids)),
                            18, self.resources.WIDTH / 2, 10,
                            self.resources.font_name)
        Interface.draw_shield_bar(self.resources.screen, 5, 5, self.player.shield)
        Interface.draw_lives(self.resources.screen, self.resources.WIDTH - 100, 5,
                             self.player.lives, self.resources.player_mini_img)
        pygame.display.flip()

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            clock.tick(FPS)
            if len(self.asteroids) == 0:
                self.lvl_system.set_next_level()
            self.process_events()
            self.player.idle()
            self.keep_player_on_screen(self.player)
            for a in self.asteroids:
                self.keep_asteroid_on_screen(a)
            self.all_sprites.update()
            if self.player.lives == 0:
                running = False


if __name__ == '__main__':
    game = Game(resources=Resources(img_dir))
    game.run()

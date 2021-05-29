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
        self.all_sprites = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.player = Player(resources.player_img, resources.lazer, resources.WIDTH / 2, resources.HEIGHT - 250)
        self.all_sprites.add(self.player)
        self.lvl_system = Levels.LevelSystem(self, self.player, self.resources.WIDTH, self.resources.HEIGHT)
        self.lvl_system.set_next_level()
        self.running = False

    def new_asteroid(self, position_x, position_y, size):
        if size == 2:
            a = asteroid.Asteroid(random.choice(self.resources.asteroid_big_images), size, position_x, position_y)
        if size == 1:
            a = asteroid.Asteroid(random.choice(self.resources.asteroid_medium_images), size, position_x, position_y)
        if size == 0:
            a = asteroid.Asteroid(random.choice(self.resources.asteroid_small_images), size, position_x, position_y)
        self.all_sprites.add(a)
        self.asteroids.add(a)

    def keep_player_on_screen(self, player):
        if player.rect.centerx > self.resources.WIDTH:
            player.set_position(0, player.rect.y)
        if player.rect.centerx < 0:
            player.set_position(self.resources.WIDTH, player.rect.y)
        if player.rect.centery < 0:
            player.set_position(player.rect.x, self.resources.HEIGHT)
        if player.rect.centery > self.resources.HEIGHT:
            player.set_position(player.rect.x, 0)

    def keep_asteroid_on_screen(self, this_asteroid):
        if this_asteroid.rect.centerx > self.resources.WIDTH:
            this_asteroid.set_position(0, this_asteroid.rect.y)
        if this_asteroid.rect.centerx < 0:
            this_asteroid.set_position(self.resources.WIDTH, this_asteroid.rect.y)
        if this_asteroid.rect.centery < 0:
            this_asteroid.set_position(this_asteroid.rect.x, self.resources.HEIGHT)
        if this_asteroid.rect.centery > self.resources.HEIGHT:
            this_asteroid.set_position(this_asteroid.rect.x, 0)

    def process_events(self):
        for event in pygame.event.get():
            # check closing window
            if event.type == pygame.QUIT:
                self.running = False
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP] or keystate[pygame.K_w]:
            self.player.move_up()
        if keystate[pygame.K_DOWN]:
            now = pygame.time.get_ticks()
            if now - self.player.last_hyperspace > self.player.hyperspace_delay:
                self.player.set_position(random.randrange(0, 800), random.randrange(0, 800))
                self.player.last_hyperspace = now
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.player.rotate_left()
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.player.rotate_right()
        if keystate[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.player.last_shoot > self.player.shoot_delay:
                bullet = self.player.shoot()
                self.all_sprites.add(bullet)
                self.bullets.add(bullet)
                self.player.last_shoot = now

    def process_hits(self):
        hits = pygame.sprite.groupcollide(self.asteroids, self.bullets, True, True, collided=pygame.sprite.collide_mask)
        for hit in hits.keys():
            self.score += 70 - hit.radius
            if hit.type == 2:
                game.new_asteroid(hit.rect.x, hit.rect.y, 1)
                game.new_asteroid(hit.rect.x, hit.rect.y, 1)
            if hit.type == 1:
                game.new_asteroid(hit.rect.x, hit.rect.y, 0)
                game.new_asteroid(hit.rect.x, hit.rect.y, 0)

        hits = pygame.sprite.spritecollide(self.player, self.asteroids, True, collided=pygame.sprite.collide_mask)
        for hit in hits:
            self.player.shield -= hit.radius
            # game.new_asteroid(random.randrange(self.resources.WIDTH), random.randrange(-150, -50))
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
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(FPS)
            if len(self.asteroids) == 0:
                self.lvl_system.set_next_level()
            self.process_events()
            self.process_hits()
            self.player.idle()
            self.keep_player_on_screen(self.player)
            for a in self.asteroids:
                self.keep_asteroid_on_screen(a)
            self.all_sprites.update()
            if self.player.lives == 0:
                running = False
            self.draw()


if __name__ == '__main__':
    game = Game(resources=Resources(img_dir))
    game.run()

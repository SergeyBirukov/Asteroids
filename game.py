import random
import pygame
import asteroid
from player import Player
import Levels
from interface import Interface
from resources import Resources
from powerUp import Pow
from os import path
import sys

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
        self.powerups_sprites = pygame.sprite.Group()
        self.player = Player(resources.player_img, resources.player_with_shield_image, resources.lazer, resources.WIDTH / 2, resources.HEIGHT - 250)
        self.all_sprites.add(self.player)
        self.lvl_system = Levels.LevelSystem(self, self.player, self.resources.WIDTH, self.resources.HEIGHT)
        self.lvl_system.set_next_level()
        self.running = False
        self.isPause = False
        self.isGameOver = False
        self.click = False
        self.mx, self.my = pygame.mouse.get_pos()

    def new_asteroid(self, position_x, position_y, size):
        if size == 2:
            a = asteroid.Asteroid(random.choice(self.resources.asteroid_big_images), size, position_x, position_y)
        if size == 1:
            a = asteroid.Asteroid(random.choice(self.resources.asteroid_medium_images), size, position_x, position_y)
        if size == 0:
            a = asteroid.Asteroid(random.choice(self.resources.asteroid_small_images), size, position_x, position_y)
        self.all_sprites.add(a)
        self.asteroids.add(a)

    def _keep_on_screen(self, obj):
        if obj.rect.centerx > self.resources.WIDTH:
            obj.set_position(0, obj.rect.y)
        if obj.rect.centerx < 0:
            obj.set_position(self.resources.WIDTH, obj.rect.y)
        if obj.rect.centery < 0:
            obj.set_position(obj.rect.x, self.resources.HEIGHT)
        if obj.rect.centery > self.resources.HEIGHT:
            obj.set_position(obj.rect.x, 0)

    def _process_events(self):
        self.click = False
        for event in pygame.event.get():
            # check closing window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.isPause = not self.isPause
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click = True
        if not self.isPause:
            key_state = pygame.key.get_pressed()
            if key_state[pygame.K_UP] or key_state[pygame.K_w]:
                self.player.move_up()
            if key_state[pygame.K_DOWN]:
                now = pygame.time.get_ticks()
                if now - self.player.last_hyperspace > self.player.hyperspace_delay:
                    self.player.set_position(random.randrange(0, 800), random.randrange(0, 800))
                    self.player.last_hyperspace = now
            if key_state[pygame.K_LEFT] or key_state[pygame.K_a]:
                self.player.rotate_left()
            if key_state[pygame.K_RIGHT] or key_state[pygame.K_d]:
                self.player.rotate_right()
            if key_state[pygame.K_SPACE]:
                now = pygame.time.get_ticks()
                if now - self.player.last_shoot > self.player.shoot_delay:
                    bullet = self.player.shoot()
                    self.all_sprites.add(bullet)
                    self.bullets.add(bullet)
                    self.player.last_shoot = now


    def _process_hits(self):
        bullet_hits = pygame.sprite.groupcollide(self.asteroids, self.bullets, True, True, collided=pygame.sprite.collide_mask)
        for hit in bullet_hits.keys():
            self.score += 70 - hit.radius
            if hit.type == 2:
                rnd = random.randrange(1, 10)
                if rnd > 5:
                    pow = Pow(hit.rect.center, img_dir)
                    self.all_sprites.add(pow)
                    self.powerups_sprites.add(pow)
                self.new_asteroid(hit.rect.x, hit.rect.y, 1)
                self.new_asteroid(hit.rect.x, hit.rect.y, 1)
            if hit.type == 1:
                self.new_asteroid(hit.rect.x, hit.rect.y, 0)
                self.new_asteroid(hit.rect.x, hit.rect.y, 0)

        player_hits = pygame.sprite.spritecollide(self.player, self.asteroids, True, collided=pygame.sprite.collide_mask)
        for hit in player_hits:
            if not self.player.is_shield_on:
                self.player.HP -= hit.radius
            if self.player.HP <= 0:
                self.player.hide()
                self.player.lives -= 1
                self.player.gun_level = 0
                self.player.HP = 100

        bonus_hits = pygame.sprite.spritecollide(self.player, self.powerups_sprites, True, collided=pygame.sprite.collide_mask)
        for hit in bonus_hits:
            if hit.type == "live" and self.player.lives < 3:
                self.player.lives += 1
            if hit.type == "gun" and self.player.gun_level <2:
                self.player.gun_level_up()
            if hit.type == "shield":
                self.player.shield_on()

    def _draw(self):
        self.resources.screen.fill(BLACK)
        self.resources.screen.blit(self.resources.background, self.resources.background_rect)
        self.all_sprites.draw(self.resources.screen)
        if self.isGameOver:
            self.game_over_interface()
        elif self.isPause:
            self.pause_interface()
        else:
            Interface.draw_text(self.resources.screen, "Score: " + str(len(self.asteroids)),
                                18, self.resources.WIDTH / 2, 10,
                                self.resources.font_name, WHITE)
            Interface.draw_shield_bar(self.resources.screen, 5, 5, self.player.HP)
            Interface.draw_lives(self.resources.screen, self.resources.WIDTH - 100, 5,
                                 self.player.lives, self.resources.player_mini_img)

        pygame.display.flip()

    def pause_interface(self):
        Interface.draw_text(self.resources.screen, "Pause",
                            52, self.resources.WIDTH / 2, self.resources.HEIGHT/2 - 100,
                            self.resources.font_name, WHITE)
        button1 = pygame.Rect(self.resources.screen.get_width() / 2 - 100, self.resources.screen.get_height() / 2, 200, 50)
        pygame.draw.rect(self.resources.screen, (255, 255, 255), button1)
        Interface.draw_text(screen=self.resources.screen, text="Main menu", size=28, x=self.resources.screen.get_width() / 2,
                            y=self.resources.screen.get_height() / 2 + 10,
                            font=self.resources.font_name, color=BLACK)
        if button1.collidepoint(self.mx, self.my):
            if self.click:
                self.running = False

    def game_over_interface(self):
        Interface.draw_text(self.resources.screen, "Game Over",
                            52, self.resources.WIDTH / 2, self.resources.HEIGHT / 2 - 100,
                            self.resources.font_name, RED)
        button1 = pygame.Rect(self.resources.screen.get_width() / 2 - 100, self.resources.screen.get_height() / 2, 200, 50)
        pygame.draw.rect(self.resources.screen, (255, 255, 255), button1)
        Interface.draw_text(screen=self.resources.screen, text="Main menu", size=28, x=self.resources.screen.get_width() / 2,
                            y=self.resources.screen.get_height() / 2 + 10,
                            font=self.resources.font_name, color=BLACK)
        if button1.collidepoint(self.mx, self.my):
            if self.click:
                self.running = False

    def run(self):
        self.running, self.isPause = True, False
        clock = pygame.time.Clock()
        while self.running:
            self.mx, self.my = pygame.mouse.get_pos()
            clock.tick(FPS)
            if len(self.asteroids) == 0:
                self.lvl_system.set_next_level()
            self._process_events()
            self._process_hits()
            self.player.idle()
            if not self.player.hidden:
                self._keep_on_screen(self.player)
            for a in self.asteroids:
                self._keep_on_screen(a)
            for bullet in self.bullets:
                self._keep_on_screen(bullet)
            if not self.isPause and not self.isGameOver:
                self.all_sprites.update()
            if self.player.lives == 0:
                self.isGameOver = True
            self._draw()


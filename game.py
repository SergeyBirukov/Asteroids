import random
import pygame
import asteroid
from UFO import UFO
from player import Player
import levels
from interface import Interface
from powerUp import PowerUp
from leaderboard import LeaderBoard
import sys

FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Game:
    def __init__(self, resources):
        self.resources = resources
        self.leaderboard = LeaderBoard()
        pygame.display.set_caption("Asteroids")

        self.all_sprites = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.ufos = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.ufo_bullets = pygame.sprite.Group()
        self.power_up_sprites = pygame.sprite.Group()

        self.clock = pygame.time.Clock()
        self.ufo_last_spawned = pygame.time.get_ticks()
        self.ufo_spawn_delay = 20000

        self.player = Player(self.resources.player_img, self.resources.player_with_shield_image,
                             self.resources.laser, self.resources.WIDTH / 2, self.resources.HEIGHT - 250)
        self.all_sprites.add(self.player)
        self.lvl_system = levels.LevelSystem(self, self.player, self.resources.WIDTH, self.resources.HEIGHT)
        self.lvl_system.set_next_level()

        self.running = False
        self.isPause = False
        self.isGameOver = False
        self.click = False
        self.need_input = False
        self.mx, self.my = pygame.mouse.get_pos()
        self.input_text = ""
        self.score = 0
        self.power_up_probability = 5
        self.temp = 0
        self.game_over_buttons = [
            Interface.Button(self.resources.screen, self.resources.screen.get_width() * 0.75, self.resources.screen.get_height() * 0.9,
                             150, 50, "Main menu", self.resources.font_name, self.stop_game),
            Interface.Button(self.resources.screen, self.resources.screen.get_width() / 2 - 100, self.resources.screen.get_height() / 2 * 1.3,
                             200, 50, "Save score", self.resources.font_name, self.save_score_action)]
        self.pause_buttons = [Interface.Button(self.resources.screen, self.resources.WIDTH * 0.75, self.resources.HEIGHT * 0.9,
                                               150, 50, "Main menu", self.resources.font_name, self.stop_game)]

    def new_asteroid(self, position_x, position_y, size):
        if size == 2:
            a = asteroid.Asteroid(random.choice(self.resources.asteroid_big_images), size, position_x, position_y)
        if size == 1:
            a = asteroid.Asteroid(random.choice(self.resources.asteroid_medium_images), size, position_x, position_y)
        if size == 0:
            a = asteroid.Asteroid(random.choice(self.resources.asteroid_small_images), size, position_x, position_y)
        self.all_sprites.add(a)
        self.asteroids.add(a)

    def new_power_up(self, pos_x, pos_y, type=None):
        if type is None:
            power_up = PowerUp(pos_x, pos_y, self.resources.img_dir)
        else:
            power_up = PowerUp(pos_x, pos_y, self.resources.img_dir, type)
        self.all_sprites.add(power_up)
        self.power_up_sprites.add(power_up)

    def get_player_position(self):
        return self.player.rect.centerx, self.player.rect.centery

    def new_UFO(self):
        now = pygame.time.get_ticks()
        if now - self.ufo_last_spawned > self.ufo_spawn_delay:
            self.ufo_last_spawned = now
            u = UFO(self.resources.ufo_image, self.resources.UFO_laser, self.resources.WIDTH, self.resources.HEIGHT)
            self.all_sprites.add(u)
            self.ufos.add(u)

    def _UFO_try_to_shoot(self, u):
        bullet = u.shoot(pygame.time.get_ticks(), self.get_player_position())
        if bullet is not None:
            self.all_sprites.add(bullet)
            self.ufo_bullets.add(bullet)

    def _keep_on_screen(self, obj):
        if obj.rect.centerx > self.resources.WIDTH:
            obj.set_position(0, obj.rect.y)
        if obj.rect.centerx < 0:
            obj.set_position(self.resources.WIDTH, obj.rect.y)
        if obj.rect.centery < 0:
            obj.set_position(obj.rect.x, self.resources.HEIGHT)
        if obj.rect.centery > self.resources.HEIGHT:
            obj.set_position(obj.rect.x, 0)

    def _process_input(self, event):
        if event.key == pygame.K_RETURN:
            self.leaderboard.save_score(self.input_text, self.score)
            self.input_text = ""
            self.leaderboard.run()
            self.running = False
        if event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        elif len(self.input_text) < 15:
            self.input_text += event.unicode

    def _process_events(self):
        self.click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not self.isPause:
                        self.temp = self.ufo_last_spawned
                    else:
                        self.ufo_last_spawned = self.temp
                    self.isPause = not self.isPause
                if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and not self.isPause and not self.isGameOver:
                    self.player.hyperspace()
                    pygame.mixer.Sound.play(self.resources.teleport_sound)
                elif self.need_input:
                    self._process_input(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click = True
        if self.isPause or self.isGameOver:
            return
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_UP] or key_state[pygame.K_w]:
            self.player.move_up(self.player.offset)
        if key_state[pygame.K_LEFT] or key_state[pygame.K_a]:
            self.player.rotate(is_left=True)
        if key_state[pygame.K_RIGHT] or key_state[pygame.K_d]:
            self.player.rotate(is_left=False)
        if key_state[pygame.K_SPACE]:
            self._process_player_shoot()

    def _process_player_shoot(self):
        now = pygame.time.get_ticks()
        if now - self.player.last_shoot > self.player.shoot_delay:
            pygame.mixer.Sound.play(self.resources.shoot_sound)
            bullet = self.player.shoot()
            self.all_sprites.add(bullet)
            self.bullets.add(bullet)
            self.player.last_shoot = now

    def _process_hits(self):
        bullet_hits = pygame.sprite.groupcollide(self.asteroids, self.bullets, True, True, collided=pygame.sprite.collide_mask)
        bullet_hits.update(pygame.sprite.groupcollide(self.ufos, self.bullets, False, True, collided=pygame.sprite.collide_mask))
        for hit in bullet_hits.keys():
            self.score += 70 - hit.radius
            pygame.mixer.Sound.play(self.resources.explosion_sound2)
            if hit.type == 2:
                rnd = random.randrange(1, 10)
                if rnd - self.power_up_probability > 0:
                    self.new_power_up(hit.rect.centerx, hit.rect.centery)
                self.new_asteroid(hit.rect.x, hit.rect.y, 1)
                self.new_asteroid(hit.rect.x, hit.rect.y, 1)
            if hit.type == 1:
                self.new_asteroid(hit.rect.x, hit.rect.y, 0)
                self.new_asteroid(hit.rect.x, hit.rect.y, 0)
            if hit.type == "UFO":
                hit.HP -= 1
                self.score += 70 - hit.radius

        player_hits = pygame.sprite.spritecollide(self.player, self.asteroids, True, collided=pygame.sprite.collide_mask)
        for hit in player_hits:
            pygame.mixer.Sound.play(self.resources.explosion_sound)
            if not self.player.is_shield_on:
                self.player.HP -= hit.radius
            if self.player.HP <= 0:
                self.player.hide()
                self.player.lives -= 1
                self.player.gun_level = 0
                self.player.HP = 100

        ufos_hits = pygame.sprite.spritecollide(self.player, self.ufos, True, collided=pygame.sprite.collide_mask)
        for hit in ufos_hits:
            if not self.player.is_shield_on:
                self.player.HP -= hit.radius

        ufo_bullets_hits = pygame.sprite.spritecollide(self.player, self.ufo_bullets, True, collided=pygame.sprite.collide_mask)
        for hit in ufo_bullets_hits:
            if not self.player.is_shield_on:
                self.player.HP -= hit.radius
            if self.player.HP <= 0:
                self.player.hide()
                self.player.lives -= 1
                self.player.gun_level = 0
                self.player.HP = self.player.max_HP

        bonus_hits = pygame.sprite.spritecollide(self.player, self.power_up_sprites, True, collided=pygame.sprite.collide_mask)
        for hit in bonus_hits:
            pygame.mixer.Sound.play(self.resources.bonus_sound)
            if hit.type == "live" and self.player.lives < 3:
                self.player.lives += 1
            if hit.type == "gun" and self.player.gun_level < 2:
                self.player.gun_level_up()
            if hit.type == "shield":
                self.player.shield_on()

    def _draw(self):
        self.resources.screen.fill(BLACK)
        self.resources.screen.blit(self.resources.background, self.resources.background_rect)
        self.all_sprites.draw(self.resources.screen)
        if self.isGameOver:
            self.game_over()
        elif self.isPause:
            self.pause()
        else:
            Interface.draw_text_centered(self.resources.screen, "Score: " + str(self.score),
                                         18, self.resources.WIDTH / 2, 10,
                                         self.resources.font_name, WHITE)
            Interface.draw_shield_bar(self.resources.screen, 5, 5, self.player.HP)
            Interface.draw_lives(self.resources.screen, self.resources.WIDTH * 0.9, 5,
                                 self.player.lives, self.resources.player_mini_img)
        pygame.display.flip()

    def pause(self):
        Interface.draw_text_centered(self.resources.screen, "Pause", 52, self.resources.WIDTH / 2,
                                     (self.resources.HEIGHT / 2) * 0.9, self.resources.font_name, WHITE)
        for button in self.pause_buttons:
            button.handle(self.mx, self.my, self.click)

    def stop_game(self):
        self.running = False

    def save_score_action(self):
        if self.input_text != "":
            self.leaderboard.save_score(self.input_text, self.score)
            self.input_text = ""
            self.leaderboard.run()
            self.running = False

    def game_over(self):
        self.need_input = True
        Interface.draw_text_centered(self.resources.screen, "Game Over",
                                     52, self.resources.WIDTH / 2, self.resources.HEIGHT / 2 - self.resources.HEIGHT * 0.2,
                                     self.resources.font_name, RED)
        Interface.draw_text_centered(self.resources.screen, "Your score: " + str(self.score),
                                     52, self.resources.WIDTH / 2, self.resources.HEIGHT / 2 - self.resources.HEIGHT * 0.1,
                                     self.resources.font_name, WHITE)
        entry_field = pygame.Rect(self.resources.screen.get_width() * 0.15, self.resources.screen.get_height() / 2,
                                  self.resources.screen.get_width() * 0.7, 50)
        pygame.draw.rect(self.resources.screen, WHITE, entry_field)
        Interface.draw_text_centered(self.resources.screen, "Enter your name: ", 30,
                                     self.resources.screen.get_width() * 0.28, self.resources.screen.get_height() / 2 + 5, self.resources.font_name,
                                     BLACK)
        Interface.draw_text(self.resources.screen, self.input_text, 30,
                            self.resources.screen.get_width() / 2 - self.resources.WIDTH * 0.05, self.resources.screen.get_height() / 2 + 5,
                            self.resources.font_name, BLACK)
        for button in self.game_over_buttons:
            button.handle(self.mx, self.my, self.click)

    def quit(self):
        pygame.quit()
        sys.exit()

    def run(self):
        self.running, self.isPause = True, False
        clock = pygame.time.Clock()
        while self.running:
            self.mx, self.my = pygame.mouse.get_pos()
            if len(self.asteroids) == 0:
                self.lvl_system.set_next_level()
            self._process_events()
            self._process_hits()
            self.player.idle()
            if self.player.HP <= 0:
                self.player.respawn()
            for u in self.ufos:
                self._UFO_try_to_shoot(u)
                self._keep_on_screen(u)
            if not self.player.hidden:
                self._keep_on_screen(self.player)
            for a in self.asteroids:
                self._keep_on_screen(a)
            for bullet in self.bullets:
                self._keep_on_screen(bullet)
            if not self.isPause and not self.isGameOver:
                self.all_sprites.update()
                self.new_UFO()
            if self.player.lives == 0:
                self.player.kill()
                self.isGameOver = True
            self._draw()
            self.clock.tick(60)

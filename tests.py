import unittest
import pygame
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'
os.environ["SDL_VIDEODRIVER"] = "dummy"
from resources import Resources
from game import Game
from threading import Thread
from time import sleep


class TestGame(unittest.TestCase):
    def setUp(self):
        pygame.init()
        # pygame.mixer.init()
        self.resources = Resources()
        self.game = Game(self.resources)
        self.game_thread = Thread(target=self.game.run)

    def test_player_lives_decrease(self):
        self.game_thread.start()
        self.game.player.HP = -1
        sleep(0.1)
        self.assertLess(self.game.player.lives, self.game.player.max_lives)
        self.game.running = False

    def test_player_die(self):
        self.game_thread.start()
        self.game.player.lives = 0
        sleep(0.1)
        self.assertEqual(self.game.player.groups(), [])
        self.game.running = False

    def test_player_get_damage_from_asteroid(self):
        self.game_thread.start()
        self.game.new_asteroid(position_x=self.game.player.rect.centerx, position_y= self.game.player.rect.centery, size=2)
        sleep(0.1)
        self.assertLess(self.game.player.HP, self.game.player.max_HP)
        self.game.running = False

    def test_player_get_damage_from_UFO(self):
        self.game_thread.start()
        self.game.ufo_last_spawned = -self.game.ufo_spawn_delay
        self.game.new_UFO()
        for ufo in self.game.ufos:
            ufo.set_position(self.game.player.rect.centerx, self.game.player.rect.centery)
        sleep(0.1)
        self.assertLess(self.game.player.HP, self.game.player.max_HP)
        self.game.running = False

    def test_player_get_damage_from_UFO_bullet(self):
        self.game_thread.start()
        self.game.ufo_last_spawned = -self.game.ufo_spawn_delay
        self.game.new_UFO()
        for u in self.game.ufos:
            u.shoot_delay = -3000
            self.game._UFO_try_to_shoot(u)
        for bullet in self.game.ufo_bullets:
            bullet.set_position(self.game.player.rect.centerx, self.game.player.rect.centery)
        sleep(0.1)
        self.assertLess(self.game.player.HP, self.game.player.max_HP)
        self.game.running = False

    def test_player_get_gun_power_up(self):
        self.game_thread.start()
        self.game.new_power_up(self.game.player.rect.centerx, self.game.player.rect.centery, "gun")
        sleep(0.1)
        self.assertGreater(self.game.player.gun_level, 0)
        self.game.running = False

    def test_player_get_live(self):
        self.game_thread.start()
        self.game.player.lives -= 1
        self.game.new_power_up(self.game.player.rect.centerx, self.game.player.rect.centery, "live")
        sleep(0.1)
        self.assertEqual(self.game.player.lives, self.game.player.max_lives)
        self.game.running = False

    def test_player_get_shield(self):
        self.game_thread.start()
        self.game.player.lives = 2
        self.game.new_power_up(self.game.player.rect.centerx, self.game.player.rect.centery, "shield")
        sleep(0.1)
        self.assertEqual(self.game.player.is_shield_on, True)
        self.game.running = False

    def test_player_with_shield_dont_get_damage_from_asteroid(self):
        self.game_thread.start()
        self.game.player.is_shield_on = True
        self.game.new_asteroid(position_x=self.game.player.rect.centerx, position_y= self.game.player.rect.centery, size=2)
        sleep(0.1)
        self.assertEqual(self.game.player.HP, self.game.player.max_HP)
        self.game.running = False

    def test_player_with_shield_dont_get_damage_from_UFO(self):
        self.game_thread.start()
        self.game.player.is_shield_on = True
        self.game.ufo_last_spawned = -10000
        self.game.new_UFO()
        for ufo in self.game.ufos:
            ufo.set_position(self.game.player.rect.centerx, self.game.player.rect.centery)
        sleep(0.1)
        self.assertEqual(self.game.player.HP, self.game.player.max_HP)
        self.game.running = False

    def test_player_with_shield_dont_get_damage_from_UFO_bullet(self):
        self.game_thread.start()
        self.game.player.is_shield_on = True
        self.game.ufo_last_spawned = -self.game.ufo_spawn_delay
        self.game.new_UFO()
        for u in self.game.ufos:
            u.shoot_delay = -u.shoot_delay
            self.game._UFO_try_to_shoot(u)
        for bullet in self.game.ufo_bullets:
            bullet.set_position(self.game.player.rect.centerx, self.game.player.rect.centery)
        sleep(0.1)
        self.assertEqual(self.game.player.HP, self.game.player.max_HP)
        self.game.running = False

    def test_UFO_get_damage(self):
        self.game_thread.start()
        self.game.ufo_last_spawned = -self.game.ufo_spawn_delay
        self.game.new_UFO()
        self.game.player.shoot_delay = -10
        for ufo in self.game.ufos:
            ufo.set_position(self.game.player.rect.centerx, self.game.player.rect.centery - 100)
        self.game._process_player_shoot()
        for bullet in self.game.bullets:
            bullet.set_position(self.game.player.rect.centerx, self.game.player.rect.centery - 100)
        sleep(0.1)
        for ufo in self.game.ufos:
            self.assertLess(ufo.HP, ufo.max_HP)
        self.game.running = False

    def test_UFO_die(self):
        self.game_thread.start()
        self.game.ufo_last_spawned = -self.game.ufo_spawn_delay
        self.game.new_UFO()
        for ufo in self.game.ufos:
            ufo.HP = 0
        sleep(0.1)
        for ufo in self.game.ufos:
            self.assertEqual(ufo.groups(), [])
        self.game.running = False

    def test_score_increase(self):
        self.game_thread.start()
        self.game.player.shoot_delay = -10
        self.game._process_player_shoot()
        for asteroid in self.game.asteroids:
            asteroid.set_position(self.game.player.rect.centerx, self.game.player.rect.centery - 200)
        print(len(self.game.bullets))
        for bullet in self.game.bullets:
            bullet.speed_const = 100
            bullet.set_position(self.game.player.rect.centerx, self.game.player.rect.centery - 100)
        sleep(0.3)
        self.assertGreater(self.game.score, 0)
        self.game.running = False

    def test_asteroid_divide(self):
        self.game_thread.start()
        sleep(0.1)
        start_asteroid_count = len(self.game.asteroids)
        self.game.player.shoot_delay = -10
        self.game._process_player_shoot()
        for asteroid in self.game.asteroids:
            asteroid.set_position(self.game.player.rect.centerx, self.game.player.rect.centery - 210)
        for bullet in self.game.bullets:
            bullet.speed_const = 100
            bullet.set_position(self.game.player.rect.centerx, self.game.player.rect.centery - 190)
        sleep(0.3)
        self.assertGreater(len(self.game.asteroids), start_asteroid_count)
        self.game.running = False




from os import path

import random
import pygame
import asteroid
import player


img_dir = path.join(path.dirname(__file__), "img")
sound_dir = path.join(path.dirname(__file__), "sound")

WIDTH = 800
HEIGHT = 800
FPS = 60
score = 0

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def draw_text(surf, text, size, x, y, font):
    font = pygame.font.Font(font, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGHT = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGHT
    outline_rect = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Asteroids")
        self.clock = pygame.time.Clock()
        self.font_name = pygame.font.match_font('arial')
        self.background = pygame.image.load(
            path.join(img_dir, "space_shooter_background.png")).convert()
        self.background_rect = self.background.get_rect()
        self.player_img = pygame.image.load(
            path.join(img_dir, "playerShip1_red.png")).convert()
        self.player_mini_img = pygame.transform.scale(self.player_img, (25, 19))
        self.player_mini_img.set_colorkey((0, 0, 0))
        self.lazer = pygame.image.load(
            path.join(img_dir, "laserBlue03.png")).convert()
        self.asteroid_images = []
        self.asteroid_list = ["meteorBrown_med3.png", "meteorBrown_big1.png", "meteorBrown_big2.png",
                       "meteorBrown_big4.png",
                       "meteorBrown_med1.png"]
        for img in self.asteroid_list:
            self.asteroid_images.append(
                pygame.image.load(path.join(img_dir, img)).convert())


def new_asteroid(position_x, position_y, image=None):
    if image is None:
        image = random.choice(game.asteroid_images)
    else:
        image = game.asteroid_images[0]
    a = asteroid.Asteroid(image, position_x, position_y)
    all_sprites.add(a)
    asteroids.add(a)


def keep_player_on_screen():
    if player.rect.x > WIDTH + 40:
        player.set_position(-40, player.rect.y)
    if player.rect.x < -100:
        player.set_position(WIDTH + 40, player.rect.y)
    if player.rect.y < -100:
        player.set_position(player.rect.x, HEIGHT)
    if player.rect.y > HEIGHT:
        player.set_position(player.rect.x, 0)


def keep_asteroid_on_screen(this_asteroid):
    if this_asteroid.rect.x > WIDTH+30:
        this_asteroid.set_position(0, this_asteroid.rect.y)
    if this_asteroid.rect.x < -30:
        this_asteroid.set_position(WIDTH, this_asteroid.rect.y)
    # if this_asteroid.rect.y < 0:
    #     this_asteroid.set_position(player.rect.x, HEIGHT)
    if this_asteroid.rect.y > HEIGHT:
        this_asteroid.set_position(this_asteroid.rect.x, -60)


if __name__ == '__main__':
    game = Game()
    all_sprites = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = player.Player(game.player_img, game.lazer, WIDTH/2, HEIGHT-250)
    all_sprites.add(player)
    running = True
    clock = pygame.time.Clock()
    for i in range(1):
        new_asteroid(random.randrange(WIDTH), random.randrange(-150, -50))
    while running:
        # keep loop running at the right speed
        clock.tick(FPS)
        # Process input (events)
        for event in pygame.event.get():
            # check closing window
            if event.type == pygame.QUIT:
                running = False
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            player_moving = True
            player.move_up()
        if keystate[pygame.K_DOWN]:
            player_moving = True
            player.move_down()
        if keystate[pygame.K_LEFT]:
            player_moving = True
            player.move_left()
        if keystate[pygame.K_RIGHT]:
            player_moving = True
            player.move_right()
        if keystate[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - player.last_shoot > player.shoot_delay:
                bullet = player.shoot()
                all_sprites.add(bullet)
                bullets.add(bullet)
                player.last_shoot = now
        player.idle()
        all_sprites.update()
        # check to see if bullet hit the asteroid
        hit_small_asteroids_counter = 0
        hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
        for hit in hits:
            if hit.image_orig != game.asteroid_images[0]:
                score += 70 - hit.radius
                new_asteroid(hit.rect.x - 5, hit.rect.y, game.asteroid_images[0])
                new_asteroid(hit.rect.x + 5, hit.rect.y, game.asteroid_images[0])
                if hit_small_asteroids_counter == 2:
                    hit_small_asteroids_counter = 0
                    new_asteroid(random.randrange(WIDTH), random.randrange(-150, -50))
            else:
                hit_small_asteroids_counter += 1


        # check to see if asteroid hit the player
        hits = pygame.sprite.spritecollide(player, asteroids, True,
                                           pygame.sprite.collide_circle)
        for hit in hits:
            player.shield -= hit.radius
            new_asteroid(random.randrange(WIDTH), random.randrange(-150, -50))
            if player.shield <= 0:
                player.hide()
                player.lives -= 1
                player.shield = 100
                hide_time = pygame.time.get_ticks()


        keep_player_on_screen()
        for a in asteroids:
            keep_asteroid_on_screen(a)
        if player.lives == 0:
            running = False

        # Draw 
        game.screen.fill(BLACK)
        game.screen.blit(game.background, game.background_rect)
        all_sprites.draw(game.screen)
        pygame.draw.rect(game.screen, GREEN, (player.rect.x, player.rect.y, 5, 5))
        draw_text(game.screen, "Score: " + str(score), 18, WIDTH / 2, 10, game.font_name)
        draw_shield_bar(game.screen, 5, 5, player.shield)
        draw_lives(game.screen, WIDTH - 100, 5, player.lives, game.player_mini_img)

        pygame.display.flip()
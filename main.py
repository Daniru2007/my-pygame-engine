import pygame
import sys
import random


import engine as e
from engine.loadmap import Map


class Player(e.Entity):
    def __init__(self, x, y, width, height, e_type):
        self.score = 0
        super().__init__(x, y, width, height, e_type)


WINDOW_SIZE = [600, 400]
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface((300, 200))

player = Player(0, 0, 16, 16, 'idle')
player.set_image(pygame.image.load('data/imgs/player/player_1.png'))
player.load_animations("data/animations/player.json")

map = Map("data/imgs/tiles", "data/maps/level1")

building_image = pygame.image.load('data/imgs/objects/building.png')
coin_images = [pygame.image.load('data/imgs/objects/coin_1.png'),
               pygame.image.load('data/imgs/objects/coin_2.png')]
coin_frame = 0
coins = map.coins

health_tank_image = pygame.image.load('data/imgs/tiles/health_tank.png')
health_tanks = map.health_tanks

jumper_image = pygame.image.load("data/imgs/tiles/jumper.png")
jumpers = map.jumpers

larva = map.larva

buildings = []

for i in range(20):
    buildings.append([pygame.Rect(random.randint(
        0, map.act_width), random.randint(0, 500), random.randint(60, 300), map.act_height),
        round(random.uniform(0.0, 0.5), 2), (random.randint(20, 60), random.randint(90, 255),  random.randint(0, 1))])

buildings.sort(key=lambda x: x[1], reverse=True)

particles = []

font = pygame.font.Font('data/fonts/B04.ttf', 20)

shake = 0
scroll = [0, 0]
run = True
while run:
    score = font.render(f"score: {player.score}", True, (255, 255, 255))
    health = font.render(f"health: {round(player.health)}", True, (255, 255, 255))
    display.fill((0, 34, 34))
    player.gravity += 0.2
    if player.gravity > 5:
        player.gravity = 5

    scroll[0] += (player.x - scroll[0] - 152) / 10
    scroll[1] += (player.y - scroll[1] - 106) / 10

    for building in buildings:
        display.blit(building_image,  pygame.Rect(
            building[0].x - scroll[0] * building[1], building[0].y - scroll[1] * building[1], building[0].width, building[0].height))

    player.movement = [0, 0]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if player.air_time < 6:
                    player.gravity = -3
            if event.key == pygame.K_RIGHT:
                player.x_vel = 0
                player.right = [True, False]
                player.left = [False, True]
                player.set_action('run')
                player.flip = False
            if event.key == pygame.K_LEFT:
                player.x_vel = 0
                player.left = [True, False]
                player.right = [False, True]
                player.set_action('run')
                player.flip = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.right[1] = True
                player.set_action("idle")
            if event.key == pygame.K_LEFT:
                player.left[1] = True
                player.set_action("idle")

    for jumper in jumpers:
        if jumper.colliderect(player.rect()):
            player.gravity = -5
        display.blit(jumper_image, [jumper.x - scroll[0], jumper.y-scroll[1]])

    player.movement[1] = player.gravity

    if player.left[0]:
        if not player.left[1]:
            player.x_vel += 0.2
            if player.x_vel >= 3:
                player.x_vel = 3
        else:
            player.x_vel -= 0.1
            if player.x_vel <= 0:
                player.x_vel = 0
                player.left = [False, True]
        player.movement[0] = -player.x_vel
    elif player.right[0]:
        if not player.right[1]:
            player.x_vel += 0.2
            if player.x_vel >= 3:
                player.x_vel = 3
        else:
            player.x_vel -= 0.1
            if player.x_vel <= 0:
                player.x_vel = 0
                player.right = [False, True]
        player.movement[0] = player.x_vel

    for tile in larva:
        player_rect = player.obj.rect.copy()
        player_rect.y += 2
        if tile.colliderect(player_rect):
            player.health -= 0.01
            if player.movement[0] > 0:
                player.movement[0] *= 0.5
            if player.movement[0] < 0:
                # BUG(player moving left is not working properly)
                player.movement[0] *= 0.05
            player.movement[1] = 0
            break

    if shake > 0:
        shake -= 1
        scroll[0] += random.randint(0, 8) -4
        scroll[1] += random.randint(0, 8) -4

    collisions = player.move(map.tiles)
    if collisions["bottom"]:
        player.gravity = 0
        if player.air_time >= 50:
            shake = 20
        player.air_time = 0
    if collisions["top"]:
        player.gravity = 1

    if coin_frame > 14:
        coin_frame = 0
    for coin in coins.copy():
        if coin_frame <= 7:
            image = coin_images[0]
        if coin_frame > 7:
            image = coin_images[1]
        if coin.colliderect(player.obj.rect):
            player.score += 5
            coins.remove(coin)
        else:
            display.blit(image,
                         (coin.x - scroll[0], coin.y - scroll[1] - 2))
    coin_frame += 1

    player.air_time += 1

    player.animation_frame += 1
    if player.animation_frame > len(player.animation_database[player.action]) - 1:
        player.animation_frame = 0

    map.display(display, scroll)

    player.health -= 0.01
    for health_tank in health_tanks.copy():
        if health_tank.colliderect(player.obj.rect):
            player.health += 0.1
            if player.health > 10:
                player.health = 10
        else:
            display.blit(health_tank_image,
                         (health_tank.x - scroll[0], health_tank.y - scroll[1] - 2))
    if round(player.health) < 0:
        run = False
    player.display(display, scroll)

    mx, my = pygame.mouse.get_pos()

    for i in range(20):
        particles.append([[mx, my + random.uniform(0, 5.5)], 0, 255])

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    for particle in particles.copy():

        particles[particles.index(particle)][1] += 0.5
        particle[0][1] += random.uniform(-5, 5) + 5
        particle[0][0] += random.uniform(-5, 5)
        if particle[1] > 8:
            particles.remove(particle)
        particle[2] -= 255 / 40
        pygame.draw.circle(
            screen, (particle[2], particle[2], particle[2]), particle[0], particle[1])
    screen.blit(score, [0, 0])
    screen.blit(health, [0, 20])
    pygame.display.update()
    clock.tick(60)

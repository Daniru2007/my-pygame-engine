import pygame
import sys


import engine as e
from engine.loadmap import Map

WINDOW_SIZE = [600, 400]
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface((300, 200))

player = e.Entity(0, 0, 16, 16, 'idle')
player.set_image(pygame.image.load('data/imgs/player/player_1.png'))

map = Map("data/imgs/tiles", "data/maps/level1")

scroll = [0, 0]
run = True
while run:
    display.fill((0, 34, 34))
    player.gravity += 0.2
    if player.gravity > 5:
        player.gravity = 5

    scroll[0] += (player.x - scroll[0] - 152) / 10
    scroll[1] += (player.y - scroll[1] - 106) / 10

    player.movement = [0, 0]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if player.air_time < 6:
                    player.gravity = -6
            if event.key == pygame.K_RIGHT:
                player.x_vel = 0
                player.right = [True, False]
                player.left = [False, True]
            if event.key == pygame.K_LEFT:
                player.x_vel = 0
                player.left = [True, False]
                player.right = [False, True]
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.right[1] = True
            if event.key == pygame.K_LEFT:
                player.left[1] = True

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

    collisions = player.move(map.tiles)
    if collisions["bottom"]:
        player.gravity = 0
        player.air_time = 0

    player.air_time += 1

    map.display(display, scroll)
    player.display(display, scroll)
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)

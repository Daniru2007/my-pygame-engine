from curses import KEY_UP
import pygame
import sys


import engine as e

WINDOW_SIZE = [600, 400]
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface((300, 200))

player = e.Entity(100, 0, 32, 32, 'idle')
player.set_image(pygame.image.load('data/imgs/player/player_1.png'))

run = True
while run:
    display.fill((0, 34, 34))
    player.gravity += 0.2
    if player.gravity < 2:
        player.gravity = 2

    player.movement = [0, 0]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
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
    if not player.y + player.width > WINDOW_SIZE[1]:
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

    player.move()

    player.display(display, [0, 0])
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)

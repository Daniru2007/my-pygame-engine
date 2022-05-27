import pygame
import sys
import random


import engine as e
from engine.loadmap import Map

WINDOW_SIZE = [600, 400]
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface((300, 200))

player = e.Entity(0, 0, 16, 16, 'idle')
player.set_image(pygame.image.load('data/imgs/player/player_1.png'))
player.load_animations("data/animations/player.json")

map = Map("data/imgs/tiles", "data/maps/level1")

building = pygame.image.load('data/imgs/objects/building.png')

background_objects = []

for i in range(20):
    background_objects.append([pygame.Rect(random.randint(
        0, map.act_width), random.randint(0, 500), random.randint(60, 300), map.act_height),
        round(random.uniform(0.0, 0.5), 2), (random.randint(20, 60), random.randint(90, 255),  random.randint(0, 1))])

background_objects.sort(key=lambda x:x[1], reverse=True )

particles = []

scroll = [0, 0]
run = True
while run:
    display.fill((0, 34, 34))
    player.gravity += 0.2
    if player.gravity > 5:
        player.gravity = 5

    scroll[0] += (player.x - scroll[0] - 152) / 10
    scroll[1] += (player.y - scroll[1] - 106) / 10

    for object in background_objects:
        display.blit(building,  pygame.Rect(
            object[0].x - scroll[0] * object[1], object[0].y - scroll[1] * object[1], object[0].width, object[0].height))

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
    if collisions["top"]:
        player.gravity = 1

    player.air_time += 1

    player.animation_frame += 1
    if player.animation_frame > len(player.animation_database[player.action]) - 1:
        player.animation_frame = 0

    map.display(display, scroll)
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
        pygame.draw.circle(screen, (particle[2], particle[2], particle[2]), particle[0], particle[1])
    pygame.display.update()
    clock.tick(60)

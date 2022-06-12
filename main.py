import pygame
import sys
import random
import json


import engine as e
from engine.loadmap import Map
from engine.physics import collide_test


class Player(e.Entity):
    def __init__(self, x, y, width, height, e_type):
        self.score = 0
        super().__init__(x, y, width, height, e_type)
        self.bullet_delay = 0
        self.bullets = []
        self.facing = True  # True == right, False == left
        self.shoot = False


class Enemy(e.Entity):
    def __init__(self, x, y, width, height, e_type):
        super().__init__(x, y, width, height, e_type)
        self.health = 5


class Bullet(object):
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = 1 if direction else -1
        self.speed = 5

    def move(self):
        self.x += self.speed * self.direction

    def rect(self):
        return pygame.Rect(self.x, self.y, 2, 2)

    def display(self, display, scroll):
        pygame.draw.circle(display, (255, 255, 255), (self.x -
                           scroll[0], self.y - scroll[1]), 2)


class HealthBar(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.percent = 10

    def move(self, x, y):
        self.x = x
        self.y = y

    def display(self, display, scroll):
        pygame.draw.rect(display, (255, 255, 255),
                         ((self.x - scroll[0])-4, self.y-9 - scroll[1], 24, 9))
        pygame.draw.rect(display, (150, 0, 0),
                         ((self.x - scroll[0])-2, self.y-7 - scroll[1], 20, 5))
        pygame.draw.rect(display, (0, 150, 0), ((
            self.x - scroll[0])-2, self.y-7 - scroll[1], self.percent * 2, 5))
        text = font_pixel.render(
            f"{int(round(self.percent * 10))}%", True, (255, 255, 255))
        display.blit(text, (self.x - scroll[0] + 22, self.y - scroll[1] - 7))


WINDOW_SIZE = [600, 400]
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface((300, 200))

player_data = json.load(open("data/info.json"))
player = Player(player_data["position"][0],
                player_data["position"][1], 16, 16, 'idle')
player.set_image(pygame.image.load('data/imgs/player/player_1.png'))
player.load_animations("data/animations/player.json")

player.score = player_data["score"]

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

enemies = [Enemy(8*16, 6*16, 16, 16, "enemy"),
           Enemy(9*16, 7*16, 16, 16, "enemy"),
           Enemy(35*16, 56*16, 16, 16, "enemy"),
           ]

for i in range(len(enemies)):
    enemies[i].health_bar = HealthBar(enemies[i].x, enemies[i].y)
    enemies[i].health_bar.percent = 10

for i in range(len(enemies)):
    enemies[i].load_animations("data/animations/enemy.json")

for i in range(20):
    buildings.append([pygame.Rect(random.randint(
        0, map.act_width), random.randint(0, 500), random.randint(60, 300), map.act_height),
        round(random.uniform(0.0, 0.5), 2), (random.randint(20, 60), random.randint(90, 255),  random.randint(0, 1))])

buildings.sort(key=lambda x: x[1], reverse=True)

particles = []

font_B04 = pygame.font.Font('data/fonts/B04.ttf', 20)
font_pixel = pygame.font.Font('data/fonts/pixel.ttf', 8)

health_bar = HealthBar(player.x, player.y)

shake = 0
scroll = [0, 0]
run = True
while run:
    score = font_B04.render(f"score: {player.score}", True, (255, 255, 255))
    display.fill((0, 34, 34))
    player.gravity += 0.2
    if player.gravity > 8:
        player.gravity = 8

    health_bar.percent = player.health

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
                player.facing = True
                player.right = [True, False]
                player.left = [False, True]
                player.set_action('run')
                player.flip = False
            if event.key == pygame.K_LEFT:
                player.x_vel = 0
                player.facing = False
                player.left = [True, False]
                player.right = [False, True]
                player.set_action('run')
                player.flip = True
            if event.key == pygame.K_SPACE:
                player.shoot = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.right[1] = True
                player.set_action("idle")
            if event.key == pygame.K_LEFT:
                player.left[1] = True
                player.set_action("idle")
            if event.key == pygame.K_SPACE:
                player.shoot = False

    if player.bullet_delay > 0:
        player.bullet_delay -= 1

    if player.shoot:
        if player.bullet_delay <= 0:
            player.bullet_delay = 20
            if player.facing:
                player.bullets.append(
                    Bullet(player.x + player.width, player.y + player.height/2, player.facing))
            else:
                player.bullets.append(
                    Bullet(player.x, player.y + player.height/2, player.facing))

    n = 0
    while n < len(player.bullets):
        player.bullets[n].move()
        player.bullets[n].display(display, scroll)
        if collide_test(player.bullets[n].rect(), map.tiles):
            player.bullets.pop(n)
        elif player.bullets[n].x - scroll[0] < 0 or player.bullets[n].y - scroll[1] < 0 or player.bullets[n].x - scroll[0] > 600 or player.bullets[n].y - scroll[1] > 400:
            player.bullets.pop(n)
        else:
            n += 1

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
            player.x_vel -= 0.2
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

    health_bar.move(player.x, player.y)

    for tile in larva:
        player_rect = player.obj.rect.copy()
        player_rect.y += 2
        if tile.colliderect(player_rect):
            player.health -= 0.01
            if player.movement[0] > 0:
                player.movement[0] *= 0.5
            if player.movement[0] < 0:
                player.movement[0] *= 0.05
            player.movement[1] = 0
            break

    if shake > 0:
        shake -= 1
        scroll[0] += random.randint(-4, 4)
        scroll[1] += random.randint(-4, 4)

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
    i = 0
    while i < len(enemies):
        enemies[i].movement = [0, 0]
        enemies[i].gravity += 0.2
        if enemies[i].air_time < 0:
            enemies[i].air_time = 0
        if enemies[i].gravity > 8:
            enemies[i].gravity = 8
        if abs(player.x - enemies[i].x) < 200 and abs(player.y - enemies[i].y) < 200:
            if player.x - (enemies[i].x+15) > 0:
                enemies[i].movement[0] = 1
            elif (player.x+15) - enemies[i].x < 0:
                enemies[i].movement[0] = -1
            else:
                enemies[i].movement[0] = 0

        if enemies[i].rect().colliderect(player.rect()):
            player.health -= 0.01
        enemies[i].movement[1] = enemies[i].gravity
        enemies[i].air_time += 1
        collisions = enemies[i].move(map.tiles)
        if collisions["right"] or collisions["left"]:
            if enemies[i].air_time < 20:
                enemies[i].gravity = -3
                enemies[i].air_time = 30
        if collisions["bottom"]:
            enemies[i].air_time = 0
        if enemies[i].movement[0] > 0:
            enemies[i].flip = False
            enemies[i].set_action("run")
        elif enemies[i].movement[0] < 0:
            enemies[i].set_action("run")
            enemies[i].flip = True
        else:
            enemies[i].set_action("idle")

        enemies[i].display(display, scroll)
        enemies[i].health_bar.move(enemies[i].x, enemies[i].y)
        enemies[i].health_bar.display(display, scroll)
        for bullet in player.bullets:
            if enemies[i].rect().colliderect(bullet.rect()):
                enemies[i].health -= 2
                enemies[i].health_bar.percent -= 0.5
        if enemies[i].health <= 0:
            enemies.pop(i)
            player.score += 100
        else:
            i += 1

    mx, my = pygame.mouse.get_pos()

    for i in range(20):
        particles.append([[mx, my + random.uniform(0, 5.5)], 0, 255])

    health_bar.display(display, scroll)
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
    pygame.display.update()
    clock.tick(60)

with open('data/info.json', 'r+') as f:
    data = json.load(f)
    data["score"] = player.score
    data["position"] = [player.x, player.y]
    f.seek(0)
    json.dump(data, f, indent=4)

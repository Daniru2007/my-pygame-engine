import json
import pygame

from .physics import PhysicsObject


class Entity(object):
    def __init__(self, x, y, width, height, e_type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.obj = PhysicsObject(self.x, self.y, self.width, self.height)
        self.type = e_type
        self.image = None
        self.flip = False
        self.movement = [0, 0]
        self.gravity = 0
        self.rotation = 0
        self.action = 'idle'
        self.animation = None
        self.animation_frame = 0
        self.animation_tags = {}
        self.animation_database = {}
        self.x_vel = 0
        self.vel = 3
        self.right = [False, False]
        self.left = [False, False]
        self.air_time = 0
        self.lose = False
        self.health = 10

    def set_action(self, action):
        self.action = action
        self.animation_frame = 0

    def load_animations(self, path):
        animation = json.load(open(path))
        for name, action in animation.items():
            path = action["path"]
            data = action["data"]
            for item in range(len(data)):
                action_id = f"{name}_{item+1}"
                path = f"{path}/{action_id}.png"
                self.animation_tags[action_id] = pygame.image.load(path)
                action_set = []
                for _ in range(data[item]):
                    action_set.append(action_id)
                self.animation_database[name] = action_set

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, tiles):
        collisions = self.obj.move(self.movement, tiles)
        self.x = self.obj.x
        self.y = self.obj.y
        return collisions

    def set_image(self, image):
        self.image = image

    def display(self, display, scroll):
        image = pygame.transform.flip(self.animation_tags[self.animation_database[self.action][self.animation_frame]], self.flip, False)
        display.blit(image, (self.x - scroll[0], self.y - scroll[1]))

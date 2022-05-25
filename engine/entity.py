import pygame

from engine.physics import collide_test, PhysicsObject


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
        self.animation_tags = []
        self.x_vel = 0
        self.vel = 3
        self.right = [False, False]
        self.up = False
        self.left = [False, False]
        self.down = False

    def set_action(self, action):
        self.action = action

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, tiles):
        self.x += self.movement[0]
        self.y += self.movement[1]

    def set_image(self, image):
        self.image = image

    def display(self, display, scroll):
        display.blit(self.image, (self.x - scroll[0], self.y - scroll[1]))

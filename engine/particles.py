import pygame
import random


class Particles(object):
    def __init__(self, x, y, radius, color, count):
        self.x = x
        self.y = y
        self.color = color
        self.count = count
        self.radius = radius
        self.particles = []

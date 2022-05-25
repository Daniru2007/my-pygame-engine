import pygame


def collide_test(rect, tiles):
    hit_boxes = []
    for tile in tiles:
        if rect.colliderect(tile[1]):
            hit_boxes.append(tile[1])
    return hit_boxes


class PhysicsObject(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, movement, tiles):
        pass

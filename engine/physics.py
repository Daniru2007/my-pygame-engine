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
        collisions = {
            "right": False, "left": False,
            "top": False, "bottom": False
        }
        self.x += movement[0]
        self.rect.x += movement[0]
        hit_boxes = collide_test(self.rect, tiles)
        for tile in hit_boxes:
            if movement[0] > 0:
                self.rect.right = tile.left
                collisions["right"] = True
            if movement[0] < 0:
                self.rect.left = tile.right
                collisions["left"] = True
        self.x = self.rect.x

        self.y += movement[1]
        self.rect.y += movement[1]
        hit_boxes = collide_test(self.rect, tiles)
        for tile in hit_boxes:
            if movement[1] < 0:
                self.rect.top = tile.bottom
                collisions["top"] = True
            if movement[1] > 0:
                self.rect.bottom = tile.top
                collisions["bottom"] = True
        self.y = self.rect.y

        return collisions

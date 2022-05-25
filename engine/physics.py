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
        collision_types = {
            "right": False, "left": False,
            "top": False, "bottom": False
        }
        self.x += movement[0]
        self.rect.x += movement[0]
        hit_boxes = collide_test(self.rect, tiles)
        for tile in hit_boxes:
            if movement[0] > 0:
                self.rect.right = tile.left
                collision_types["right"] = True
            if movement[0] < 0:
                self.rect.left = tile.right
            self.x = self.rect.x

        self.y += movement[1]
        self.rect.y += movement[1]
        hit_boxes = collide_test(self.rect, tiles)
        for tile in hit_boxes:
            if movement[1] < 0:
                self.rect.top = tile.bottom
                collision_types["up"] = True
            if movement[1] > 0:
                self.rect.bottom = tile.top
                collision_types["bottom"] = True
            self.y = self.rect.y

        return collision_types

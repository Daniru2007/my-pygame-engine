import pygame


def collide_test(rect, tiles):
    hit_boxes = []
    for tile in tiles:
        if rect.colliderect(tile[1]):
            hit_boxes.append(tile[1])
    return hit_boxes

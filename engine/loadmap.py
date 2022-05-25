import pygame
import json


class Map(object):
    def __init__(self, tiles_path, maps_path):
        self.tiles_path = tiles_path
        self.map_file = json.load(f"{maps_path}/map.json")
        self.map = self.map_file["layers"][0]["data"]
        self.width = self.map_file["layers"][0]["width"]
        self.height = self.map_file["layers"][0]["height"]
        self.tile_height = self.map_file["tileheight"]
        self.tile_width = self.map_file["tilewidth"]
        self.database = {}
        for tile in self.map_file["tilesets"]:
            index = tile["firstgid"]
            tile_file = json.load(tile["source"])
            tile_image = tile_file["image"].split("/")[-1]
            tile = pygame.image.load(f"{tiles_path}/{tile_image}")
            self.database[index] = tile
        self.tile_rects = []
        for y in range(self.height):
            for x in range(self.width):
                if not self.map[x + y*self.width]:
                    self.tile_rects.append([self.map[x + y*self.width], pygame.Rect(
                        x * self.tile_width, y * self.height, self.tile_width, self.tile_height)])

    def display(self, display, scroll):
        for tile in self.tile_rects:
            display.blit(self.database[tile[0]], (tile[1].x - scroll[0], tile[1].y - scroll[1]))

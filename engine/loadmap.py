import pygame
import json


class Map(object):
    def __init__(self, tiles_path, maps_path):
        self.tiles_path = tiles_path
        self.map_file = json.load(open(f"{maps_path}/map.json"))
        self.map = self.map_file["layers"][0]["data"]
        self.width = self.map_file["layers"][0]["width"]
        self.height = self.map_file["layers"][0]["height"]
        self.tile_height = self.map_file["tileheight"]
        self.tile_width = self.map_file["tilewidth"]
        self.act_height = self.height * self.tile_height
        self.act_width = self.width * self.tile_width
        self.database = {}
        for tile in self.map_file["tilesets"]:
            index = tile["firstgid"]
            tile_file = json.load(open(f"{maps_path}/{tile['source']}"))
            tile_image = tile_file["image"].split("/")[-1]
            tile = pygame.image.load(f"{tiles_path}/{tile_image}")
            self.database[index] = tile
        self.tiles = []
        self.coins = []
        self.jumpers = []
        self.larva = []
        self.health_tanks = []
        for y in range(self.height):
            for x in range(self.width):
                if self.map[x + y*self.width] == 3:
                    self.coins.append(pygame.Rect(x * self.tile_width, y * self.tile_height, self.tile_width, self.tile_height))
                    continue
                if self.map[x + y*self.width] == 4:
                    self.jumpers.append(pygame.Rect(x * self.tile_width, y * self.tile_height, self.tile_width, self.tile_height))
                    continue
                if self.map[x + y*self.width] == 6:
                    self.health_tanks.append(pygame.Rect(x * self.tile_width, y * self.tile_height, self.tile_width, self.tile_height))
                    continue
                if self.map[x + y*self.width] == 5:
                    self.larva.append(pygame.Rect(x * self.tile_width, y * self.tile_height, self.tile_width, self.tile_height))

                if self.map[x + y*self.width]:
                    self.tiles.append([self.map[x + y*self.width], pygame.Rect(
                        x * self.tile_width, y * self.tile_height, self.tile_width, self.tile_height)])

    def display(self, display, scroll):
        for tile in self.tiles:
            display.blit(self.database[tile[0]], (tile[1].x - scroll[0], tile[1].y - scroll[1]))

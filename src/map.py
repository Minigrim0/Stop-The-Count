import json

import pygame


class Map(object):
    def __init__(self, mapFile):
        map_info = json.load(open(mapFile, "r"))
        self.image = pygame.image.load(map_info["img"]).convert_alpha()

    def draw(self, screen, position):
        screen.blit(self.image, position)

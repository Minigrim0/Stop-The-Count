import json

import pygame


class Map(object):
    def __init__(self, mapFile):
        map_info = json.load(open(mapFile, "r"))
        self.image = pygame.image.load(map_info["img"]).convert_alpha()
        self.size = self.image.get_size()
        self.absolute_position = [0, 0]

    def draw(self, screen, player):
        position = [player.get_map_position(), 0]

        screen.blit(self.image, position)

        if position[0] + self.size[0] < 0:
            player.map_pos = position[0] + self.size[0]
        elif self.size[0] - abs(position[0]) < screen.nativeSize[0]:
            screen.blit(self.image, (self.size[0] - abs(position[0]), position[1]))

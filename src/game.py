import json

from src.map import Map
from src.player import Player
import pygame


class Game(object):
    def __init__(self, saveFile=None):
        self.isRunning = False
        if saveFile is None:
            self.map = Map("assets/maps/default.json")
            self.player = Player()
        else:
            self.load(saveFile)

    def load(self, saveFile):
        """
        Loads the game from a save file, creates an empty game if the save is None
        """
        save = json.load(open(saveFile, "r"))
        self.map = Map(save['map'])
        self.player = Player(save['player'])

    def update(self, screen):
        for event in screen.events():
            if event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_ESCAPE:
                    print("oui")

        self.player.update(screen)

    def draw(self, screen):
        self.map.draw(screen, (self.player.get_map_position(), 0))
        self.player.draw(screen)

        screen.flip()

    def run(self, screen):
        self.isRunning = True
        while self.isRunning:
            self.update(screen)
            self.draw(screen)

class PauseMenu(object):
    def __init__(self):
        self.hi = ""

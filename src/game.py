import json

from src.map import Map
from src.player import Player


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
        pass

    def draw(self, screen):
        self.map.draw(screen, (0, 0))

    def run(self, screen):
        while self.isRunning:
            self.update()
            self.draw()

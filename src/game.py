import json
import time
import random

from src.map import Map
from src.player import Player
import pygame
from src.ennemy import Ennemy


class Game(object):
    def __init__(self, saveFile=None):
        self.isRunning = False
        if saveFile is None:
            self.map = Map("assets/maps/default.json")
            self.player = Player()
        else:
            self.load(saveFile)

        self.ennemyController = EnnemyController(5)

    def load(self, saveFile):
        """
        Loads the game from a save file, creates an empty game if the save is None
        """
        save = json.load(open(saveFile, "r"))
        self.map = Map(save['map'])
        self.player = Player(save['player'])

    def update(self, screen):
        for event in screen.events():
            action = self.player.eventUpdate(event)
            if action == "HIT":
                self.ennemyController.hit(self.player.hitbox, self.player.damage)

            if event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_ESCAPE:
                    print("oui")

        self.player.update(screen)
        self.ennemyController.update(screen)

    def draw(self, screen):
        self.map.draw(screen, self.player)
        self.ennemyController.draw(screen)
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


class EnnemyController(object):
    def __init__(self, difficulty):
        """Initialize an ennemy controller

        Args:
            difficulty (Int): The difficulty of the game (between 1 and 5)
        """
        self.ennemies = []
        self.minTimeBetweenEnnemySpawn = 5 - difficulty  # seconds
        self.timeAtLastEnnemySpawn = 0
        self.timeAtLastEnnemySpawnAttempt = 0
        self.ennemySpawnChance = 10 * difficulty  # Ten percent chance of spawning each second

    def update(self, screen):
        for ennemy in self.ennemies:
            ennemy.update(screen)

        if time.time() - self.timeAtLastEnnemySpawn > self.minTimeBetweenEnnemySpawn:
            if time.time() - self.timeAtLastEnnemySpawnAttempt > 1:
                self.timeAtLastEnnemySpawnAttempt = time.time()
                if random.randint(0, 100) < self.ennemySpawnChance:
                    self.ennemies.append(Ennemy())
                    self.timeAtLastEnnemySpawn = time.time()

    def draw(self, screen):
        for ennemy in self.ennemies:
            ennemy.draw(screen)

    def hit(self, hitbox, damage):
        for ennemy in self.ennemies[:]:
            if ennemy.hurtbox.colliderect(hitbox):
                result = ennemy.hit(damage)
                if result == "DEAD":
                    del self.ennemies[self.ennemies.index(ennemy)]

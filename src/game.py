import json
import time
import random

from src.map import Map
from src.player import Player
import pygame
from src.ennemy import Ennemy
from src.menu import Menu, Button


class Game(object):
    def __init__(self, screen, saveFile=None):
        self.isRunning = False
        if saveFile is None:
            self.map = Map("assets/maps/default.json")
            self.player = Player()
        else:
            self.load(saveFile)
        self.openMenu = "[Esc] Open Menu"
        self.openMenu = screen.fonts["25"].render(self.openMenu, 1, (255, 255, 255))
        self.closeMenu = "[Esc] Close Menu"
        self.closeMenu = screen.fonts["25"].render(self.closeMenu, 1, (255, 255, 255))
        self.ennemyController = EnnemyController(0)
        button_help = Button((700, 300), (300, 60), "How to Build Walls", exit)
        button_help.build(screen)
        button_save = Button((1100, 300), (300, 60), "Save", exit)
        button_save.build(screen)
        button_quit = Button((1500, 300), (300, 60), "Quit", self.stop)
        button_quit.build(screen)
        self.pauseMenu = Menu(None, [button_help, button_save, button_quit], True)

        button_resume = Button((300, 300), (300, 60), "Resume", self.pauseMenu.stop)
        button_resume.build(screen)
        self.pauseMenu.buttons.append(button_resume)
        

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
                    self.pauseMenu.run(screen, self)

        self.player.update(screen)
        self.ennemyController.update(screen)
        

    def draw(self, screen):
        self.map.draw(screen, (self.player.get_map_position(), 0))
        self.ennemyController.draw(screen)
        self.player.draw(screen)
    
    def stop(self):
        self.isRunning = False
        self.pauseMenu.stop()

    def run(self, screen):
        self.isRunning = True
        while self.isRunning:
            self.update(screen)
            self.draw(screen)
            screen.blit(self.openMenu, (10,10))
            screen.flip()


class EnnemyController(object):
    def __init__(self, difficulty):
        self.ennemies = []
        self.minTimeBetweenEnnemySpawn = 5  # seconds
        self.timeAtLastEnnemySpawn = 0
        self.timeAtLastEnnemySpawnAttempt = 0
        self.ennemySpawnChance = 10  # Ten percent chance of spawning each second

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

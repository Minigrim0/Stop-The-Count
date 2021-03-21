import json
import time
import random

from src.map import Map
from src.player import Player
import pygame
from src.ennemy import Ennemy
from src.menu import Menu, Button
from src.ballot import Ballot
import src.constants as cst
import datetime
from src.wall import Wall


class Game(object):
    def __init__(self, screen, tutorialMenu, saveFile=None):
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
        self.ennemyController = EnnemyController(5)
        button_help = Button((700, 300), (300, 60), "How to Build Walls", tutorialMenu.run, screen=screen)
        button_help.build(screen)
        button_save = Button((1100, 300), (300, 60), "Save", exit)
        button_save.build(screen)
        button_quit = Button((1500, 300), (300, 60), "Quit", self.stop)
        button_quit.build(screen)
        self.pauseMenu = Menu(None, [button_help, button_save, button_quit], True)

        
        
        self.winMenu = Menu(pygame.image.load("assets/img/youWon.jpg"), [], True)
        button_continue = Button((10, 1000), (300, 60), "4 Years Later >>", self.winMenu.stop)
        button_continue.build(screen)
        self.winMenu.buttons.append(button_continue)

        button_quit = Button((10, 1000), (300, 60), "Quit Because I'm Bad", exit)
        button_quit.build(screen)
        self.loseMenu = Menu(pygame.image.load("assets/img/youLose.jpg"), [button_quit], True)
        button_continue = Button((400, 1000), (300, 60), "Continue & Sue Bedin", self.loseMenu.stop)
        button_continue.build(screen)
        self.loseMenu.buttons.append(button_continue)

        self.invocations = []

        button_resume = Button((300, 300), (300, 60), "Resume", self.pauseMenu.stop)
        button_resume.build(screen)
        self.pauseMenu.buttons.append(button_resume)
        self.gameEndTime = cst.GAME_TIME
        

        self.ballots = {
            "republican": Ballot((1800, 20), "assets/img/republican.png"),
            "democrat": Ballot((1800, 140), "assets/img/democrat.png"),
        }

    def load(self, saveFile):
        """
        Loads the game from a save file, creates an empty game if the save is None
        """
        save = json.load(open(saveFile, "r"))
        self.map = Map(save['map'])
        self.player = Player(save['player'])

    def update(self, screen):
        self.gameEndTime = int(self.gameEndTime - screen.timeElapsed)
        if self.gameEndTime <= 0:
            if self.ballots["republican"].votes <= self.ballots["democrat"].votes:
                self.winMenu.run(screen)
            else:
                self.loseMenu.run(screen)
            self.stop()
        for event in screen.events():
            action = self.player.eventUpdate(event)
            if action == "HIT":
                self.ennemyController.hit(self.player.hitbox, self.player.damage)
            elif action == "BUILDWALL":
                self.invocations.append(
                    Wall(
                        [
                            self.player.position[0] + 205,
                            self.player.position[1]
                        ]
                    )
                )

            if event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_ESCAPE:
                    self.pauseMenu.run(screen, self)

        for inv in self.invocations[:]:
            result = inv.update(self.ennemyController)
            if result == "DEAD":
                del self.invocations[self.invocations.index(inv)]

        self.player.update(screen, self.ennemyController, self.invocations)

        deaths, democrat_votes = self.ennemyController.update(screen)
        self.player.addSpecialAttack(deaths * 5)

        for key, ballot in self.ballots.items():
            if key == "democrat":
                ballot.add_votes(democrat_votes)
            ballot.update(screen)

    def draw(self, screen):
        self.map.draw(screen, self.player)
        self.ennemyController.draw(screen)
        for inv in self.invocations:
            inv.draw(screen)

        self.player.draw(screen)

        for key, ballot in self.ballots.items():
            ballot.draw(screen)

    def stop(self):
        self.isRunning = False
        self.pauseMenu.stop()

    def getTimeDisplay(self):
        return str(datetime.timedelta(seconds=self.gameEndTime))

    def run(self, screen):
        self.isRunning = True
        while self.isRunning:
            self.update(screen)
            self.draw(screen)
            screen.blit(self.openMenu, (10, 10))
            self.gameEndTimeDisplay = screen.fonts["75"].render(self.getTimeDisplay(), 0, (255, 255, 255))
            screen.blit(self.gameEndTimeDisplay, (10, 30))
            screen.flip()


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
        if time.time() - self.timeAtLastEnnemySpawn > self.minTimeBetweenEnnemySpawn:
            if time.time() - self.timeAtLastEnnemySpawnAttempt > 1:
                self.timeAtLastEnnemySpawnAttempt = time.time()
                if random.randint(0, 100) < self.ennemySpawnChance:
                    self.ennemies.append(Ennemy())
                    self.timeAtLastEnnemySpawn = time.time()

        results = [0, 0]  # 0 deaths, 0 votes to add
        for ennemy in self.ennemies:
            result = ennemy.update(screen)
            if result == "DEAD":
                del self.ennemies[self.ennemies.index(ennemy)]
                results[0] += 1
            elif result == "ADDVOTE":
                del self.ennemies[self.ennemies.index(ennemy)]
                results[1] += 1

        return results

    def draw(self, screen):
        for ennemy in self.ennemies:
            ennemy.draw(screen)

    def hit(self, hitbox, damage):
        for ennemy in self.ennemies[:]:
            if ennemy.hurtbox.colliderect(hitbox):
                ennemy.hit(damage)
                ennemy.velAngle = 120

    def move(self, delta):
        for ennemy in self.ennemies:
            ennemy.position[0] -= delta

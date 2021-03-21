import random
import math
import glob
import time
import os

import pygame

from src.healthbar import HealthBar
import src.constants as cst


class Ennemy(object):
    def __init__(self):
        self.images = {}
        for filename in glob.glob("assets/img/ennemy/*.png"):
            dirname, file = os.path.split(filename)
            file, ext = os.path.splitext(file)
            animation, index = file.split("_")
            if animation not in self.images.keys():
                self.images[animation] = [
                    pygame.image.load(filename).convert_alpha()
                ]
            else:
                self.images[animation].append(pygame.image.load(filename).convert_alpha())

        self.timeAtLastAttack = 0

        self.image = pygame.image.load("assets/img/player/animation/idle_1.png").convert_alpha()
        self.speed = random.randrange(200, 420)
        self.position = [1920, random.randrange(500 - self.image.get_size()[1], 1080 - self.image.get_size()[1])]
        self.healthBar = HealthBar(100)
        self.health = 100
        self.velAngle = 270  # degrees (Not a mathematician here)
        self.velocity = [-1, 0]

        self.animstate = 0

    @property
    def can_attack(self):
        return (time.time() - self.timeAtLastAttack) * 1000 >= cst.ENNEMY_ATTACK_COOLDOWN

    def attack(self):
        self.timeAtLastAttack = time.time()

    def update(self, screen):
        if self.velAngle < 270:
            self.velocity[0] = math.sin(self.velAngle * math.pi / 180)
            self.velAngle += 90 * screen.timeElapsed
        self.position[0] += self.speed * self.velocity[0] * screen.timeElapsed
        self.animstate += screen.timeElapsed * 10
        if self.animstate > len(self.images["walk"]):
            self.animstate = 0

        if self.health < 0:
            return "DEAD"
        if self.position[0] < 0:
            return "DEMOCRAT_ADDVOTE"

    def hit(self, damage):
        self.health -= damage
        if self.health > 0:
            self.healthBar.update(self.health)

    def collide(self, event):
        if event.pos[0] > self.position[0] > self.pos[0] + self.image.get_size()[0]:
            if event.pos[1] > self.position[1] > self.pos[1] + self.image.get_size()[1]:
                return True
        return False

    def draw(self, screen):
        screen.blit(self.images["walk"][min(round(self.animstate), len(self.images["walk"])-1)], self.position)
        self.healthBar.draw(
            screen,
            (
                self.position[0] + (
                    (self.image.get_size()[0] - self.healthBar.size[0]) // 2
                ),
                self.position[1] - 10
            )
        )

    @property
    def hurtbox(self):
        return pygame.Rect((self.position[0] + cst.HURTBOX_RELATIVE[0], self.position[1]), cst.HURTBOX_RELATIVE[2:])

    @property
    def collisionbox(self):
        return pygame.Rect(
            (self.position[0] + cst.COLLISION_RELATIVE[0], self.position[1]), cst.COLLISION_RELATIVE[2:])

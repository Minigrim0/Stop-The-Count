import random

import pygame

from src.healthbar import HealthBar
import src.constants as cst


class Ennemy(object):
    def __init__(self):
        self.image = pygame.image.load("assets/img/player/player_idle_1.png").convert_alpha()
        self.speed = random.randrange(200, 420)
        self.position = [1920, random.randrange(500 - self.image.get_size()[1], 1080 - self.image.get_size()[1])]
        self.healthBar = HealthBar(100)
        self.health = 100
        self.velocity = [-1, 0]

    def update(self, screen):
        self.position[0] += self.speed * self.velocity[0] * screen.timeElapsed

    def hit(self, damage):
        self.health -= damage
        if self.health < 0:
            return "DEAD"
        self.healthBar.update(self.health)

    def collide(self, event):
        if event.pos[0] > self.position[0] > self.pos[0] + self.image.get_size()[0]:
            if event.pos[1] > self.position[1] > self.pos[1] + self.image.get_size()[1]:
                return True
        return False

    def draw(self, screen):
        screen.blit(self.image, self.position)
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

import random

import pygame


class Ennemy(object):
    def __init__(self):
        self.image = pygame.image.load("assets/img/player/trump_face2.png").convert_alpha()
        self.speed = random.randrange(200, 420)
        self.position = [1920, random.randrange(500 - self.image.get_size()[1], 1080 - self.image.get_size()[1])]

    def update(self, screen):
        self.position[0] -= self.speed * screen.timeElapsed

    def draw(self, screen):
        screen.blit(self.image, self.position)

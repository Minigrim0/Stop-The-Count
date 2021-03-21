import pygame
import random


class Twat(object):
    def __init__(self, screen, position):
        self.image = pygame.image.load("assets/img/twat.png").convert_alpha()
        self.lifetime = 10
        self.rt = random.randrange(100)
        self.rt_img = screen.fonts["50"].render(str(self.rt), 1, (255, 0, 0))
        self.position = position

    def update(self, screen):
        self.lifetime -= screen.timeElapsed
        if self.lifetime < 0:
            return "DEAD"

    def draw(self, screen):
        screen.blit(self.image, self.position)
        screen.blit(self.rt_img, (self.position[0] + 300, self.position[1] + 75))

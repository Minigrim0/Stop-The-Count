import pygame


class HealthBar(object):
    def __init__(self, max_health=100, size=(250, 10)):
        self.maxHealth = max_health
        self.currentHealth = max_health
        self.size = size

        self.back = pygame.Surface(size)
        self.front = pygame.Surface(size)
        self.back.fill((255, 0, 0))
        self.front.fill((0, 255, 0))

    def update(self, health):
        self.currentHealth = health
        length = self.currentHealth / self.maxHealth * self.size[0]

        self.front = pygame.Surface((length, self.size[1]))
        self.front.fill((0, 255, 0))

    def draw(self, screen, position):
        screen.blit(self.back, position)
        screen.blit(self.front, position)

import pygame

from src.healthbar import HealthBar


class Wall(object):
    def __init__(self, position):
        self.image = pygame.image.load("assets/img/wall.png")
        self.collisionbox = pygame.Rect(position, self.image.get_size())
        self.health = 100
        self.healthbar = HealthBar()
        self.position = position

    def draw(self, screen):
        screen.blit(self.image, self.position)
        self.healthbar.draw(
            screen,
            (
                self.position[0] + (
                    (self.image.get_size()[0] - self.healthbar.size[0]) // 2
                ),
                self.position[1] - 10
            )
        )

    def move(self, delta):
        self.position[0] += delta
        self.collisionbox = pygame.Rect(self.position, self.image.get_size())

    def update(self, ennemyController):
        for ennemy in ennemyController.ennemies:
            self.collide(ennemy)

        if self.health > 0:
            self.healthbar.update(self.health)
        else:
            return "DEAD"

    def collide(self, ennemy):
        if ennemy.collisionbox and ennemy.collisionbox.colliderect(self.collisionbox):
            if ennemy.can_attack:
                ennemy.attack()
                self.health -= 1
            ennemy.velAngle = 120

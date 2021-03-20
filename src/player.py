import pygame

import src.constants as cst


class Player(object):
    def __init__(self):
        self.images = []
        self.position = [0, 600]
        self.image = pygame.image.load("assets/img/player/player_idle_1.png").convert_alpha()
        self.velocity = [0, 0]
        self.speed = 400

        self.status = cst.IDLE
        self.damage = 30

        self.map_pos = 0

    def draw(self, screen):
        screen.blit(self.image, self.position)

    def get_map_position(self):
        return self.map_pos

    def update(self, screen):
        if pygame.key.get_pressed()[pygame.locals.K_UP]:
            self.velocity[1] = -1
            if self.position[1] < screen.nativeSize[1] - 490 - self.image.get_size()[1]:
                self.velocity[1] = 0
        if pygame.key.get_pressed()[pygame.locals.K_DOWN]:
            self.velocity[1] = 1
            if self.position[1] > screen.nativeSize[1] - self.image.get_size()[1]:
                self.velocity[1] = 0
        if pygame.key.get_pressed()[pygame.locals.K_LEFT]:
            self.velocity[0] = -1
            if self.position[0] < 20:
                self.velocity[0] = 0
        if pygame.key.get_pressed()[pygame.locals.K_RIGHT]:
            self.velocity[0] = 1

        self.move(screen.timeElapsed)

    def move(self, timeElapsed):
        if self.position[0] < 500:
            self.position[0] += self.speed * self.velocity[0] * timeElapsed
        elif self.velocity[0] < 0:
            self.position[0] += self.speed * self.velocity[0] * timeElapsed
        else:
            self.map_pos -= self.speed * self.velocity[0] * timeElapsed

        self.position[1] += self.speed * self.velocity[1] * timeElapsed

        self.velocity[0] -= self.velocity[0] * 0.1
        self.velocity[1] -= self.velocity[1] * 0.1

    def eventUpdate(self, event):
        if event.type == pygame.locals.KEYDOWN:
            if event.key == pygame.locals.K_SPACE:
                self.status = cst.ATTACK
                print("HIT ME")
                return "HIT"

    @property
    def hitbox(self):
        return pygame.Rect((self.position[0] + cst.HITBOX_RELATIVE[0], self.position[1]), cst.HITBOX_RELATIVE[2:])

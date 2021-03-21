import os
import glob
import random

import pygame

import src.constants as cst


class Player(object):
    def __init__(self):
        self.images = []
        self.position = [0, 600]
        self.images = {}
        for filename in glob.glob("assets/img/player/animation/*.png"):
            dirname, file = os.path.split(filename)
            file, ext = os.path.splitext(file)
            animation, index = file.split("_")
            if animation not in self.images.keys():
                self.images[animation] = [
                    pygame.image.load(filename).convert_alpha()
                ]
            else:
                self.images[animation].append(pygame.image.load(filename).convert_alpha())

        self.sounds = {}
        for filename in glob.glob("assets/sound/player/*.wav"):
            dirname, file = os.path.split(filename)
            file, ext = os.path.splitext(file)
            sound, index = file.split("_")
            if sound not in self.sounds.keys():
                newSound = pygame.mixer.Sound(filename)
                newSound.set_volume(0.5)
                self.sounds[sound] = [newSound]
            else:
                newSound = pygame.mixer.Sound(filename)
                newSound.set_volume(0.5)
                self.sounds[sound].append(newSound)

        self.size = (205, 415)
        self.velocity = [0, 0]
        self.speed = 400

        self.attackCooldown = 0

        self.status = cst.IDLE
        self.damage = 30

        self.map_pos = 0

    def draw(self, screen):
        if self.status == cst.IDLE:
            screen.blit(self.images["idle"][0], self.position)
        elif self.status == cst.ATTACK:
            screen.blit(self.images["attack"][0], self.position)

    def get_map_position(self):
        return self.map_pos

    def update(self, screen):
        if pygame.key.get_pressed()[pygame.locals.K_UP]:
            self.velocity[1] = -1
            if self.position[1] < screen.nativeSize[1] - 490 - self.size[1]:
                self.velocity[1] = 0
        if pygame.key.get_pressed()[pygame.locals.K_DOWN]:
            self.velocity[1] = 1
            if self.position[1] > screen.nativeSize[1] - self.size[1]:
                self.velocity[1] = 0
        if pygame.key.get_pressed()[pygame.locals.K_LEFT]:
            self.velocity[0] = -1
            if self.position[0] < 20:
                self.velocity[0] = 0
        if pygame.key.get_pressed()[pygame.locals.K_RIGHT]:
            self.velocity[0] = 1

        self.move(screen.timeElapsed)

        if self.attackCooldown > 0:
            self.attackCooldown -= screen.timeElapsed
            if self.attackCooldown <= 0:
                self.status = cst.IDLE

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
            if event.key == pygame.locals.K_SPACE and self.attackCooldown <= 0:
                self.status = cst.ATTACK
                self.attackCooldown = cst.ATTACK_COOLDOWN / 1000
                pygame.mixer.Sound.play(random.choice(self.sounds["attack"]))
                return "HIT"

    @property
    def hitbox(self):
        return pygame.Rect((self.position[0] + cst.HITBOX_RELATIVE[0], self.position[1]), cst.HITBOX_RELATIVE[2:])

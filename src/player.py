import os
import glob
import random

import pygame

import src.constants as cst


class Player(object):
    def __init__(self):
        self.images = []
        self.position = [0, 600]
        self.absolute_x = 0
        self.images = {}

        for filename in sorted(glob.glob("assets/img/player/animation/*.png")):
            dirname, file = os.path.split(filename)
            file, ext = os.path.splitext(file)
            animation, index = file.split("_")
            if animation not in self.images.keys():
                self.images[animation] = [
                    pygame.image.load(filename).convert_alpha()
                ]
            else:
                self.images[animation].append(pygame.image.load(filename).convert_alpha())

        self.expressions = {}
        for filename in glob.glob("assets/img/player/expressions/*.png"):
            dirname, file = os.path.split(filename)
            file, ext = os.path.splitext(file)
            self.expressions[file] = pygame.image.load(filename).convert_alpha()

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

        self.wall_building_sound = pygame.mixer.Sound("assets/sound/build a wall.wav")
        self.wall_building_sound.set_volume(0.5)

        self.size = (205, 415)
        self.velocity = [0, 0]
        self.speed = 500

        self.attackCooldown = 0
        self.walkCooldown = 0
        self.whichFoot = 0

        self.specialAttack = 0
        self.specialAttackBarBack = pygame.Surface((10, 200))
        self.specialAttackBarBack.fill((50, 50, 50))
        self.specialAttackBar = pygame.Surface((10, 200))

        self.popularity = 50  # Keep it above 50
        self.popularityBarBack = pygame.Surface((1500, 25))
        self.popularityText = pygame.Surface((25, 20))
        self.popularityBarBack.fill((0, 0, 255))
        self.popularityBar = pygame.Surface((round(1500 * self.popularity / 100), 25))
        self.popularityBar.fill((255, 0, 0))

        self.status = cst.IDLE
        self.damage = 30
        self.attackType = 0

        self.map_pos = 0

    def draw(self, screen):
        if self.status == cst.IDLE:
            screen.blit(self.images["idle"][0], self.position)
            screen.blit(self.expressions["meh"], self.position)
        elif self.status == cst.ATTACK:
            screen.blit(self.images["attack"][self.attackType], self.position)
            screen.blit(self.expressions["angry"], self.position)
        elif self.status == cst.WALK:
            screen.blit(self.images["walk"][self.whichFoot], self.position)
            screen.blit(self.expressions["happy"], self.position)

        self.drawUI(screen)

    def get_map_position(self):
        return self.map_pos

    def updateAttackBar(self):
        self.specialAttackBar = pygame.Surface((10, round((self.specialAttack / cst.SPECIAL_ATTACK_COST) * 200)))
        self.specialAttackBar.fill((255, 0, 255))

    def updatePopularity(self, screen):
        self.popularityBar = pygame.Surface((round(1500 * self.popularity / 100), 25))
        self.popularityBar.fill((255, 0, 0))

        self.popularityText = screen.fonts["25"].render(f"Popularity : {round(self.popularity, 2)}%", 0, (255, 255, 255))

    def drawUI(self, screen):
        screen.blit(self.popularityBarBack, (210, 1000))
        screen.blit(self.popularityBar, (210, 1000))
        screen.blit(self.popularityText, ((1920 - self.popularityText.get_size()[0]) // 2, 1000))

        screen.blit(self.specialAttackBarBack, (self.position[0] - 10, self.position[1] + ((self.size[1] - 200) // 2)))
        if self.attackCooldown < cst.SPECIAL_ATTACK_COST:
            screen.blit(
                self.specialAttackBar,
                (
                    self.position[0] - 10,
                    self.position[1] + (
                        200 - (
                            self.specialAttack / cst.SPECIAL_ATTACK_COST) * 200
                        ) + (
                            (self.size[1] - 200) // 2)
                )
            )
        else:
            screen.blit(self.specialAttackBar, (self.position[0] - 10, self.position[1] + ((self.size[1] - 200) // 2)))

    def update(self, screen, ennemyController, invocations):
        if self.walkCooldown <= 0:
            if pygame.key.get_pressed()[pygame.locals.K_UP]:
                self.velocity[1] = -1
                self.status = cst.WALK
                self.walkCooldown = cst.WALK_COOLDOWN / 1000
                if self.position[1] < screen.nativeSize[1] - 490 - self.size[1]:
                    self.velocity[1] = 0
            if pygame.key.get_pressed()[pygame.locals.K_DOWN]:
                self.velocity[1] = 1
                self.status = cst.WALK
                self.walkCooldown = cst.WALK_COOLDOWN / 1000
                if self.position[1] > screen.nativeSize[1] - self.size[1]:
                    self.velocity[1] = 0
            if pygame.key.get_pressed()[pygame.locals.K_LEFT]:
                self.velocity[0] = -1
                self.status = cst.WALK
                self.walkCooldown = cst.WALK_COOLDOWN / 1000
                if self.position[0] < 20:
                    self.velocity[0] = 0
            if pygame.key.get_pressed()[pygame.locals.K_RIGHT]:
                self.status = cst.WALK
                self.walkCooldown = cst.WALK_COOLDOWN / 1000
                self.velocity[0] = 1

        self.move(screen.timeElapsed, ennemyController, invocations)
        if self.specialAttack < cst.SPECIAL_ATTACK_COST:
            self.specialAttack += screen.timeElapsed
            self.updateAttackBar()

        if self.attackCooldown > 0:
            self.attackCooldown -= screen.timeElapsed
            if self.attackCooldown <= 0:
                self.status = cst.IDLE
        elif self.walkCooldown > 0:
            self.walkCooldown -= screen.timeElapsed
            if self.walkCooldown <= 0:
                self.status = cst.IDLE
                self.whichFoot = 1 - self.whichFoot

    def addSpecialAttack(self, value):
        if self.specialAttack < cst.SPECIAL_ATTACK_COST:
            self.specialAttack = min(self.specialAttack + value, cst.SPECIAL_ATTACK_COST)
            self.updateAttackBar()

    def move(self, timeElapsed, ennemyController, invocations):
        if self.position[0] < 500:
            self.position[0] += self.speed * self.velocity[0] * timeElapsed
        elif self.velocity[0] < 0:
            self.position[0] += self.speed * self.velocity[0] * timeElapsed
        else:
            self.map_pos -= self.speed * self.velocity[0] * timeElapsed
            ennemyController.move(self.speed * self.velocity[0] * timeElapsed)
            for invocation in invocations:
                invocation.move(-self.speed * self.velocity[0] * timeElapsed)

        self.position[1] += self.speed * self.velocity[1] * timeElapsed
        self.absolute_x += self.speed * self.velocity[0] * timeElapsed

        self.velocity[0] -= self.velocity[0] * 0.1
        self.velocity[1] -= self.velocity[1] * 0.1

    def eventUpdate(self, event):
        if event.type == pygame.locals.KEYDOWN:
            if event.key in cst.ATTACK_KEYS and self.attackCooldown <= 0:
                if event.key == pygame.locals.K_x:
                    self.attackType = 0
                elif event.key == pygame.locals.K_c:
                    self.attackType = 3
                elif event.key == pygame.locals.K_v:
                    self.attackType = 2
                elif event.key == pygame.locals.K_SPACE:
                    self.attackType = 1
                self.status = cst.ATTACK
                self.attackCooldown = cst.ATTACK_COOLDOWN / 1000
                pygame.mixer.Sound.play(random.choice(self.sounds["attack"]))
                return "HIT"
            elif event.key == pygame.locals.K_RETURN and self.specialAttack >= 25:
                self.specialAttack = 0
                self.updateAttackBar()
                pygame.mixer.Sound.play(self.wall_building_sound)
                return "BUILDWALL"

    @property
    def hitbox(self):
        return pygame.Rect((self.position[0] + cst.HITBOX_RELATIVE[0], self.position[1]), cst.HITBOX_RELATIVE[2:])

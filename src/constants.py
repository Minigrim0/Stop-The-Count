import pygame
IDLE = 0
ATTACK = 1
WALK = 2

HITBOX_RELATIVE = (130, 0, 150, 270)
HITBOX_HIGH_KICK = (130, 0, 150, 270)
HITBOX_LOW_KICK = (130, 250, 150, 150)
HITBOX_KAMEHA = (130, 100, 250, 270)

HURTBOX_RELATIVE = (0, 0, 150, 270)
COLLISION_RELATIVE = (0, 270, 150, 150)

ENNEMY_HURTBOX_RELATIVE = (70, 100, 100, 220)
ENNEMY_COLLISION_RELATIVE = (30, 300, 140, 100)


ATTACK_COOLDOWN = 500  # Milliseconds
WALK_COOLDOWN = 100
ENNEMY_ATTACK_COOLDOWN = 500

LEFT_PUNCH = 0
HIGH_KICK = 1
LOW_KICK = 2

SPECIAL_ATTACK_COST = 25
ATTACK_KEYS = [pygame.locals.K_x, pygame.locals.K_c, pygame.locals.K_v]
GAME_TIME = 18000

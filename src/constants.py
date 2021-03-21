import pygame
IDLE = 0
ATTACK = 1
WALK = 2

HITBOX_RELATIVE = (130, 0, 150, 270)
HURTBOX_RELATIVE = (0, 0, 150, 270)
COLLISION_RELATIVE = (0, 270, 150, 150)

ATTACK_COOLDOWN = 500  # Milliseconds
WALK_COOLDOWN = 300

LEFT_PUNCH = 0
HIGH_KICK = 1
LOW_KICK = 2

ATTACK_KEYS = [pygame.locals.K_SPACE, pygame.locals.K_x, pygame.locals.K_c, pygame.locals.K_v]

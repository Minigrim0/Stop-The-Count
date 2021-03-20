import time

import pygame
from pygame.locals import MOUSEBUTTONDOWN, MOUSEMOTION


class Screen(object):
    def __init__(self, size, name, fullScreen=True):
        info = pygame.display.Info()

        self.fonts = {}
        for x in [12, 25, 50, 75, 100, 200, 300]:
            self.fonts[str(x)] = pygame.font.SysFont("assets/fonts/Trump Town Pro.otf", x)

        self.nativeSize = size

        self.fullSize = (info.current_w, info.current_h)
        self.fullScreen = fullScreen
        if self.fullScreen:
            self.resize(self.fullSize)
        else:
            self.resize(self.nativeSize)

        # self.ScaleButton = pygame.image.load(const.ScaleImg).convert_alpha()
        self.ScaleRect = pygame.Rect((2, self.nativeSize[1] - 22), (20, 20))

        self.fenetre = pygame.Surface(self.nativeSize)
        pygame.display.set_caption(name)
        # Icon = pygame.image.load(IconImg).convert_alpha()
        # pygame.display.set_icon(Icon)

        self.delay = 0.05
        self.timeElapsed = time.process_time()
        self.startTime = time.process_time()

        self.frameCounter = 0
        self.FPS = 0
        self.ShowFPS = False

    def rescale(self):
        if self.fullScreen:
            self.fullScreen = False
            self.resize((1152, 704))
        else:
            self.fullScreen = True
            self.resize(self.fullSize)

    def resize(self, size):
        if self.fullScreen:
            self.fenetreAffiche = pygame.display.set_mode(
                self.fullSize, pygame.locals.FULLSCREEN)
        else:
            self.fenetreAffiche = pygame.display.set_mode(size)

        taillex = size[0]/self.nativeSize[0]
        tailley = size[1]/self.nativeSize[1]
        self.taille = min(taillex, tailley)

        self.posAffiche = (
            (size[0] - int(self.taille*self.nativeSize[0]))//2,
            (size[1] - int(self.taille*self.nativeSize[1]))//2
        )

    def flip(self):
        self.update()
        # self.fenetre.blit(self.ScaleButton, self.ScaleRect.topleft)
        # self.fenetreAffiche.blit(
        #     pygame.transform.smoothscale(
        #         self.fenetre, (
        #             int(self.nativeSize[0]*self.taille),
        #             int(self.nativeSize[1]*self.taille)
        #         )
        #     ), self.posAffiche
        # )
        self.fenetreAffiche.blit(self.fenetre, (0, 0))
        pygame.display.flip()

    def blit(self, Surface, Pos):
        self.fenetre.blit(Surface, Pos)

    def update(self):
        self.timeElapsed = time.time() - self.startTime
        self.startTime = time.time()
        self.FPS = 1/self.timeElapsed

        if self.ShowFPS:
            self.fenetre.blit(
                self.fonts["25"].render(str(round(self.FPS)), 1, (0, 0, 0)), (0, 0))

    def events(self):
        for event in pygame.event.get():
            if event.type == MOUSEMOTION or event.type == MOUSEBUTTONDOWN:
                event.pos = (
                    int((event.pos[0] - self.posAffiche[0])/self.taille),
                    int((event.pos[1] - self.posAffiche[1])/self.taille)
                )
                if event.pos[0] < 0 or event.pos[1] < 0 or event.pos[0] >= self.nativeSize[0] or event.pos[1] >= self.nativeSize[1]:
                    continue

            if event.type == pygame.locals.QUIT:
                exit()

            elif event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_F2:
                    pygame.image.save(
                        self.fenetre,
                        "screen/{}.bmp".format(
                            time.strftime("%Y_%m_%d_%H_%M_%S")
                        )
                    )
                elif event.key == pygame.locals.K_F11:
                    self.rescale()
                elif event.key == pygame.locals.K_F3:
                    self.ShowFPS = not self.ShowFPS

            elif event.type == pygame.locals.VIDEORESIZE:
                self.resize(event.size)
            elif event.type == MOUSEBUTTONDOWN:
                if self.ScaleRect.collidepoint(event.pos):
                    self.rescale()

            yield event

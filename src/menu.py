import pygame


class Menu(object):
    def __init__(self, background, buttons=[], quitOnEscape=False):
        self.buttons = buttons
        self.background = background
        self.running = True
        self.pointerImg = pygame.transform.scale(pygame.image.load("assets/img/cursor.png"), (60, 80))
        self.pointerImg_rect = self.pointerImg.get_rect()
        self.quitOnEscape = quitOnEscape
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
    
    def update(self, screen):
        for event in screen.events():
            if event.type == pygame.locals.MOUSEBUTTONUP:
                for button in self.buttons:
                    button.click(event.pos)
            elif event.type == pygame.locals.MOUSEMOTION:
                for button in self.buttons:
                    button.collide(event.pos)
            elif event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_ESCAPE and self.quitOnEscape:
                    self.stop()
        self.pointerImg_rect.center = pygame.mouse.get_pos()

    def draw(self, screen):
        if self.background is not None:
            screen.blit(self.background, (0, 0))
        for button in self.buttons:
            button.draw(screen)
        screen.blit(self.pointerImg, self.pointerImg_rect)
        screen.flip()

    def stop(self):
        self.running = False
    
    def run(self, screen, game=None):
        self.running = True
        while self.running:
            if game:
                game.draw(screen)
                screen.blit(game.closeMenu, (10, 10))
                screen.blit(game.gameEndTimeDisplay, (10, 30))
            self.update(screen)
            self.draw(screen)


class Button(object):
    def __init__(self, pos, size, text, callback, **callbackargs):
        self.position = pos
        self.size = size
        self.text = text
        self.callback = callback
        self.callback_args = callbackargs
        self.hover = False

    def build(self, screen):
        self.image = pygame.Surface(self.size)
        self.textImage = screen.fonts["25"].render(self.text, 1, (255, 255, 255))
        self.text_rect = self.textImage.get_rect(center=(self.image.get_size()[0] / 2, self.image.get_size()[1] / 2))
        self.image.blit(self.textImage, self.text_rect) 

    def draw(self, screen):
        if self.hover:
            self.image.fill(pygame.Color(128,128,128))
        else:
            self.image.fill(pygame.Color(0, 0, 0))
        self.image.blit(self.textImage, self.text_rect) 
        screen.blit(self.image, self.position)

    def collide(self, position):
        if self.position[0] + self.size[0] > position[0] > self.position[0]:
            if self.position[1] + self.size[1] > position[1] > self.position[1]:
                self.hover = True
                return True
        self.hover = False
        return False

    def click(self, position):
        if self.collide(position):
            self.callback(**self.callback_args)

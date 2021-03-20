import pygame


class Menu(object):
    def __init__(self, background, buttons=[]):
        self.buttons = buttons
        self.background = background
        self.running = True

    def update(self, screen):
        for event in screen.events():
            if event.type == pygame.locals.MOUSEBUTTONUP:
                for button in self.buttons:
                    button.click(event.pos)

    def draw(self, screen):
        if self.background is not None:
            screen.blit(self.background, (0, 0))
        for button in self.buttons:
            button.draw(screen)

        screen.flip()

    def run(self, screen):
        while self.running:
            self.update(screen)
            self.draw(screen)


class Button(object):
    def __init__(self, pos, size, text, callback):
        self.position = pos
        self.size = size
        self.text = text
        self.callback = callback

    def build(self, screen):
        self.image = pygame.Surface((self.size))
        self.image.blit(screen.fonts["25"].render(self.text, 1, (255, 255, 255)), (0, 0))

    def draw(self, screen):
        screen.blit(self.image, self.position)

    def collide(self, position):
        if self.position[0] + self.size[0] > position[0] > self.position[0]:
            if self.position[1] + self.size[1] > position[1] > self.position[1]:
                return True
        return False

    def click(self, position):
        if self.collide(position):
            self.callback()

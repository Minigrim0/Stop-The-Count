import pygame


class Menu(object):
    def __init__(self, background, buttons=[]):
        self.buttons = buttons
        self.background = background
        self.running = True
        self.pointerImg = pygame.transform.scale(pygame.image.load("assets/img/cursor.png"), (60, 80))
        self.pointerImg_rect = self.pointerImg.get_rect()
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        self.title = "Stop the count!"
        self.title2 = "______________" 
        self.title3 = "____________________" 
        self.iVoted = pygame.transform.scale(pygame.image.load("assets/img/Ivoted.jpg").convert_alpha(), (300, 200))

    def rot_center(self, image, angle):
        """ Rotations en gardant l'image au centre """
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def update(self, screen):
        for event in screen.events():
            if event.type == pygame.locals.MOUSEBUTTONUP:
                for button in self.buttons:
                    button.click(event.pos)
            elif event.type == pygame.locals.MOUSEMOTION:
                for button in self.buttons:
                    button.collide(event.pos)
        self.pointerImg_rect.center = pygame.mouse.get_pos()

    def draw(self, screen):
        if self.background is not None:
            screen.blit(self.background, (0, 0))
            screen.blit(screen.fonts["200"].render(self.title, 1, (220, 20, 60)), (200, 70)) 
            screen.blit(screen.fonts["200"].render(self.title2, 1, (220, 20, 60)), (200, 90))
            screen.blit(screen.fonts["200"].render(self.title3, 1, (220, 20, 60)), (200, 110))
            screen.blit(self.iVoted, (1450, 150))
        for button in self.buttons:
            button.draw(screen)
        screen.blit(self.pointerImg, self.pointerImg_rect)
        screen.flip()

    def run(self, screen):
        while self.running:
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
            self.callback(self.callbackargs)

import pygame
from src.menu import Menu, Button
from src.screen import Screen


pygame.init()

screen = Screen((1920, 1080), "Stop the count!", fullScreen=True)

button_play = Button((100, 100), (250, 40), "Test lel", None)
button_play.build(screen)
mainMenu = Menu(pygame.image.load("assets/img/background.png"), [button_play])


def main():
    mainMenu.run(screen)


if __name__ == "__main__":
    main()

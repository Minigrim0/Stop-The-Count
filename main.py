import pygame
from src.menu import Menu, Button
from src.screen import Screen


pygame.init()

screen = Screen((1920, 1080), "Stop the count!", fullScreen=False)

button_play = Button((835, 200), (250, 40), "Jouer", None)
button_quit = Button((835, 300), (250, 40), "Quitter", exit)
button_play.build(screen)
button_quit.build(screen)
mainMenu = Menu(pygame.image.load("assets/img/background.png"), [button_play, button_quit])


def main():
    mainMenu.run(screen)


if __name__ == "__main__":
    main()

import pygame
from src.menu import Menu, Button
from src.screen import Screen
from src.game import Game


pygame.init()

screen = Screen((1920, 1080), "Stop the count!", fullScreen=False)

game = Game()

button_play = Button((300, 400), (300, 60), "Jouer", game.run, screen=screen)
button_load = Button((300, 500), (300, 60), "Charger une partie", exit)
button_howToPlay = Button((300, 600), (300, 60), "Comment Jouer ?", exit)
button_quit = Button((300, 700), (300, 60), "Quitter", exit)
button_play.build(screen)
button_load.build(screen)
button_howToPlay.build(screen)
button_quit.build(screen)
mainMenu = Menu(pygame.image.load("assets/img/background.jpg"), [button_play, button_load, button_howToPlay, button_quit])


def main():
    mainMenu.run(screen)


if __name__ == "__main__":
    main()

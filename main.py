import pygame
from src.menu import Menu, Button
from src.screen import Screen
from src.game import Game

def runGame(screen, tutorialMenu):
    game = Game(screen, tutorialMenu)
    game.run(screen)

pygame.init()

screen = Screen((1920, 1080), "Stop the count!", fullScreen=False)

tutorialMenu = Menu(pygame.image.load("assets/img/buildWall.jpg"), [], True)
button_quitMenu = Button((10, 10), (60, 60), "Back", tutorialMenu.stop)
button_quitMenu.build(screen)
tutorialMenu.buttons.append(button_quitMenu)



button_play = Button((300, 400), (300, 60), "Play", runGame, screen=screen, tutorialMenu=tutorialMenu)

button_howToPlay = Button((300, 500), (300, 60), "How To Build Walls", tutorialMenu.run, screen=screen)
button_quit = Button((300, 700), (300, 60), "Quit", exit)
button_play.build(screen)

button_howToPlay.build(screen)
button_quit.build(screen)
mainMenu = Menu(pygame.image.load("assets/img/background.jpg"), [button_play, button_howToPlay, button_quit])


def main():
    mainMenu.run(screen)


if __name__ == "__main__":
    main()

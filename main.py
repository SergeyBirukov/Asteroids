from resources import Resources
from game import Game
from main_menu import MainMenu
from leaderboard import LeaderBoard
import pygame


if __name__ == '__main__':
    pygame.init()
    leaderboard = LeaderBoard()
    main_menu = MainMenu(Game, leaderboard)
    main_menu.menu()

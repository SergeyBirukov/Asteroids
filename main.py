from resources import Resources
from game import Game
from main_menu import MainMenu
from leaderboard import LeaderBoard


if __name__ == '__main__':
    game = Game(resources=Resources())
    leaderboard = LeaderBoard()
    main_menu = MainMenu(game, leaderboard)
    main_menu.menu()

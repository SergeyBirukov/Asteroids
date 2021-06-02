from resources import Resources
from game import Game
from main_menu import MainMenu


if __name__ == '__main__':
    game = Game(resources=Resources())
    main_menu = MainMenu(game)
    main_menu.menu()

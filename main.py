from os import path
from resources import Resources
from game import Game
from main_menu import MainMenu


img_dir = path.join(path.dirname(__file__), "img")
sound_dir = path.join(path.dirname(__file__), "sound")


if __name__ == '__main__':
    game = Game(resources=Resources(img_dir))
    main_menu = MainMenu(game)
    main_menu.menu()

"""
Simple jeu fait avec arcade.
Le jeu consiste a ce que notre poisson mange des poissons plus petits que lui pour grossir.
L'utilisateur doit aussi éviter les poissons plus gros afin de ne pas perdre de vie.
"""
import random

import arcade

import game_constants as gc

from menu_view import MenuView


def main():
    """ Main method """
    window = arcade.Window(gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT, gc.SCREEN_TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()

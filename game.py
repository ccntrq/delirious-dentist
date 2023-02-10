"""
Delirious Dentist
"""
import os
import sys
import arcade

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, "src")
sys.path.append(mymodule_dir)

import config

from view.game import GameView
from view.instruction import InstructionView


def main():
    """Main function"""
    window = arcade.Window(
        config.SCREEN_WIDTH, config.SCREEN_HEIGHT, config.SCREEN_TITLE
    )

    game_view = GameView()
    game_view.setup()
    start_view = InstructionView(game_view)
    start_view.setup()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()

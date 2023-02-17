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

from sound import Sound
from view.game import GameView
from view.instruction import InstructionView


def main():
    """Main function"""
    if config.DEBUG:
        arcade.enable_timings()

    window = arcade.Window(
        config.SCREEN_WIDTH, config.SCREEN_HEIGHT, config.SCREEN_TITLE
    )

    sound = Sound()
    game_view = GameView(sound)
    game_view.setup()
    start_view = InstructionView(game_view, sound)
    start_view.setup()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()

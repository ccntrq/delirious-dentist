import arcade

import config

class InstructionView(arcade.View):
    """View to show instructions before the game"""

    def __init__(self, game_view):
        """This is run once when we switch to this view"""
        super().__init__()

        self.game_view = game_view

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, config.SCREEN_WIDTH - 1, 0, config.SCREEN_HEIGHT - 1)
        self.game_opening_sound = arcade.load_sound(config.GAME_OPENING_SOUND_RESOURCE)
        arcade.play_sound(self.game_opening_sound)

        self.cover_art_list = None

        self.setup()

    def setup(self):
        self.cover_art_list = arcade.SpriteList()

        # Create main title
        main_title = arcade.Sprite(config.SCREEN_MAIN_TITLE_IMAGE_SOURCE, 1)
        main_title.center_x = config.SCREEN_WIDTH / 2
        main_title.center_y = config.SCREEN_HEIGHT - 120
        self.cover_art_list.append(main_title)

    def on_draw(self):
        """Draw this view"""
        self.clear()

        self.game_view.on_draw()

        self.cover_art_list.draw()
        font = "Kenney Blocks"
        text_color = arcade.color.WHITE
        text_start = config.SCREEN_HEIGHT * 0.75
        arcade.draw_text(
            "Press space to perform a root treatment. Collect tooth for your precious roots collection and avoid beeing hit by angry patients",
            0,
            text_start - 90,
            text_color,
            32,
            width=config.SCREEN_WIDTH,
            align="center",
            font_name=font,
        )
        arcade.draw_text(
            "PRESS SPACE TO START THE GAME",
            0,
            text_start - 350,
            text_color,
            24,
            width=config.SCREEN_WIDTH,
            align="center",
            font_name=font,
        )

    def on_key_release(self, key, _modifiers):
        """If the user releases the space key, start the game."""
        if key == arcade.key.SPACE:
            self.window.show_view(self.game_view)
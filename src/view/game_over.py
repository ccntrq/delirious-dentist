import arcade

import config
from score_board import ScoreBoard

class GameOverView(arcade.View):
    """View to show when game is over"""

    def __init__(self, game_view):
        """This is run once when we switch to this view"""
        super().__init__()
        self.game_view = game_view
        self.score = game_view.score
        self.gameover_time = ScoreBoard().store_score(self.score)

        self.scoreboard_ui_elements_list = None

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, config.SCREEN_WIDTH - 1, 0, config.SCREEN_HEIGHT - 1)

    def setup(self):
        self.scoreboard_ui_elements_list = arcade.SpriteList()
        ui_scoreboard = arcade.Sprite(config.UI_SCOREBOARD_IMAGE_SOURCE, 1.25)
        ui_scoreboard.center_x = config.SCREEN_WIDTH / 2
        ui_scoreboard.center_y = config.SCREEN_HEIGHT / 2 - 48
        self.scoreboard_ui_elements_list.append(ui_scoreboard)

    def on_draw(self):
        """Draw this view"""

        self.clear()

        self.game_view.on_draw()

        ui_scoreboard = arcade.Sprite(config.UI_SCOREBOARD_IMAGE_SOURCE, 1.25)
        ui_scoreboard.center_x = config.SCREEN_WIDTH / 2
        ui_scoreboard.center_y = config.SCREEN_HEIGHT / 2 - 48
        ui_scoreboard.draw()

        text_color = arcade.color.BLACK
        text_color_current = arcade.color.BANANA_YELLOW
        begin_x = config.SCREEN_HEIGHT * 0.75
        font = "Kenney Blocks"
        arcade.draw_text(
            "GAME OVER",
            0,
            begin_x,
            text_color,
            48,
            width=config.SCREEN_WIDTH,
            align="center",
            font_name=font,
        )
        arcade.draw_text(
            f"SCORE: {self.score}",
            0,
            begin_x - 48,
            text_color_current,
            32,
            width=config.SCREEN_WIDTH,
            align="center",
            font_name=font,
        )
        arcade.draw_text(
            "PRESS ENTER TO RESTART",
            0,
            begin_x - 90,
            text_color,
            24,
            width=config.SCREEN_WIDTH,
            align="center",
            font_name=font,
        )

        arcade.draw_text(
            "HIGH SCORES:",
            0,
            begin_x - 140,
            text_color,
            24,
            width=config.SCREEN_WIDTH,
            align="center",
            font_name=font,
        )
        i = 0
        for high_score in ScoreBoard().get_high_scores():
            arcade.draw_text(
                f"{high_score[0]:03}  -  {high_score[1]}",
                0,
                begin_x - 170 - i * 30,
                text_color_current
                if self.gameover_time == high_score[1]
                else text_color,
                24,
                width=config.SCREEN_WIDTH,
                align="center",
                font_name=font,
            )
            i += 1

    def on_key_release(self, key, _modifiers):
        """If the user releases the ENTER key, re-start the game."""
        if key == arcade.key.ENTER:
            self.game_view.setup()
            self.window.show_view(self.game_view)

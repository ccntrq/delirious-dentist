import arcade

import config
from sprite.bolt import BoltSprite
from sprite.dentist import DentistSprite
from sprite.flask import FlaskSprite
from sprite.heart import HeartSprite
from sprite.pliers import PliersSprite
from util.position import PositionUtil


class UI:
    def __init__(self, game):
        self.game = game

        self.life_list = None
        self.static_ui_elements_list = None
        self.pliers_sprite = None
        self.flask_sprite = None
        self.bolt_sprite = None

        self.setup()

    def setup(self):
        self.life_list = arcade.SpriteList()
        self.static_ui_elements_list = arcade.SpriteList()

        for _ in range(config.CHARACTER_LIFES):
            self.add_life()

        ui_tooth = arcade.Sprite(config.UI_TOOTH_IMAGE_SOURCE, 0.25)
        ui_tooth.center_x = 930
        ui_tooth.center_y = config.UI_HEIGHT - 38
        self.static_ui_elements_list.append(ui_tooth)

        self.setup_bolt()
        self.setup_pliers()
        self.setup_flask()

    def on_draw(self):
        "Draw ui elements"
        self.static_ui_elements_list.draw()
        self.life_list.draw()

        self.life_list.draw()
        self.static_ui_elements_list.draw()
        arcade.draw_text(
            str(self.game.score),
            950,
            12,
            arcade.color.BLACK,
            24,
            width=config.SCREEN_WIDTH,
            align="left",
        )

    def on_update(self, delta_time):
        self.pliers_sprite.alpha = (
            255 if self.game.player_sprite.pliers_equipped else 50
        )

        if self.game.bolt_active > 100:
            self.bolt_sprite.alpha = 255
            self.bolt_sprite.is_blinking = False
        elif self.game.bolt_active > 0:
            self.bolt_sprite.is_blinking = True
        else:
            self.bolt_sprite.is_blinking = False
            self.bolt_sprite.alpha = 50

        if self.game.flask_active > 100:
            self.flask_sprite.alpha = 255
            self.flask_sprite.is_blinking = False
        elif self.game.flask_active > 0:
            self.flask_sprite.is_blinking = True
        else:
            self.flask_sprite.is_blinking = False
            self.flask_sprite.alpha = 50

        self.static_ui_elements_list.update_animation(delta_time)

    def add_life(self):
        lifes = len(self.life_list.sprite_list)
        life = HeartSprite()
        life.center_x = lifes * 40 + 32
        life.center_y = config.UI_HEIGHT - 40

        self.life_list.append(life)

    def remove_life(self):
        if len(self.life_list.sprite_list) > 0:
            life = self.life_list.sprite_list[-1]
            life.remove_from_sprite_lists()

    def setup_pliers(self):
        self.pliers_sprite = PliersSprite(0.2)
        self.pliers_sprite.center_x = 900
        self.pliers_sprite.center_y = config.UI_HEIGHT - 40
        self.pliers_sprite.alpha = 50
        self.static_ui_elements_list.append(self.pliers_sprite)

    def setup_bolt(self):
        self.bolt_sprite = BoltSprite(0.4)
        self.bolt_sprite.center_x = 870
        self.bolt_sprite.center_y = config.UI_HEIGHT - 40
        self.bolt_sprite.alpha = 50
        self.static_ui_elements_list.append(self.bolt_sprite)

    def setup_flask(self):
        self.flask_sprite = FlaskSprite(0.4)
        self.flask_sprite.center_x = 840
        self.flask_sprite.center_y = config.UI_HEIGHT - 40
        self.flask_sprite.alpha = 50
        self.static_ui_elements_list.append(self.flask_sprite)

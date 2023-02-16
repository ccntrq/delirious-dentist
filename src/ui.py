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

    def add_pliers(self):
        pliers = PliersSprite(0.2)
        pliers.center_x = 900
        pliers.center_y = config.UI_HEIGHT - 40
        self.static_ui_elements_list.append(pliers)

    def add_bolt(self):
        bolt = BoltSprite(0.4)
        bolt.center_x = 870
        bolt.center_y = config.UI_HEIGHT - 40
        self.static_ui_elements_list.append(bolt)

    def remove_bolt(self):
        items = self.static_ui_elements_list.sprite_list
        self.static_ui_elements_list.clear()
        for item in items:
            if not isinstance(item, BoltSprite):
                self.static_ui_elements_list.append(item)

    def add_flask(self):
        flask = FlaskSprite(0.4)
        flask.center_x = 840
        flask.center_y = config.UI_HEIGHT - 40
        self.static_ui_elements_list.append(flask)

    def remove_flask(self):
        items = self.static_ui_elements_list.sprite_list
        self.static_ui_elements_list.clear()
        for item in items:
            if not isinstance(item, FlaskSprite):
                self.static_ui_elements_list.append(item)

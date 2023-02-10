import arcade

import config


class PliersSprite(arcade.Sprite):
    def __init__(self, scale):
        # Set up parent class
        super().__init__()

        self.scale = scale
        self.texture = arcade.load_texture(config.UI_PLIER_IMAGE_SOURCE)

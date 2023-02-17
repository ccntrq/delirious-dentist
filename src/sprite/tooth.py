import arcade

import config


class ToothSprite(arcade.Sprite):
    def __init__(self):
        # Set up parent class
        super().__init__()

        self.scale = 0.5
        self.points = config.TOOTH_POINTS
        self.texture = arcade.load_texture(config.UI_TOOTH_IMAGE_SOURCE)

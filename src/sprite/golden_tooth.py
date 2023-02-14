import arcade

import config


class GoldenToothSprite(arcade.Sprite):
    def __init__(self):
        # Set up parent class
        super().__init__()

        self.scale = 0.75
        self.points = config.GOLDEN_TOOTH_POINTS
        self.texture = arcade.load_texture(config.UI_GOLDEN_TOOTH_IMAGE_SOURCE)

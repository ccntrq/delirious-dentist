import arcade

import config


class HeartSprite(arcade.Sprite):
    def __init__(self):
        # Set up parent class
        super().__init__()

        self.scale = config.TILE_SCALING
        self.texture = arcade.load_texture(config.UI_HEART_IMAGE_SOURCE)

import arcade

import config
from animation.blink import BlinkAnimation


class FlaskSprite(BlinkAnimation, arcade.Sprite):
    def __init__(self, scale=config.TILE_SCALING):
        # Set up parent class
        super().__init__()

        self.scale = scale
        self.texture = arcade.load_texture(config.UI_FLASK_IMAGE_SOURCE)

import arcade

import config


class BoltSprite(arcade.Sprite):
    def __init__(self, scale=config.TILE_SCALING):
        # Set up parent class
        super().__init__()

        self.scale = scale
        self.texture = arcade.load_texture(config.UI_BOLT_IMAGE_SOURCE)

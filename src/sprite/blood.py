import arcade

import config


class BloodSprite(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.scale = 1
        self.texture = arcade.load_texture(config.FX_BLOOD_IMAGE_SOURCE)

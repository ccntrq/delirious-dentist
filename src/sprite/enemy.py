import arcade
import math
import random

import config
from util.direction import DirectionUtil


class EnemySprite(arcade.Sprite):
    def __init__(self):
        # Set up parent class
        super().__init__()

        image_sources = [
            config.ENEMY_1_IMAGE_SOURCE,
            config.ENEMY_2_IMAGE_SOURCE,
            config.ENEMY_3_IMAGE_SOURCE,
        ]
        image_source = random.choice(image_sources)
        self.scale = config.CHARACTER_SCALING
        self.texture = arcade.load_texture(image_source)

    def away_from(self, sprite):
        dir = DirectionUtil.away_from(self, sprite)

        self.change_x = dir[0] * config.ENEMY_MAX_SPEED / 2
        self.change_y = dir[1] * config.ENEMY_MAX_SPEED / 2

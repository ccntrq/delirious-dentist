import arcade
import math
import random

import config


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
        start_x = self.center_x
        start_y = self.center_y

        dest_x = sprite.center_x
        dest_y = sprite.center_y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        self.change_x = -1 * math.cos(angle) * config.ENEMY_MAX_SPEED / 2
        self.change_y = -1 * math.sin(angle) * config.ENEMY_MAX_SPEED / 2

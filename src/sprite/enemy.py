import arcade
import math
import random

import config
from util.direction import DirectionUtil


class EnemySprite(arcade.Sprite):
    def __init__(self, decoration_list):
        # Set up parent class
        super().__init__()

        image_sources = [
            config.ENEMY_1_IMAGE_SOURCE,
            # TODO: readd more sprites
            #config.ENEMY_2_IMAGE_SOURCE,
            #config.ENEMY_3_IMAGE_SOURCE,
        ]
        image_source = random.choice(image_sources)
        self.scale = config.TILE_SCALING
        self.texture = arcade.load_texture(image_source)
        self.decoration_list = decoration_list
        self.set_random_speed_and_direction()

    def on_update(self, delta_time: float = 1 / 60):
        self.move()

    def move(self):
        super().update()

        if self.right > config.ENEMY_RIGHT_BORDER:
            self.change_x = -abs(self.change_x)
        elif self.left < config.ENEMY_LEFT_BORDER:
            self.change_x = abs(self.change_x)
        if self.top > config.ENEMY_TOP_BORDER:
            self.change_y = -abs(self.change_y)
        elif self.bottom < config.ENEMY_BOTTOM_BORDER:
            self.change_y = abs(self.change_y)
        else:
            collisions = arcade.check_for_collision_with_list(
                self, self.decoration_list
            )
            if len(collisions) > 0:
                self.away_from(collisions[0])

    def set_random_speed_and_direction(self):
        self.change_x = random.randint(0, config.ENEMY_MAX_SPEED)
        self.change_y = random.randint(0, config.ENEMY_MAX_SPEED - self.change_x)

    def away_from(self, sprite):
        dir = DirectionUtil.away_from(self, sprite)

        self.change_x = dir[0] * config.ENEMY_MAX_SPEED / 2
        self.change_y = dir[1] * config.ENEMY_MAX_SPEED / 2

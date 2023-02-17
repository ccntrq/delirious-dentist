import arcade
import random

import config


class PositionUtil:
    @staticmethod
    def random_x():
        return random.randint(
            config.ENEMY_LEFT_BORDER + 64, config.ENEMY_RIGHT_BORDER - 64
        )

    @staticmethod
    def random_y():
        return random.randint(
            config.ENEMY_BOTTOM_BORDER + 64, config.ENEMY_TOP_BORDER - 64
        )

    @staticmethod
    def set_random_position_without_collision(sprite, *otherSpriteLists):
        for _ in range(0, 99):
            sprite.center_x = PositionUtil.random_x()
            sprite.center_y = PositionUtil.random_y()

            if not arcade.check_for_collision_with_lists(sprite, otherSpriteLists):
                return

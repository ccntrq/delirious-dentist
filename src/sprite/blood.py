import arcade

import config


class BloodSprite(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.scale = 1
        self.texture = arcade.load_texture(config.FX_BLOOD_IMAGE_SOURCE)

    def on_update(self, delta_time: float = 1 / 60):
        self.move()
        self.change_x -= 0.7
        self.change_y -= 0.7

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

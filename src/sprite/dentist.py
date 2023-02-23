import arcade

import config

MAIN_TEXTURE = 0
HIT_TEXTURE = 1
PLIERS_HIT_TEXTURE = 2


class DentistSprite(arcade.Sprite):
    def __init__(self):
        # Set up parent class
        super().__init__()

        self.scale = config.CHARACTER_SCALING
        self.pliers_equipped = False

        self.movement_speed = config.CHARACTER_MOVEMENT_SPEED

        texture_resources = [
            config.CHARACTER_DENTIST_IMAGE_SOURCE,
            config.CHARACTER_DENTIST_ATTACK_IMAGE_SOURCE,
            config.CHARACTER_DENTIST_ATTACK_PLIER_IMAGE_SOURCE,
        ]

        self.hit_boxes = list(
            map(
                lambda r: arcade.Sprite(r, self.scale).get_hit_box(),
                texture_resources,
            )
        )

        # Set up the player, specifically placing it at these coordinates.
        self.textures = list(map(arcade.load_texture, texture_resources))
        self.texture = self.textures[MAIN_TEXTURE]
        self.hit_active = 0
        self.flask_active = False

    def update_animation(self, delta_time: float = 1 / 60):
        texture_index = (
            PLIERS_HIT_TEXTURE
            if self.hit_active and self.pliers_equipped
            else HIT_TEXTURE
            if self.hit_active
            else MAIN_TEXTURE
        )

        self.texture = self.textures[texture_index]
        self.hit_box = self.hit_boxes[texture_index]

    def is_hitting(self):
        return self.hit_active > 0 or self.flask_active

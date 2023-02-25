import arcade

import config

MAIN_TEXTURE = 0
HIT_TEXTURE = 8
PLIERS_HIT_TEXTURE = 12


class DentistSprite(arcade.Sprite):
    def __init__(self):
        # Set up parent class
        super().__init__()

        self.scale = config.CHARACTER_SCALING
        self.pliers_equipped = False

        self.movement_speed = config.CHARACTER_MOVEMENT_SPEED

        self.time_passed = 0

        texture_resources = [
            config.CHARACTER_DENTIST_IMAGE_SOURCE_1,
            config.CHARACTER_DENTIST_IMAGE_SOURCE_2,
            config.CHARACTER_DENTIST_LEFT_IMAGE_SOURCE_1,
            config.CHARACTER_DENTIST_LEFT_IMAGE_SOURCE_2,
            config.CHARACTER_DENTIST_RIGHT_IMAGE_SOURCE_1,
            config.CHARACTER_DENTIST_RIGHT_IMAGE_SOURCE_2,
            config.CHARACTER_DENTIST_UP_IMAGE_SOURCE_1,
            config.CHARACTER_DENTIST_UP_IMAGE_SOURCE_2,
            config.CHARACTER_DENTIST_ATTACK_IMAGE_SOURCE,
            config.CHARACTER_DENTIST_ATTACK_LEFT_IMAGE_SOURCE,
            config.CHARACTER_DENTIST_ATTACK_RIGHT_IMAGE_SOURCE,
            config.CHARACTER_DENTIST_ATTACK_UP_IMAGE_SOURCE,
            config.CHARACTER_DENTIST_ATTACK_PLIER_IMAGE_SOURCE,
            config.CHARACTER_DENTIST_ATTACK_PLIER_LEFT_IMAGE_SOURCE,
            config.CHARACTER_DENTIST_ATTACK_PLIER_RIGHT_IMAGE_SOURCE,
            config.CHARACTER_DENTIST_ATTACK_PLIER_UP_IMAGE_SOURCE,
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
        self.time_passed += 1
        texture_index = (
            PLIERS_HIT_TEXTURE
            if self.is_hitting() and self.pliers_equipped
            else HIT_TEXTURE
            if self.is_hitting()
            else MAIN_TEXTURE
        )

        if texture_index == MAIN_TEXTURE:
            texture_index += 2 * (
                0
                if self.change_y < 0
                else 3
                if self.change_y > 0
                else 1
                if self.change_x < 0
                else 2
                if self.change_x > 0
                else 0
            )
            if self.change_x != 0 or self.change_y !=0:
              texture_index += 1 if ((self.time_passed // 20) % 2 == 0) else 0
        else:
            texture_index += (
                0
                if self.change_y < 0
                else 3
                if self.change_y > 0
                else 1
                if self.change_x < 0
                else 2
                if self.change_x > 0
                else 0
            )

        self.texture = self.textures[texture_index]
        self.hit_box = self.hit_boxes[texture_index]

    def is_hitting(self):
        return self.hit_active > 0 or self.flask_active

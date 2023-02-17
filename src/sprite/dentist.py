import arcade

import config


class DentistSprite(arcade.Sprite):
    def __init__(self):
        # Set up parent class
        super().__init__()

        self.scale = config.CHARACTER_SCALING
        self.pliers_equipped = False

        self.movement_speed = config.CHARACTER_MOVEMENT_SPEED

        # Set up the player, specifically placing it at these coordinates.
        main_image_source = config.CHARACTER_DENTIST_IMAGE_SOURCE
        hit_image_source = config.CHARACTER_DENTIST_ATTACK_IMAGE_SOURCE
        pliers_hit_image_source = config.CHARACTER_DENTIST_ATTACK_PLIER_IMAGE_SOURCE
        self.main_texture = arcade.load_texture(main_image_source)
        self.hit_texture = arcade.load_texture(hit_image_source)
        self.pliers_hit_texture = arcade.load_texture(pliers_hit_image_source)
        self.texture = self.main_texture
        self.hit_active = 0
        self.flask_active = False

    def update_animation(self, delta_time: float = 1 / 60):
        if self.is_hitting():
            self.texture = (
                self.pliers_hit_texture if self.pliers_equipped else self.hit_texture
            )
            return

        self.texture = self.main_texture

    def is_hitting(self):
        return self.hit_active > 0 or self.flask_active

import arcade

import config


class DentistSprite(arcade.Sprite):
    def __init__(self):
        # Set up parent class
        super().__init__()

        self.scale = config.CHARACTER_SCALING
        self.pliers_equipped = False

        self.movement_speed = config.CHARACTER_MOVEMENT_SPEED

        # XXX auto set hitbox or adjust coordinates to our sprite
        # self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        # Set up the player, specifically placing it at these coordinates.
        main_image_source = config.CHARACTER_DENTIST_IMAGE_SOURCE
        hit_image_source = config.CHARACTER_DENTIST_ATTACK_IMAGE_SOURCE
        pliers_hit_image_source = config.CHARACTER_DENTIST_ATTACK_PLIER_IMAGE_SOURCE
        self.main_texture = arcade.load_texture(main_image_source)
        self.hit_texture = arcade.load_texture(hit_image_source)
        self.pliers_hit_texture = arcade.load_texture(pliers_hit_image_source)
        self.texture = self.main_texture
        self.main_hit_box = self.get_hit_box()
        self.hit_hit_box = self.main_hit_box
        # XXX Unused. Changing to a larger hit box pushes us away from borders
        # XXX when hitting close while close to one
        # self.hit_hit_box = list(map(
        #    lambda x: [x[0] * 1.5, x[1] * 1.5], list(self.main_hit_box)))
        self.hit_active = 0
        self.flask_active = False

    def update_animation(self, delta_time: float = 1 / 60):
        if self.is_hitting():
            self.texture = (
                self.pliers_hit_texture if self.pliers_equipped else self.hit_texture
            )
            self.hit_box = self.hit_hit_box
            return

        self.texture = self.main_texture
        self.hit_box = self.main_hit_box

    def is_hitting(self):
        return self.hit_active > 0 or self.flask_active

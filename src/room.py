import arcade

import config
from sprite.dentist import DentistSprite
from util.position import PositionUtil


class Room:
    def __init__(self):
        self.wall_list = None
        self.decoration_list = None
        self.floor_list = None

        self.setup()

    def setup(self):
        # Walls use spatial hashing for faster collision detection
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.decoration_list = arcade.SpriteList(use_spatial_hash=True)
        self.floor_list = arcade.SpriteList(use_spatial_hash=True)

        # Create walls
        # Create lower boundary
        for x in range(0, config.SCREEN_WIDTH, 256):
            wall = arcade.Sprite(config.ROOM_WINDOW_IMAGE_SOURCE, 0.5)
            wall.center_x = x + 128
            wall.center_y = config.UI_HEIGHT + 16
            self.wall_list.append(wall)

        # Create upper boundary
        for x in range(0, config.SCREEN_WIDTH, 256):
            wall = arcade.Sprite(config.ROOM_WINDOW_IMAGE_SOURCE, 0.5)
            wall.center_x = x + 128
            wall.center_y = config.SCREEN_HEIGHT - 32
            self.wall_list.append(wall)

        # Create left boundary
        for y in range(config.UI_HEIGHT + 80, config.SCREEN_HEIGHT, 56):
            wall = arcade.Sprite(config.ROOM_WINDOW_LEFT_IMAGE_SOURCE, 0.5)
            wall.center_x = 12
            wall.center_y = y
            self.wall_list.append(wall)

        # Create right boundary
        for y in range(config.UI_HEIGHT + 80, config.SCREEN_HEIGHT, 56):
            wall = arcade.Sprite(config.ROOM_WINDOW_RIGHT_IMAGE_SOURCE, 0.5)
            wall.center_x = config.SCREEN_WIDTH - 12
            wall.center_y = y
            self.wall_list.append(wall)

        # Create the floor
        for x in range(0, config.SCREEN_WIDTH, 256):
            for y in range(config.UI_HEIGHT, config.SCREEN_HEIGHT, 256):
                floor = arcade.Sprite(
                    config.ROOM_TILE_FLOOR_IMAGE_SOURCE, 2
                )
                floor.center_x = x + 128
                floor.center_y = y
                self.floor_list.append(floor)

        # Create interior
        room_chair = arcade.Sprite(config.ROOM_CHAIR_IMAGE_SOURCE, config.TILE_SCALING)
        self.set_random_sprite_location_without_decoration_collision(room_chair)
        self.decoration_list.append(room_chair)

        room_plant = arcade.Sprite(config.ROOM_PLANT_IMAGE_SOURCE, config.TILE_SCALING)
        self.set_random_sprite_location_without_decoration_collision(room_plant)
        self.decoration_list.append(room_plant)

        room_xray = arcade.Sprite(config.ROOM_XRAY_IMAGE_SOURCE, config.TILE_SCALING)
        self.set_random_sprite_location_without_decoration_collision(room_xray)
        self.decoration_list.append(room_xray)

        room_vending_machine = arcade.Sprite(
            config.ROOM_VENDING_MACHINE_IMAGE_SOURCE, config.TILE_SCALING
        )
        self.set_random_sprite_location_without_decoration_collision(
            room_vending_machine
        )
        self.decoration_list.append(room_vending_machine)

        room_water_dispenser = arcade.Sprite(
            config.ROOM_WATER_DISPENSER_IMAGE_SOURCE, config.TILE_SCALING
        )
        self.set_random_sprite_location_without_decoration_collision(
            room_water_dispenser
        )
        self.decoration_list.append(room_water_dispenser)

    def on_draw(self):
        "Draw room elements"
        self.floor_list.draw(pixelated=True)
        self.wall_list.draw(pixelated=True)
        self.decoration_list.draw(pixelated=True)

    def set_random_sprite_location_without_decoration_collision(self, sprite):
        PositionUtil.set_random_position_without_collision(sprite, self.decoration_list)

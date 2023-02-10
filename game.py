"""
Delirious Dentist
"""
import datetime
import math
from operator import itemgetter
import os
import random
import sys
import arcade
import pyglet

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, "src")
sys.path.append(mymodule_dir)

import config


class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__()

        arcade.set_background_color(arcade.csscolor.WHITE_SMOKE)

        self.score = None
        self.player_list = None
        self.wall_list = None
        self.decoration_list = None
        self.enemy_list = None
        self.power_up_list = None
        self.static_ui_elements_list = None
        self.pliers_dropped = None
        self.bolt_active = None

        self.hit_active = None
        self.hit_cooldown = None
        self.has_hit = None
        self.enemy_auto_spawn = None

        self.key_history = []

        # Load sounds
        self.enemy_hit_sound = arcade.load_sound(config.ENEMY_HIT_SOUND_RESOURCE)
        self.enemy_hit_miss_sound = arcade.load_sound(
            config.ENEMY_HIT_MISS_SOUND_RESOURCE
        )
        self.enemy_hit_punch_sound = arcade.load_sound(
            config.ENEMY_HIT_PUNCH_SOUND_RESOURCE
        )
        self.enemy_hit_gold_punch_sound = arcade.load_sound(
            config.ENEMY_HIT_GOLD_PUNCH_SOUND_RESOURCE
        )
        self.enemy_collision_sound = arcade.load_sound(
            config.ENEMY_COLLISION_SOUND_RESOURCE
        )
        self.game_over_sound = arcade.load_sound(config.GAME_OVER_SOUND_RESOURCE)
        self.game_opening_sound = arcade.load_sound(config.GAME_OPENING_SOUND_RESOURCE)
        self.space_spam_sound = arcade.load_sound(config.SPACE_SPAM_SOUND_RESOURCE)
        self.tooth_collect_sound = arcade.load_sound(
            config.TOOTH_COLLECT_SOUND_RESOURCE
        )
        self.tooth_gold_collect_sound = arcade.load_sound(
            config.TOOTH_GOLD_COLLECT_SOUND_RESOURCE
        )
        self.tooth_drop_sound = arcade.load_sound(config.TOOTH_DROP_SOUND_RESOURCE)
        self.tooth_gold_drop_sound = arcade.load_sound(
            config.TOOTH_GOLD_DROP_SOUND_RESOURCE
        )
        self.item_collect_pliers_sound = arcade.load_sound(
            config.ITEM_COLLECT_PLIERS_SOUND_RESOURCE
        )
        self.item_collect_bolt_sound = arcade.load_sound(
            config.ITEM_COLLECT_BOLT_SOUND_RESOURCE
        )
        self.item_collect_generic_sound = arcade.load_sound(
            config.ITEM_COLLECT_GENERIC_SOUND_RESOURCE
        )
        # self.music_sound = arcade.load_sound(MUSIC_SOUND_SOURCE)

        # Our physics engine
        self.physics_engine = None

        self.camera = arcade.Camera(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        self.ui_camera = arcade.Camera(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        # arcade.play_sound(self.music_sound, 0.1, 0.0, True, 1.0)
        self.score = 0
        self.hit_cooldown = 0
        self.hit_active = 0
        self.has_hit = False
        self.key_history = []

        self.pliers_dropped = False
        self.bolt_active = 0
        self.flask_active = 0
        self.enemy_auto_spawn = 0

        # Marker if gameover
        self.gameover_state = False

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.life_list = arcade.SpriteList()
        self.interior_list = arcade.SpriteList()
        self.static_ui_elements_list = arcade.SpriteList()

        # Walls use spatial hashing for faster collision detection
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.decoration_list = arcade.SpriteList(use_spatial_hash=True)
        self.power_up_list = arcade.SpriteList(use_spatial_hash=True)

        for _ in range(config.CHARACTER_LIFES):
            self.add_life()

        ui_tooth = arcade.Sprite(config.UI_TOOTH_IMAGE_SOURCE, 0.25)
        ui_tooth.center_x = 930
        ui_tooth.center_y = config.UI_HEIGHT - 38
        self.static_ui_elements_list.append(ui_tooth)

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
        for x in range(0, config.SCREEN_WIDTH, 32):
            for y in range(config.UI_HEIGHT, config.SCREEN_HEIGHT, 32):
                floor = arcade.Sprite(config.ROOM_TILE_FLOOR_IMAGE_SOURCE, 0.25)
                floor.center_x = x + 16
                floor.center_y = y
                self.interior_list.append(floor)

        # Create interior
        room_chair = arcade.Sprite(config.ROOM_CHAIR_IMAGE_SOURCE, 0.5)
        self.set_random_sprite_position_no_collisions(room_chair)
        self.decoration_list.append(room_chair)

        room_plant = arcade.Sprite(config.ROOM_PLANT_IMAGE_SOURCE, 0.4)
        self.set_random_sprite_position_no_collisions(room_plant)
        self.decoration_list.append(room_plant)

        room_xray = arcade.Sprite(config.ROOM_XRAY_IMAGE_SOURCE, 0.4)
        self.set_random_sprite_position_no_collisions(room_xray)
        self.decoration_list.append(room_xray)

        room_vending_machine = arcade.Sprite(
            config.ROOM_VENDING_MACHINE_IMAGE_SOURCE, 0.4
        )
        self.set_random_sprite_position_no_collisions(room_vending_machine)
        self.decoration_list.append(room_vending_machine)

        room_water_dispenser = arcade.Sprite(
            config.ROOM_WATER_DISPENSER_IMAGE_SOURCE, 0.4
        )
        self.set_random_sprite_position_no_collisions(room_water_dispenser)
        self.decoration_list.append(room_water_dispenser)

        # Set up the player, specifically placing it at these coordinates.
        image_source = config.CHARACTER_DENTIST_IMAGE_SOURCE
        self.player_sprite = DentistCharacter()
        self.set_random_sprite_position_no_collisions(self.player_sprite)
        self.player_list.append(self.player_sprite)

        for deco in self.decoration_list:
            self.wall_list.append(deco)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.wall_list
        )

    def on_draw(self):
        """Render the screen."""
        self.clear()
        # Code to draw the screen goes here

        self.camera.use()

        self.interior_list.draw()
        self.player_list.draw()
        self.enemy_list.draw()
        self.wall_list.draw()
        self.decoration_list.draw()
        self.power_up_list.draw()

        self.ui_camera.use()

        self.life_list.draw()
        self.static_ui_elements_list.draw()
        arcade.draw_text(
            str(self.score),
            950,
            12,
            arcade.color.BLACK,
            24,
            width=config.SCREEN_WIDTH,
            align="left",
        )

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()
        self.player_list.update_animation()
        self.static_ui_elements_list.update_animation()

        # Check for tooth collections
        power_up_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.power_up_list
        )

        for power_up in power_up_hit_list:
            if isinstance(power_up, HeartSprite):
                self.add_life()
                arcade.play_sound(self.item_collect_generic_sound)
            elif isinstance(power_up, ToothSprite):
                self.on_score(power_up.points)
                arcade.play_sound(self.tooth_collect_sound)
            elif isinstance(power_up, GoldenToothSprite):
                self.on_score(power_up.points)
                arcade.play_sound(self.tooth_gold_collect_sound)
                animation_sprite = ToothAnimation()
                animation_sprite.center_x = power_up.center_x
                animation_sprite.center_y = power_up.center_y
                self.static_ui_elements_list.append(animation_sprite)

            elif isinstance(power_up, PliersSprite):
                self.add_pliers_to_ui()
                self.player_sprite.pliers_equipped = True
                arcade.play_sound(self.item_collect_pliers_sound)
            elif isinstance(power_up, FlaskSprite):
                self.add_flask_to_ui()
                self.flask_active += 500
                self.player_sprite.flask_active = True
                arcade.play_sound(self.item_collect_generic_sound)
            elif isinstance(power_up, BoltSprite):
                self.add_bolt_to_ui()
                self.bolt_active += 500
                self.player_sprite.movement_speed = (
                    config.CHARACTER_MOVEMENT_SPEED * 1.5
                )
                arcade.play_sound(self.item_collect_bolt_sound)
            else:
                raise Exception("Unknown power up type.")
            power_up.remove_from_sprite_lists()

        if self.bolt_active > 0:
            self.bolt_active -= 1
            if self.bolt_active == 0:
                self.player_sprite.movement_speed = config.CHARACTER_MOVEMENT_SPEED
                self.remove_bolt_from_ui()

        if self.flask_active > 0:
            self.flask_active -= 1
            if self.flask_active == 0:
                self.player_sprite.flask_active = False
                self.remove_flask_from_ui()

        # Check for collisions with or hits of enemies
        enemy_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.enemy_list
        )

        self.player_sprite.hit_active = self.hit_active
        if self.player_sprite.is_hitting():
            self.hit_active -= 1
            if self.hit_active == 0:
                if not enemy_hit_list and not self.has_hit:
                    arcade.play_sound(self.enemy_hit_miss_sound)
                self.has_hit = False
            for enemy in enemy_hit_list:
                self.on_enemy_hit(enemy)
                self.has_hit = True
        else:
            for enemy in enemy_hit_list:
                enemy.remove_from_sprite_lists()
                arcade.play_sound(self.enemy_collision_sound)
                self.remove_life()

        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

        self.enemy_move()

        self.add_enemies()
        self.add_hearts()
        self.add_bolts()
        self.add_flasks()
        self.check_game_over()

    def update_player_speed(self):
        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if not self.key_history:
            return

        actions = list(reversed(self.key_history))

        horz = next((x for x in actions if x == "left" or x == "right"), None)
        vert = next((x for x in actions if x == "up" or x == "down"), None)

        if vert == "up":
            self.player_sprite.change_y = self.player_sprite.movement_speed
        elif vert == "down":
            self.player_sprite.change_y = -self.player_sprite.movement_speed

        if horz == "left":
            self.player_sprite.change_x = -self.player_sprite.movement_speed
        elif horz == "right":
            self.player_sprite.change_x = self.player_sprite.movement_speed

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.key_history.append("up")
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.key_history.append("down")
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.key_history.append("left")
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.key_history.append("right")
        elif key == arcade.key.SPACE:
            if self.hit_cooldown > 0:
                arcade.play_sound(self.space_spam_sound)
            else:
                arcade.play_sound(self.enemy_hit_miss_sound)
                self.hit_active = config.CHARACTER_HIT_TIMEOUT + (
                    15 if self.player_sprite.pliers_equipped else 0
                )
            self.hit_cooldown = (
                config.CHARACTER_HIT_TIMEOUT + config.CHARACTER_HIT_TIMEOUT
            )

        self.update_player_speed()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.key_history = list(filter(lambda x: x != "up", self.key_history))
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.key_history = list(filter(lambda x: x != "down", self.key_history))
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.key_history = list(filter(lambda x: x != "left", self.key_history))
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.key_history = list(filter(lambda x: x != "right", self.key_history))

        self.update_player_speed()

    def on_enemy_hit(self, enemy):
        drop_tooth = random.uniform(0, 100)
        if drop_tooth <= config.TOOTH_DROP_CHANCE + (
            25 if self.player_sprite.pliers_equipped else 0
        ):
            self.drop_tooth(enemy)

        arcade.play_sound(self.enemy_hit_sound)

        enemy.remove_from_sprite_lists()

        self.has_hit = True
        self.hit_cooldown = 0

    def on_score(self, score):
        self.score += score

        self.add_pliers()

    def add_pliers_to_ui(self):
        pliers = PliersSprite(0.2)
        pliers.center_x = 900
        pliers.center_y = config.UI_HEIGHT - 40
        self.static_ui_elements_list.append(pliers)

    def add_bolt_to_ui(self):
        bolt = BoltSprite(0.4)
        bolt.center_x = 870
        bolt.center_y = config.UI_HEIGHT - 40
        self.static_ui_elements_list.append(bolt)

    def remove_bolt_from_ui(self):
        items = self.static_ui_elements_list.sprite_list
        self.static_ui_elements_list.clear()
        for item in items:
            if not isinstance(item, BoltSprite):
                self.static_ui_elements_list.append(item)

    def add_flask_to_ui(self):
        flask = FlaskSprite(0.4)
        flask.center_x = 840
        flask.center_y = config.UI_HEIGHT - 40
        self.static_ui_elements_list.append(flask)

    def remove_flask_from_ui(self):
        items = self.static_ui_elements_list.sprite_list
        self.static_ui_elements_list.clear()
        for item in items:
            if not isinstance(item, FlaskSprite):
                self.static_ui_elements_list.append(item)

    def drop_tooth(self, enemy):
        # Drop golden tooth
        drop_golden_tooth = random.uniform(0, 100)
        tooth = None
        if drop_golden_tooth <= config.TOOTH_GOLDEN_DROP_CHANCE + (
            10 if self.player_sprite.pliers_equipped else 0
        ):
            tooth = GoldenToothSprite()
            self.camera.shake(pyglet.math.Vec2(5, 5))
            arcade.play_sound(self.enemy_hit_gold_punch_sound)
            arcade.play_sound(self.tooth_gold_drop_sound)
        else:
            tooth = ToothSprite()
            arcade.play_sound(self.enemy_hit_punch_sound)
            arcade.play_sound(self.tooth_drop_sound)

        self.power_up_list.append(tooth)
        self.position_after_hit(self.player_sprite, enemy, tooth)
        tooth.center_x = min(
            [
                max([tooth.center_x, 32]),
                config.ENEMY_RIGHT_BORDER - 32,
            ]
        )
        tooth.center_y = min([max([tooth.center_y, 128]), config.ENEMY_TOP_BORDER])

    def add_pliers(self):
        if (
            not self.pliers_dropped
            and not self.player_sprite.pliers_equipped
            and random.randint(10, 20) <= self.score
        ):
            self.pliers_dropped = True
            pliers = PliersSprite(0.5)
            self.set_random_sprite_position_no_collisions(pliers)
            self.power_up_list.append(pliers)

    def add_hearts(self):
        if random.randint(1, 1000) == 1:
            self.add_heart()

    def add_heart(self):
        heart = HeartSprite()
        self.set_random_sprite_position_no_collisions(heart)
        self.power_up_list.append(heart)

    def add_bolts(self):
        if random.randint(1, 2000) == 1:
            self.add_bolt()

    def add_bolt(self):
        bolt = BoltSprite()
        self.set_random_sprite_position_no_collisions(bolt)
        self.power_up_list.append(bolt)

    def add_flasks(self):
        if random.randint(1, 3000) == 1:
            self.add_flask()

    def add_flask(self):
        flask = FlaskSprite()
        self.set_random_sprite_position_no_collisions(flask)
        self.power_up_list.append(flask)

    def add_life(self):
        lifes = len(self.life_list.sprite_list)
        life = HeartSprite()
        life.center_x = lifes * 40 + 32
        life.center_y = config.UI_HEIGHT - 40

        self.life_list.append(life)

    def add_enemies(self):
        enemy_count = int(self.score / 5) + 1
        add_enemies = enemy_count - len(self.enemy_list.sprite_list)

        for _ in range(add_enemies):
            self.add_random_enemy()

        if self.enemy_auto_spawn > random.randint(0, 250000):
            self.add_random_enemy()
            self.enemy_auto_spawn = 0
        else:
            self.enemy_auto_spawn += 1

    def add_random_enemy(self):
        enemy_sprite = EnemySprite()
        self.set_enemy_speed(enemy_sprite)

        for _ in range(0, 9):
            enemy_sprite.center_x = self.random_x()
            enemy_sprite.center_y = self.random_y()

            collides_with_other_object = arcade.check_for_collision(
                self.player_sprite, enemy_sprite
            )
            # or arcade.check_for_collision_with_list(enemy_sprite, self.enemy_list)

            if not collides_with_other_object:
                self.enemy_list.append(enemy_sprite)
                return

    def set_enemy_speed(self, enemy):
        enemy.change_x = random.randint(0, config.ENEMY_MAX_SPEED)
        enemy.change_y = random.randint(0, config.ENEMY_MAX_SPEED - enemy.change_x)

    def enemy_move(self):
        for enemy_sprite in self.enemy_list.sprite_list:
            enemy_sprite.center_y += enemy_sprite.change_y
            enemy_sprite.center_x += enemy_sprite.change_x

        for enemy_sprite in self.enemy_list.sprite_list:
            if enemy_sprite.right > config.ENEMY_RIGHT_BORDER:
                enemy_sprite.change_x = -abs(enemy_sprite.change_x)
            elif enemy_sprite.left < config.ENEMY_LEFT_BORDER:
                enemy_sprite.change_x = abs(enemy_sprite.change_x)
            if enemy_sprite.top > config.ENEMY_TOP_BORDER:
                enemy_sprite.change_y = -abs(enemy_sprite.change_y)
            elif enemy_sprite.bottom < config.ENEMY_BOTTOM_BORDER:
                enemy_sprite.change_y = abs(enemy_sprite.change_y)
            else:
                collisions = arcade.check_for_collision_with_list(
                    enemy_sprite, self.decoration_list, 3
                )
                if len(collisions) > 0:
                    enemy_sprite.away_from(collisions[0])

    def remove_life(self):
        if len(self.life_list.sprite_list) > 0:
            life = self.life_list.sprite_list[-1]
            life.remove_from_sprite_lists()

    def check_game_over(self):
        if not self.life_list.sprite_list:
            arcade.play_sound(self.game_over_sound)
            gameover_view = GameOverView(self)
            gameover_view.setup()
            self.window.show_view(gameover_view)

    def set_random_sprite_position_no_collisions(self, sprite):
        for _ in range(0, 99):
            x = self.random_x()
            y = self.random_y()

            sprite.center_x = x
            sprite.center_y = y

            if not arcade.check_for_collision_with_list(sprite, self.decoration_list):
                return

    def random_x(self):
        return random.randint(
            config.ENEMY_LEFT_BORDER + 64, config.ENEMY_RIGHT_BORDER - 64
        )

    def random_y(self):
        return random.randint(
            config.ENEMY_BOTTOM_BORDER + 64, config.ENEMY_TOP_BORDER - 64
        )

    def position_after_hit(self, player, enemy, sprite):
        start_x = player.center_x
        start_y = player.center_y

        dest_x = enemy.center_x
        dest_y = enemy.center_y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        sprite.center_x = enemy.center_x + math.cos(angle) * 128
        sprite.center_y = enemy.center_y + math.sin(angle) * 128


class GameOverView(arcade.View):
    """View to show when game is over"""

    def __init__(self, game_view):
        """This is run once when we switch to this view"""
        super().__init__()
        self.game_view = game_view
        self.score = game_view.score
        self.gameover_time = ScoreBoard().store_score(self.score)

        self.scoreboard_ui_elements_list = None

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, config.SCREEN_WIDTH - 1, 0, config.SCREEN_HEIGHT - 1)

    def setup(self):
        self.scoreboard_ui_elements_list = arcade.SpriteList()
        ui_scoreboard = arcade.Sprite(config.UI_SCOREBOARD_IMAGE_SOURCE, 1.25)
        ui_scoreboard.center_x = config.SCREEN_WIDTH / 2
        ui_scoreboard.center_y = config.SCREEN_HEIGHT / 2 - 48
        self.scoreboard_ui_elements_list.append(ui_scoreboard)

    def on_draw(self):
        """Draw this view"""

        self.clear()

        self.game_view.on_draw()

        ui_scoreboard = arcade.Sprite(config.UI_SCOREBOARD_IMAGE_SOURCE, 1.25)
        ui_scoreboard.center_x = config.SCREEN_WIDTH / 2
        ui_scoreboard.center_y = config.SCREEN_HEIGHT / 2 - 48
        ui_scoreboard.draw()

        text_color = arcade.color.BLACK
        text_color_current = arcade.color.BANANA_YELLOW
        begin_x = config.SCREEN_HEIGHT * 0.75
        font = "Kenney Blocks"
        arcade.draw_text(
            "GAME OVER",
            0,
            begin_x,
            text_color,
            48,
            width=config.SCREEN_WIDTH,
            align="center",
            font_name=font,
        )
        arcade.draw_text(
            f"SCORE: {self.score}",
            0,
            begin_x - 48,
            text_color_current,
            32,
            width=config.SCREEN_WIDTH,
            align="center",
            font_name=font,
        )
        arcade.draw_text(
            "PRESS ENTER TO RESTART",
            0,
            begin_x - 90,
            text_color,
            24,
            width=config.SCREEN_WIDTH,
            align="center",
            font_name=font,
        )

        arcade.draw_text(
            "HIGH SCORES:",
            0,
            begin_x - 140,
            text_color,
            24,
            width=config.SCREEN_WIDTH,
            align="center",
            font_name=font,
        )
        i = 0
        for high_score in ScoreBoard().get_high_scores():
            arcade.draw_text(
                f"{high_score[0]:03}  -  {high_score[1]}",
                0,
                begin_x - 170 - i * 30,
                text_color_current
                if self.gameover_time == high_score[1]
                else text_color,
                24,
                width=config.SCREEN_WIDTH,
                align="center",
                font_name=font,
            )
            i += 1

    def on_key_release(self, key, _modifiers):
        """If the user releases the ENTER key, re-start the game."""
        if key == arcade.key.ENTER:
            self.game_view.setup()
            self.window.show_view(self.game_view)


class InstructionView(arcade.View):
    """View to show instructions before the game"""

    def __init__(self, game_view):
        """This is run once when we switch to this view"""
        super().__init__()

        self.game_view = game_view

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, config.SCREEN_WIDTH - 1, 0, config.SCREEN_HEIGHT - 1)
        self.game_opening_sound = arcade.load_sound(config.GAME_OPENING_SOUND_RESOURCE)
        arcade.play_sound(self.game_opening_sound)

        self.cover_art_list = None

        self.setup()

    def setup(self):
        self.cover_art_list = arcade.SpriteList()

        # Create main title
        main_title = arcade.Sprite(config.SCREEN_MAIN_TITLE_IMAGE_SOURCE, 1)
        main_title.center_x = config.SCREEN_WIDTH / 2
        main_title.center_y = config.SCREEN_HEIGHT - 120
        self.cover_art_list.append(main_title)

    def on_draw(self):
        """Draw this view"""
        self.clear()

        self.game_view.on_draw()

        self.cover_art_list.draw()
        font = "Kenney Blocks"
        text_color = arcade.color.WHITE
        text_start = config.SCREEN_HEIGHT * 0.75
        """arcade.draw_text(
            "DELIRIOUS DENTIST",
            0,
            text_start,
            text_color,
            48,
            width=SCREEN_WIDTH,
            align="center",
            font_name=font,
        )"""
        arcade.draw_text(
            "Press space to perform a root treatment. Collect tooth for your precious roots collection and avoid beeing hit by angry patients",
            0,
            text_start - 90,
            text_color,
            32,
            width=config.SCREEN_WIDTH,
            align="center",
            font_name=font,
        )
        arcade.draw_text(
            "PRESS SPACE TO START THE GAME",
            0,
            text_start - 350,
            text_color,
            24,
            width=config.SCREEN_WIDTH,
            align="center",
            font_name=font,
        )

    def on_key_release(self, key, _modifiers):
        """If the user releases the space key, start the game."""
        if key == arcade.key.SPACE:
            self.window.show_view(self.game_view)


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


class PliersSprite(arcade.Sprite):
    def __init__(self, scale):
        # Set up parent class
        super().__init__()

        self.scale = scale
        self.texture = arcade.load_texture(config.UI_PLIER_IMAGE_SOURCE)


class ToothSprite(arcade.Sprite):
    def __init__(self):
        # Set up parent class
        super().__init__()

        self.scale = 0.5
        self.points = config.TOOTH_POINTS
        self.texture = arcade.load_texture(config.UI_TOOTH_IMAGE_SOURCE)


class GoldenToothSprite(arcade.Sprite):
    def __init__(self):
        # Set up parent class
        super().__init__()

        self.scale = 0.75
        self.points = config.GOLDEN_TOOTH_POINTS
        self.texture = arcade.load_texture(config.UI_GOLDEN_TOOTH_IMAGE_SOURCE)


class HeartSprite(arcade.Sprite):
    def __init__(self):
        # Set up parent class
        super().__init__()

        self.scale = config.TILE_SCALING
        self.texture = arcade.load_texture(config.UI_HEART_IMAGE_SOURCE)


class BoltSprite(arcade.Sprite):
    def __init__(self, scale=config.TILE_SCALING):
        # Set up parent class
        super().__init__()

        self.scale = scale
        self.texture = arcade.load_texture(config.UI_BOLT_IMAGE_SOURCE)


class FlaskSprite(arcade.Sprite):
    def __init__(self, scale=config.TILE_SCALING):
        # Set up parent class
        super().__init__()

        self.scale = scale
        self.texture = arcade.load_texture(config.UI_FLASK_IMAGE_SOURCE)


class DentistCharacter(arcade.Sprite):
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


class ScoreBoard:
    def store_score(self, score):
        timestamp = datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")
        with open(config.HIGH_SCORE_FILE, "a+") as high_score_file:
            high_score_file.write(f"{score},{timestamp}\n")
        return timestamp

    def get_high_scores(self, limit=10):
        with open(config.HIGH_SCORE_FILE, "r+") as high_score_file:
            lines = list(
                reversed(
                    sorted(
                        map(
                            lambda x: [int(x[0]), x[1]],
                            map(
                                lambda x: x.rstrip().split(","),
                                high_score_file.readlines(),
                            ),
                        ),
                        key=itemgetter(0),
                    )
                )
            )
            return lines[0:limit]


class ToothAnimation(GoldenToothSprite):
    def __init__(self):
        # Set up parent class
        super().__init__()
        self.scale = 1

    def update_animation(self, delta_time: float = 1 / 60):
        self.scale *= 1.2
        maximum_scale = 6
        if self.scale >= maximum_scale:
            self.remove_from_sprite_lists()


def main():
    """Main function"""
    window = arcade.Window(
        config.SCREEN_WIDTH, config.SCREEN_HEIGHT, config.SCREEN_TITLE
    )

    game_view = GameView()
    game_view.setup()
    start_view = InstructionView(game_view)
    start_view.setup()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()

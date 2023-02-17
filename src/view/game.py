import math
import random
import arcade
import pyglet

import config

from animation.grow import GrowAnimation
from performance_stats import PerfomanceStats
from room import Room
from sound import Sound
from sprite.dentist import DentistSprite
from sprite.enemy import EnemySprite
from sprite.bolt import BoltSprite
from sprite.flask import FlaskSprite
from sprite.golden_tooth import GoldenToothSprite
from sprite.heart import HeartSprite
from sprite.pliers import PliersSprite
from sprite.tooth import ToothSprite
from ui import UI
from util.direction import DirectionUtil
from util.position import PositionUtil
from view.game_over import GameOverView


class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self, sound):
        # Call the parent class and set up the window
        super().__init__()

        arcade.set_background_color(arcade.csscolor.WHITE_SMOKE)

        self.room = Room()
        self.ui = UI(self)
        self.performance_stats = PerfomanceStats()
        self.score = None
        self.player_list = None
        self.enemy_list = None
        self.power_up_list = None
        self.pliers_dropped = None
        self.bolt_active = None
        self.animation_list = None

        self.hit_active = None
        self.hit_cooldown = None
        self.has_hit = None
        self.enemy_auto_spawn = None

        self.key_history = []

        self.sound = sound

        # Our physics engine
        self.physics_engine = None

        self.camera = arcade.Camera(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        self.ui_camera = arcade.Camera(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        self.room.setup()
        self.ui.setup()

        if config.DEBUG:
            self.performance_stats.setup()
        self.score = 0
        self.hit_cooldown = 0
        self.hit_active = 0
        self.has_hit = False
        self.key_history = []

        self.pliers_dropped = False
        self.bolt_active = 0
        self.flask_active = 0
        self.enemy_auto_spawn = 0

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.animation_list = arcade.SpriteList()

        # Walls use spatial hashing for faster collision detection
        self.power_up_list = arcade.SpriteList(use_spatial_hash=True)

        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite = DentistSprite()
        self.room.set_random_sprite_location_without_decoration_collision(
            self.player_sprite
        )
        self.player_list.append(self.player_sprite)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, [self.room.wall_list, self.room.decoration_list]
        )

    def on_draw(self):
        """Render the screen."""
        self.clear()
        # Code to draw the screen goes here

        self.camera.use()

        self.room.on_draw()
        self.player_list.draw()
        self.enemy_list.draw()
        self.power_up_list.draw()
        self.animation_list.draw()

        self.ui_camera.use()
        self.ui.on_draw()

        if config.DEBUG:
            self.performance_stats.on_draw()

    def on_update(self, delta_time):
        """Movement and game logic"""
        if config.DEBUG:
            self.performance_stats.update(delta_time)

        # Move the player with the physics engine
        self.physics_engine.update()
        self.player_list.update_animation()
        self.animation_list.update_animation()
        self.enemy_list.on_update()

        # Check for tooth collections
        power_up_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.power_up_list
        )

        for power_up in power_up_hit_list:
            if isinstance(power_up, HeartSprite):
                self.ui.add_life()
                arcade.play_sound(self.sound.item_collect_generic_sound)
            elif isinstance(power_up, ToothSprite):
                self.on_score(power_up.points)
                arcade.play_sound(self.sound.tooth_collect_sound)
            elif isinstance(power_up, GoldenToothSprite):
                self.on_score(power_up.points)
                arcade.play_sound(self.sound.tooth_gold_collect_sound)
                animation_sprite = GoldenToothSprite()
                animation_sprite.scale = 1
                GrowAnimation.animate(animation_sprite)
                animation_sprite.center_x = power_up.center_x
                animation_sprite.center_y = power_up.center_y
                self.animation_list.append(animation_sprite)

            elif isinstance(power_up, PliersSprite):
                self.player_sprite.pliers_equipped = True
                arcade.play_sound(self.sound.item_collect_pliers_sound)
            elif isinstance(power_up, FlaskSprite):
                self.flask_active += 500
                self.player_sprite.flask_active = True
                arcade.play_sound(self.sound.item_collect_generic_sound)
            elif isinstance(power_up, BoltSprite):
                self.bolt_active += 500
                self.player_sprite.movement_speed = (
                    config.CHARACTER_MOVEMENT_SPEED * 1.5
                )
                arcade.play_sound(self.sound.item_collect_bolt_sound)
            else:
                raise Exception("Unknown power up type.")
            power_up.remove_from_sprite_lists()

        if self.bolt_active > 0:
            self.bolt_active -= 1
            if self.bolt_active == 0:
                self.player_sprite.movement_speed = config.CHARACTER_MOVEMENT_SPEED

        if self.flask_active > 0:
            self.flask_active -= 1
            if self.flask_active == 0:
                self.player_sprite.flask_active = False

        # Check for collisions with or hits of enemies
        enemy_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.enemy_list
        )

        self.player_sprite.hit_active = self.hit_active
        if self.player_sprite.is_hitting():
            self.hit_active -= 1
            if self.hit_active == 0:
                if not enemy_hit_list and not self.has_hit:
                    arcade.play_sound(self.sound.enemy_hit_miss_sound)
                self.has_hit = False
            for enemy in enemy_hit_list:
                self.on_enemy_hit(enemy)
                self.has_hit = True
        else:
            for enemy in enemy_hit_list:
                enemy.remove_from_sprite_lists()
                arcade.play_sound(self.sound.enemy_collision_sound)
                self.ui.remove_life()

        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

        self.ui.on_update(delta_time)

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
                arcade.play_sound(self.sound.space_spam_sound)
            else:
                arcade.play_sound(self.sound.enemy_hit_miss_sound)
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

        arcade.play_sound(self.sound.enemy_hit_sound)

        enemy.remove_from_sprite_lists()

        self.has_hit = True
        self.hit_cooldown = 0

    def on_score(self, score):
        self.score += score

        self.add_pliers()

    def drop_tooth(self, enemy):
        # Drop golden tooth
        drop_golden_tooth = random.uniform(0, 100)
        tooth = None
        if drop_golden_tooth <= config.TOOTH_GOLDEN_DROP_CHANCE + (
            10 if self.player_sprite.pliers_equipped else 0
        ):
            tooth = GoldenToothSprite()
            self.camera.shake(pyglet.math.Vec2(5, 5))
            arcade.play_sound(self.sound.enemy_hit_gold_punch_sound)
            arcade.play_sound(self.sound.tooth_gold_drop_sound)
        else:
            tooth = ToothSprite()
            arcade.play_sound(self.sound.enemy_hit_punch_sound)
            arcade.play_sound(self.sound.tooth_drop_sound)

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
            self.room.set_random_sprite_location_without_decoration_collision(pliers)
            self.power_up_list.append(pliers)

    def add_hearts(self):
        if random.randint(1, 1000) == 1:
            self.add_heart()

    def add_heart(self):
        heart = HeartSprite()
        self.room.set_random_sprite_location_without_decoration_collision(heart)
        self.power_up_list.append(heart)

    def add_bolts(self):
        if random.randint(1, 2000) == 1:
            self.add_bolt()

    def add_bolt(self):
        bolt = BoltSprite()
        self.room.set_random_sprite_location_without_decoration_collision(bolt)
        self.power_up_list.append(bolt)

    def add_flasks(self):
        if random.randint(1, 3000) == 1:
            self.add_flask()

    def add_flask(self):
        flask = FlaskSprite()
        self.room.set_random_sprite_location_without_decoration_collision(flask)
        self.power_up_list.append(flask)

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
        enemy_sprite = EnemySprite(self.room.decoration_list)

        PositionUtil.set_random_position_without_collision(
            enemy_sprite, self.player_list, self.room.decoration_list
        )

        self.enemy_list.append(enemy_sprite)

    def check_game_over(self):
        if not self.ui.life_list.sprite_list:
            arcade.play_sound(self.sound.game_over_sound)
            gameover_view = GameOverView(self)
            gameover_view.setup()
            self.window.show_view(gameover_view)

    def position_after_hit(self, player, enemy, sprite):
        dest = DirectionUtil.towards(player, enemy)

        sprite.center_x = enemy.center_x + dest[0] * 128
        sprite.center_y = enemy.center_y + dest[0] * 128

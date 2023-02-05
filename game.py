"""
Delirious Dentist
"""
import datetime
import math
from operator import itemgetter
import random
import arcade
import pyglet

VERSION = "0.1"

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
SCREEN_TITLE = f"Delirious Dentist (v{VERSION})"
UI_HEIGHT = 64

# Sprite locations
CHARACTER_DENTIST_IMAGE_SOURCE = "resources/sprites/characters/dentist.png"
CHARACTER_DENTIST_ATTACK_IMAGE_SOURCE = (
    "resources/sprites/characters/dentist_attack.png"
)
CHARACTER_DENTIST_ATTACK_PLIER_IMAGE_SOURCE = (
    "resources/sprites/characters/dentist_attack_plier.png"
)
ENEMY_1_IMAGE_SOURCE = "resources/sprites/characters/enemy_1.png"
ENEMY_2_IMAGE_SOURCE = "resources/sprites/characters/enemy_2.png"
ENEMY_3_IMAGE_SOURCE = "resources/sprites/characters/enemy_3.png"
ROOM_TILE_FLOOR_IMAGE_SOURCE = "resources/sprites/room/tile_floor.png"
ROOM_WINDOW_IMAGE_SOURCE = "resources/sprites/room/window.png"
ROOM_WINDOW_LEFT_IMAGE_SOURCE = "resources/sprites/room/window_left.png"
ROOM_WINDOW_RIGHT_IMAGE_SOURCE = "resources/sprites/room/window_right.png"
ROOM_CHAIR_IMAGE_SOURCE = "resources/sprites/room/chair.png"
ROOM_PLANT_IMAGE_SOURCE = "resources/sprites/room/plant.png"
ROOM_XRAY_IMAGE_SOURCE = "resources/sprites/room/xray.png"
ROOM_VENDING_MACHINE_IMAGE_SOURCE = "resources/sprites/room/vending_machine.png"
ROOM_WATER_DISPENSER_IMAGE_SOURCE = "resources/sprites/room/water_dispenser.png"
UI_HEART_IMAGE_SOURCE = "resources/sprites/ui/heart.png"
UI_TOOTH_IMAGE_SOURCE = "resources/sprites/ui/tooth.png"
UI_GOLDEN_TOOTH_IMAGE_SOURCE = "resources/sprites/ui/golden_tooth.png"
UI_PLIER_IMAGE_SOURCE = "resources/sprites/ui/plier.png"
UI_BOLT_IMAGE_SOURCE = "resources/sprites/ui/bolt.png"
UI_JUGGER_IMAGE_SOURCE = "resources/sprites/ui/jugger.png"
UI_SCOREBOARD_IMAGE_SOURCE = "resources/sprites/ui/scoreboard.png"

# Sounds
ENEMY_HIT_SOUND_RESOURCE = "resources/sounds/hit_nodrop.wav"
ENEMY_HIT_MISS_SOUND_RESOURCE = "resources/sounds/hit_miss.wav"
ENEMY_COLLISION_SOUND_RESOURCE = "resources/sounds/enemy_collision.wav"
GAME_OVER_SOUND_RESOURCE = "resources/sounds/gameover.wav"
GAME_OPENING_SOUND_RESOURCE = "resources/sounds/openingscore.wav"
SPACE_SPAM_SOUND_RESOURCE = "resources/sounds/space_spam.wav"
TOOTH_COLLECT_SOUND_RESOURCE = "resources/sounds/tooth_collect.wav"
TOOTH_GOLD_COLLECT_SOUND_RESOURCE = "resources/sounds/golden_tooth.wav"
TOOTH_DROP_SOUND_RESOURCE = "resources/sounds/tooth_drop.wav"
TOOTH_GOLD_DROP_SOUND_RESOURCE = "resources/sounds/golden_toothdrop.wav"
ITEM_COLLECT_PLIERS_SOUND_RESOURCE = "resources/sounds/pliers.wav"
ITEM_COLLECT_BOLT_SOUND_RESOURCE = "resources/sounds/bolt.wav"
ITEM_COLLECT_GENERIC_SOUND_RESOURCE = "resources/sounds/item_catch.wav"


# movement speed of the dentist character
CHARACTER_MOVEMENT_SPEED = 5
# hit timeout (number of updates after hitting space that you can hit an enemy)
CHARACTER_HIT_TIMEOUT = 20
CHARACTER_HIT_COOLDOWN = 10
CHARACTER_LIFES = 5
# chance for a tooth drop in percent
TOOTH_DROP_CHANCE = 50
TOOTH_GOLDEN_DROP_CHANCE = 10
ENEMY_MAX_SPEED = 5
TOOTH_POINTS = 1
GOLDEN_TOOTH_POINTS = 10

ENEMY_TOP_BORDER = SCREEN_HEIGHT - 64
ENEMY_RIGHT_BORDER = SCREEN_WIDTH
ENEMY_BOTTOM_BORDER = UI_HEIGHT + 64
ENEMY_LEFT_BORDER = 0

# Sprite scalings
CHARACTER_SCALING = 1
TILE_SCALING = 1

HIGH_SCORE_FILE = "delirious-dentist.scores"


class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self, init=False):
        # Call the parent class and set up the window
        super().__init__()

        arcade.set_background_color(arcade.csscolor.WHITE_SMOKE)

        self.init = init
        self.score = None
        self.player_list = None
        self.wall_list = None
        self.decoration_list = None
        self.enemy_list = None
        self.power_up_list = None
        self.static_ui_elements_list = None
        self.pliers_dropped = None

        self.hit_active = None
        self.hit_cooldown = None

        self.key_history = []

        # Load sounds
        self.enemy_hit_sound = arcade.load_sound(ENEMY_HIT_SOUND_RESOURCE)
        self.enemy_hit_miss_sound = arcade.load_sound(ENEMY_HIT_MISS_SOUND_RESOURCE)
        self.enemy_collision_sound = arcade.load_sound(ENEMY_COLLISION_SOUND_RESOURCE)
        self.game_over_sound = arcade.load_sound(GAME_OVER_SOUND_RESOURCE)
        self.game_opening_sound = arcade.load_sound(GAME_OPENING_SOUND_RESOURCE)
        self.space_spam_sound = arcade.load_sound(SPACE_SPAM_SOUND_RESOURCE)
        self.tooth_collect_sound = arcade.load_sound(TOOTH_COLLECT_SOUND_RESOURCE)
        self.tooth_gold_collect_sound = arcade.load_sound(TOOTH_GOLD_COLLECT_SOUND_RESOURCE)
        self.tooth_drop_sound = arcade.load_sound(TOOTH_DROP_SOUND_RESOURCE)
        self.tooth_gold_drop_sound = arcade.load_sound(TOOTH_GOLD_DROP_SOUND_RESOURCE)
        self.item_collect_pliers_sound = arcade.load_sound(ITEM_COLLECT_PLIERS_SOUND_RESOURCE)
        self.item_collect_bolt_sound = arcade.load_sound(ITEM_COLLECT_BOLT_SOUND_RESOURCE)
        self.item_collect_generic_sound = arcade.load_sound(ITEM_COLLECT_GENERIC_SOUND_RESOURCE)

        # Our physics engine
        self.physics_engine = None

        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.ui_camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Marker if gameover
        self.gameover_state = False


    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        self.score = 0
        self.hit_cooldown = 0
        self.hit_active = 0

        self.pliers_dropped = False

        # Marker if gameover
        self.gameover_state = False

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.player_list.draw_hit_boxes()
        self.enemy_list = arcade.SpriteList()
        self.life_list = arcade.SpriteList()
        self.interior_list = arcade.SpriteList()
        self.static_ui_elements_list = arcade.SpriteList()

        # Walls use spatial hashing for faster collision detection
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.decoration_list = arcade.SpriteList(use_spatial_hash=True)
        self.decoration_list.draw_hit_boxes()
        self.power_up_list = arcade.SpriteList(use_spatial_hash=True)

        # Set up the player, specifically placing it at these coordinates.
        image_source = CHARACTER_DENTIST_IMAGE_SOURCE
        self.player_sprite = DentistCharacter()
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 2 * UI_HEIGHT
        self.player_list.append(self.player_sprite)

        for _ in range(CHARACTER_LIFES):
            self.add_life()

        ui_tooth = arcade.Sprite(UI_TOOTH_IMAGE_SOURCE, 0.25)
        ui_tooth.center_x = 930
        ui_tooth.center_y = UI_HEIGHT - 38
        self.static_ui_elements_list.append(ui_tooth)


        # Create walls
        # Create lower boundary
        for x in range(0, SCREEN_WIDTH, 256):
            wall = arcade.Sprite(ROOM_WINDOW_IMAGE_SOURCE, 0.5)
            wall.center_x = x + 128
            wall.center_y = UI_HEIGHT + 16
            self.wall_list.append(wall)

        # Create upper boundary
        for x in range(0, SCREEN_WIDTH, 256):
            wall = arcade.Sprite(ROOM_WINDOW_IMAGE_SOURCE, 0.5)
            wall.center_x = x + 128
            wall.center_y = SCREEN_HEIGHT - 32
            self.wall_list.append(wall)

        # Create left boundary
        for y in range(UI_HEIGHT + 80, SCREEN_HEIGHT, 56):
            wall = arcade.Sprite(ROOM_WINDOW_LEFT_IMAGE_SOURCE, 0.5)
            wall.center_x = 12
            wall.center_y = y
            self.wall_list.append(wall)

        # Create right boundary
        for y in range(UI_HEIGHT + 80, SCREEN_HEIGHT, 56):
            wall = arcade.Sprite(ROOM_WINDOW_RIGHT_IMAGE_SOURCE, 0.5)
            wall.center_x = SCREEN_WIDTH - 12
            wall.center_y = y
            self.wall_list.append(wall)

        # Create the floor
        for x in range(0, SCREEN_WIDTH, 32):
            for y in range(UI_HEIGHT, SCREEN_HEIGHT, 32):
                floor = arcade.Sprite(ROOM_TILE_FLOOR_IMAGE_SOURCE, 0.25)
                floor.center_x = x + 16
                floor.center_y = y
                self.interior_list.append(floor)

        # Create interior
        room_chair = arcade.Sprite(ROOM_CHAIR_IMAGE_SOURCE, 0.5)
        room_chair.center_x = self.random_x()
        room_chair.center_y = self.random_y()
        self.decoration_list.append(room_chair)

        room_plant = arcade.Sprite(ROOM_PLANT_IMAGE_SOURCE, 0.4)
        room_plant.center_x = self.random_x()
        room_plant.center_y = self.random_y()
        self.decoration_list.append(room_plant)

        room_xray = arcade.Sprite(ROOM_XRAY_IMAGE_SOURCE, 0.4)
        room_xray.center_x = self.random_x()
        room_xray.center_y = self.random_y()
        self.decoration_list.append(room_xray)

        room_vending_machine = arcade.Sprite(ROOM_VENDING_MACHINE_IMAGE_SOURCE, 0.4)
        room_vending_machine.center_x = self.random_x()
        room_vending_machine.center_y = self.random_y()
        self.decoration_list.append(room_vending_machine)

        room_water_dispenser = arcade.Sprite(ROOM_WATER_DISPENSER_IMAGE_SOURCE, 0.4)
        room_water_dispenser.center_x = self.random_x()
        room_water_dispenser.center_y = self.random_y()
        self.decoration_list.append(room_water_dispenser)

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
        self.enemy_list.draw_hit_boxes((0, 0, 0, 255), 3)
        self.player_list.draw_hit_boxes((0, 0, 0, 255), 3)
        self.decoration_list.draw_hit_boxes((0, 0, 0, 255), 3)

        self.ui_camera.use()

        self.life_list.draw()
        self.static_ui_elements_list.draw()
        arcade.draw_text(
            str(self.score),
            950,
            12,
            arcade.color.BLACK,
            24,
            width=SCREEN_WIDTH,
            align="left",
        )

        if self.init:
            self.init = False
            self.window.show_view(InstructionView())

        if self.gameover_state == True:
            # Create Scoreboard Background here because of transparency; transparency issues when drawing in GameOverView
            ui_scoreboard = arcade.Sprite(UI_SCOREBOARD_IMAGE_SOURCE, 1.25)
            ui_scoreboard.center_x = SCREEN_WIDTH / 2
            ui_scoreboard.center_y = SCREEN_HEIGHT / 2 - 48
            ui_scoreboard.draw()

            gameover_view = GameOverView(self.score)
            gameover_view.setup()
            self.window.show_view(gameover_view)

        self.check_game_over()

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
                # XXX pliers pickup sound
                self.add_pliers_to_ui()
                self.player_sprite.pliers_equipped = True
                arcade.play_sound(self.item_collect_pliers_sound)
            else:
                raise Exception("Unknown power up type.")
            power_up.remove_from_sprite_lists()

        # Check for collisions with or hits of enemies
        enemy_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.enemy_list
        )

        self.player_sprite.hit_active = self.hit_active
        if self.hit_active:
            self.hit_active -= 1
            for enemy in enemy_hit_list:
                self.on_enemy_hit(enemy)
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
            self.player_sprite.change_y = CHARACTER_MOVEMENT_SPEED
        elif vert == "down":
            self.player_sprite.change_y = -CHARACTER_MOVEMENT_SPEED

        if horz == "left":
            self.player_sprite.change_x = -CHARACTER_MOVEMENT_SPEED
        elif horz == "right":
            self.player_sprite.change_x = CHARACTER_MOVEMENT_SPEED

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
                self.hit_active = CHARACTER_HIT_TIMEOUT + (
                    15 if self.player_sprite.pliers_equipped else 0
                )
            self.hit_cooldown = CHARACTER_HIT_TIMEOUT + CHARACTER_HIT_TIMEOUT

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
        if drop_tooth <= TOOTH_DROP_CHANCE + (
            25 if self.player_sprite.pliers_equipped else 0
        ):
            self.drop_tooth(enemy)
        else:
            arcade.play_sound(self.enemy_hit_sound)
        enemy.remove_from_sprite_lists()
        self.hit_cooldown = 0

    def on_score(self, score):
        self.score += score

        self.add_pliers()

    def add_pliers_to_ui(self):
        pliers = PliersSprite(0.2)
        pliers.center_x = 700
        pliers.center_y = UI_HEIGHT - 40
        self.static_ui_elements_list.append(pliers)

    def drop_tooth(self, enemy):
        # Drop golden tooth
        drop_golden_tooth = random.uniform(0, 100)
        tooth = None
        if drop_golden_tooth <= TOOTH_GOLDEN_DROP_CHANCE + (
            10 if self.player_sprite.pliers_equipped else 0
        ):
            tooth = GoldenToothSprite()
            self.camera.shake(pyglet.math.Vec2(5, 5))
        else:
            tooth = ToothSprite()

        self.power_up_list.append(tooth)
        tooth.center_x = min(
            [
                max([enemy.center_x + random.randint(-64, 64), 32]),
                ENEMY_RIGHT_BORDER - 32,
            ]
        )
        tooth.center_y = min(
            [max([enemy.center_y + random.randint(-64, 64), 128]), ENEMY_TOP_BORDER]
        )

    def add_pliers(self):
        if (
            not self.pliers_dropped
            and not self.player_sprite.pliers_equipped
            and random.randint(10, 20) <= self.score
        ):
            self.pliers_dropped = True
            pliers = PliersSprite(0.5)
            pliers.center_x = self.random_x()
            pliers.center_y = self.random_y()
            self.power_up_list.append(pliers)

    def add_hearts(self):
        if random.randint(1, 1000) == 1:
            self.add_heart()

    def add_heart(self):
        heart = HeartSprite()
        heart.center_x = self.random_x()
        heart.center_y = self.random_y()
        self.power_up_list.append(heart)

    def add_life(self):
        lifes = len(self.life_list.sprite_list)
        life = HeartSprite()
        life.center_x = lifes * 40 + 32
        life.center_y = UI_HEIGHT - 40

        self.life_list.append(life)

    def add_enemies(self):
        enemy_count = int(self.score / 5) + 1
        add_enemies = enemy_count - len(self.enemy_list.sprite_list)

        for _ in range(add_enemies):
            self.add_random_enemy()

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
        enemy.change_x = random.randint(0, ENEMY_MAX_SPEED)
        enemy.change_y = random.randint(0, ENEMY_MAX_SPEED - enemy.change_x)

    def enemy_move(self):
        for enemy_sprite in self.enemy_list.sprite_list:
            enemy_sprite.center_y += enemy_sprite.change_y
            enemy_sprite.center_x += enemy_sprite.change_x

        for enemy_sprite in self.enemy_list.sprite_list:
            if enemy_sprite.right > ENEMY_RIGHT_BORDER:
                enemy_sprite.change_x = -abs(enemy_sprite.change_x)
            elif enemy_sprite.left < ENEMY_LEFT_BORDER:
                enemy_sprite.change_x = abs(enemy_sprite.change_x)
            if enemy_sprite.top > ENEMY_TOP_BORDER:
                enemy_sprite.change_y = -abs(enemy_sprite.change_y)
            elif enemy_sprite.bottom < ENEMY_BOTTOM_BORDER:
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

            #needed to check if it's the last draw before GameOverView, to draw background board for the scoreboard
            self.gameover_state = True


    def random_x(self):
        return random.randint(ENEMY_LEFT_BORDER + 64, ENEMY_RIGHT_BORDER - 64)

    def random_y(self):
        return random.randint(ENEMY_BOTTOM_BORDER + 64, ENEMY_TOP_BORDER - 64)


class GameOverView(arcade.View):
    """View to show when game is over"""

    def __init__(self, score):
        """This is run once when we switch to this view"""
        super().__init__()
        self.score = score
        self.gameover_time = ScoreBoard().store_score(score)

        self.scoreboard_ui_elements_list = None

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def setup(self):

        self.scoreboard_ui_elements_list = arcade.SpriteList()
        ui_scoreboard = arcade.Sprite(UI_SCOREBOARD_IMAGE_SOURCE, 1.25)
        ui_scoreboard.center_x = SCREEN_WIDTH / 2
        ui_scoreboard.center_y = SCREEN_HEIGHT / 2 - 48
        self.scoreboard_ui_elements_list.append(ui_scoreboard)

    def on_draw(self):
        """Draw this view"""
        # DON'T clear here! We want to draw over the endgame screen.
        # self.clear()

        text_color = arcade.color.BLACK
        text_color_current = arcade.color.BANANA_YELLOW
        begin_x = SCREEN_HEIGHT * 0.75
        font = "Kenney Blocks"
        arcade.draw_text(
            "GAME OVER",
            0,
            begin_x,
            text_color,
            48,
            width=SCREEN_WIDTH,
            align="center",
            font_name=font,
        )
        arcade.draw_text(
            f"SCORE: {self.score}",
            0,
            begin_x - 48,
            text_color_current,
            32,
            width=SCREEN_WIDTH,
            align="center",
            font_name=font,
        )
        arcade.draw_text(
            "PRESS ENTER TO RESTART",
            0,
            begin_x - 90,
            text_color,
            24,
            width=SCREEN_WIDTH,
            align="center",
            font_name=font,
        )

        arcade.draw_text(
            "HIGH SCORES:",
            0,
            begin_x - 140,
            text_color,
            24,
            width=SCREEN_WIDTH,
            align="center",
            font_name=font,
        )
        i = 0
        for high_score in ScoreBoard().get_high_scores():
            arcade.draw_text(
                f'{high_score[0]:03}  -  {high_score[1]}',
                0,
                begin_x - 170 - i * 30,
                text_color_current if self.gameover_time == high_score[1] else text_color,
                24,
                width=SCREEN_WIDTH,
                align="center",
                font_name=font,
            )
            i += 1

    def on_key_release(self, key, _modifiers):
        """If the user releases the ENTER key, re-start the game."""
        if key == arcade.key.ENTER:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)


class InstructionView(arcade.View):
    """View to show instructions before the game"""

    def __init__(self):
        """This is run once when we switch to this view"""
        super().__init__()

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
        self.game_opening_sound = arcade.load_sound(GAME_OPENING_SOUND_RESOURCE)
        arcade.play_sound(self.game_opening_sound)

    def on_draw(self):
        """Draw this view"""
        # Don't clear hear. We want to draw over the game view!
        # self.clear()

        font = "Kenney Blocks"
        text_color = arcade.color.WHITE
        text_start = SCREEN_HEIGHT * 0.75
        arcade.draw_text(
            "DELIRIOUS DENTIST",
            0,
            text_start,
            text_color,
            48,
            width=SCREEN_WIDTH,
            align="center",
            font_name=font,
        )
        arcade.draw_text(
            "Press space to perform a root treatment. Collect tooth for your precious roots collection and avoid beeing hit by angry patients",
            0,
            text_start - 90,
            text_color,
            32,
            width=SCREEN_WIDTH,
            align="center",
            font_name=font,
        )
        arcade.draw_text(
            "PRESS SPACE TO START THE GAME",
            0,
            text_start - 350,
            text_color,
            24,
            width=SCREEN_WIDTH,
            align="center",
            font_name=font,
        )

    def on_key_release(self, key, _modifiers):
        """If the user releases the space key, start the game."""
        if key == arcade.key.SPACE:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)


class EnemySprite(arcade.Sprite):
    def __init__(self):
        # Set up parent class
        super().__init__()

        image_sources = [
            ENEMY_1_IMAGE_SOURCE,
            ENEMY_2_IMAGE_SOURCE,
            ENEMY_3_IMAGE_SOURCE,
        ]
        image_source = random.choice(image_sources)
        self.scale = CHARACTER_SCALING
        self.texture = arcade.load_texture(image_source)

    def away_from(self, sprite):
        # Random 1 in 100 chance that we'll change from our old direction and
        # then re-aim toward the player
        start_x = self.center_x
        start_y = self.center_y

        dest_x = sprite.center_x
        dest_y = sprite.center_y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        self.change_x = -1 * math.cos(angle) * ENEMY_MAX_SPEED / 2
        self.change_y = -1 * math.sin(angle) * ENEMY_MAX_SPEED / 2


class PliersSprite(arcade.Sprite):
    def __init__(self, scale):
        # Set up parent class
        super().__init__()

        self.scale = scale
        self.texture = arcade.load_texture(UI_PLIER_IMAGE_SOURCE)


class ToothSprite(arcade.Sprite):
    def __init__(self):
        # Set up parent class
        super().__init__()

        self.scale = 0.5
        self.points = TOOTH_POINTS
        self.texture = arcade.load_texture(UI_TOOTH_IMAGE_SOURCE)


class GoldenToothSprite(arcade.Sprite):
    def __init__(self):
        # Set up parent class
        super().__init__()

        self.scale = 0.75
        self.points = GOLDEN_TOOTH_POINTS
        self.texture = arcade.load_texture(UI_GOLDEN_TOOTH_IMAGE_SOURCE)


class HeartSprite(arcade.Sprite):
    def __init__(self):
        # Set up parent class
        super().__init__()

        self.scale = TILE_SCALING
        self.texture = arcade.load_texture(UI_HEART_IMAGE_SOURCE)


class DentistCharacter(arcade.Sprite):
    def __init__(self):
        # Set up parent class
        super().__init__()

        self.scale = CHARACTER_SCALING
        self.pliers_equipped = False

        # XXX auto set hitbox or adjust coordinates to our sprite
        # self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        # Set up the player, specifically placing it at these coordinates.
        main_image_source = CHARACTER_DENTIST_IMAGE_SOURCE
        hit_image_source = CHARACTER_DENTIST_ATTACK_IMAGE_SOURCE
        pliers_hit_image_source = CHARACTER_DENTIST_ATTACK_PLIER_IMAGE_SOURCE
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

    def update_animation(self, delta_time: float = 1 / 60):
        if self.hit_active:
            self.texture = (
                self.pliers_hit_texture if self.pliers_equipped else self.hit_texture
            )
            self.hit_box = self.hit_hit_box
            return

        self.texture = self.main_texture
        self.hit_box = self.main_hit_box


class ScoreBoard:
    def store_score(self, score):
        timestamp = datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")
        with open(HIGH_SCORE_FILE, "a+") as high_score_file:
            high_score_file.write(f"{score},{timestamp}\n")
        return timestamp

    def get_high_scores(self, limit=10):
        with open(HIGH_SCORE_FILE, "r+") as high_score_file:
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
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = GameView(True)
    start_view.setup()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()

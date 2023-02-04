"""
Delirious Dentist
"""
import random
import arcade

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Delirious Dentist"
UI_HEIGHT = 64

# Sprite locations
CHARACTER_DENTIST_IMAGE_SOURCE = "resources/sprites/characters/dentist.png"
CHARACTER_DENTIST_ATTACK_IMAGE_SOURCE = "resources/sprites/characters/dentist_attack.png"
ENEMY_1_IMAGE_SOURCE = "resources/sprites/characters/enemy_1.png"
ENEMY_2_IMAGE_SOURCE = "resources/sprites/characters/enemy_2.png"
ENEMY_3_IMAGE_SOURCE = "resources/sprites/characters/enemy_3.png"
ROOM_TILE_FLOOR_IMAGE_SOURCE = "resources/sprites/room/tile_floor.png"
ROOM_WINDOW_IMAGE_SOURCE = "resources/sprites/room/wall.png"
ROOM_WINDOW_IMAGE_SOURCE = "resources/sprites/room/window.png"
ROOM_WINDOW_LEFT_IMAGE_SOURCE = "resources/sprites/room/window_left.png"
ROOM_WINDOW_RIGHT_IMAGE_SOURCE = "resources/sprites/room/window_right.png"
ROOM_CHAIR_IMAGE_SOURCE = "resources/sprites/room/chair.png"
UI_HEART_IMAGE_SOURCE = "resources/sprites/ui/heart.png"
UI_TOOTH_IMAGE_SOURCE = "resources/sprites/ui/tooth.png"
UI_GOLDEN_TOOTH_IMAGE_SOURCE = "resources/sprites/ui/golden_tooth.png"

# Sounds
ENEMY_HIT_SOUND_RESOURCE = ":resources:sounds/hit2.wav"
ENEMY_COLLISION_SOUND_RESOURCE = ":resources:sounds/hurt1.wav"
GAME_OVER_SOUND_RESOURCE = ":resources:sounds/gameover1.wav"
TOOTH_COLLECT_SOUND_RESOURCE = ":resources:sounds/coin1.wav"
TOOTH_DROP_SOUND_RESOURCE = ":resources:sounds/laser1.wav"

# movement speed of the dentist character
CHARACTER_MOVEMENT_SPEED = 5
# hit timeout (number of updates after hitting space that you can hit an enemy)
CHARACTER_HIT_TIMEOUT = 20
CHARACTER_HIT_COOLDOWN = 10
CHARACTER_LIFES = 5
# chance for a tooth drop in percent
TOOTH_DROP_CHANCE = 30
TOOTH_GOLDEN_DROP_CHANCE = 10

# Sprite scalings
CHARACTER_SCALING = 1
TILE_SCALING = 1


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
        self.enemy_list = None
        self.tooth_list = None
        self.tooth_gold_list = None
        self.static_ui_elements_list = None

        self.hit_active = None
        self.hit_cooldown = None

        # Load sounds
        self.enemy_hit_sound = arcade.load_sound(ENEMY_HIT_SOUND_RESOURCE)
        self.enemy_collision_sound = arcade.load_sound(
            ENEMY_COLLISION_SOUND_RESOURCE)
        self.game_over_sound = arcade.load_sound(GAME_OVER_SOUND_RESOURCE)
        self.tooth_collect_sound = arcade.load_sound(
            TOOTH_COLLECT_SOUND_RESOURCE)
        self.tooth_drop_sound = arcade.load_sound(
            TOOTH_DROP_SOUND_RESOURCE)

        # Our physics engine
        self.physics_engine = None

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        self.score = 0
        self.hit_cooldown = 0
        self.hit_active = 0

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.life_list = arcade.SpriteList()
        self.interior_list = arcade.SpriteList()
        self.static_ui_elements_list = arcade.SpriteList()

        # Walls use spatial hashing for faster collision detection
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.tooth_list = arcade.SpriteList(use_spatial_hash=True)
        self.tooth_gold_list = arcade.SpriteList(use_spatial_hash=True)

        # Set up the player, specifically placing it at these coordinates.
        image_source = CHARACTER_DENTIST_IMAGE_SOURCE
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 2 * UI_HEIGHT
        self.player_list.append(self.player_sprite)

        for x in range(CHARACTER_LIFES):
            life = arcade.Sprite(UI_HEART_IMAGE_SOURCE, TILE_SCALING)
            life.center_x = x * 40 + 32
            life.center_y = UI_HEIGHT - 32
            self.life_list.append(life)

        ui_tooth = arcade.Sprite(UI_TOOTH_IMAGE_SOURCE, 0.25)
        ui_tooth.center_x = 730
        ui_tooth.center_y = UI_HEIGHT - 32
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

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.wall_list)

        # Create the floor
        for x in range(0, SCREEN_WIDTH, 32):
            for y in range(UI_HEIGHT, SCREEN_HEIGHT, 32):
                floor = arcade.Sprite(ROOM_TILE_FLOOR_IMAGE_SOURCE, 0.25)
                floor.center_x = x + 16
                floor.center_y = y
                self.interior_list.append(floor)

        room_chair = arcade.Sprite(ROOM_CHAIR_IMAGE_SOURCE, 0.5)
        room_chair.center_x = 400
        room_chair.center_y = 400
        self.interior_list.append(room_chair)
    def on_draw(self):
        """Render the screen."""
        self.clear()
        # Code to draw the screen goes here

        self.interior_list.draw()
        self.player_list.draw()
        self.wall_list.draw()
        self.enemy_list.draw()
        self.tooth_list.draw()
        self.tooth_gold_list.draw()
        self.life_list.draw()
        self.static_ui_elements_list.draw()

        arcade.draw_text(str(self.score), 750, 18,
                         arcade.color.BLACK, 24, width=SCREEN_WIDTH, align="left")

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

        # Check for tooth collections
        tooth_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.tooth_list)

        for tooth in tooth_hit_list:
            tooth.remove_from_sprite_lists()
            arcade.play_sound(self.tooth_collect_sound)
            self.score += 1

        # Check for tooth_gold collections
        tooth_gold_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.tooth_gold_list)

        for tooth_gold in tooth_gold_hit_list:
            tooth_gold.remove_from_sprite_lists()
            arcade.play_sound(self.tooth_collect_sound)
            self.score += 10

        # Check for collisions with or hits of enemies
        enemy_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.enemy_list)

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

        self.add_enemies()

        self.enemy_move()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = CHARACTER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -CHARACTER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -CHARACTER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = CHARACTER_MOVEMENT_SPEED
        elif key == arcade.key.SPACE:
            if self.hit_cooldown > 0:
                arcade.play_sound(self.game_over_sound)
            else:
                self.hit_active = CHARACTER_HIT_TIMEOUT
            self.hit_cooldown = CHARACTER_HIT_COOLDOWN + CHARACTER_HIT_TIMEOUT

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_enemy_hit(self, enemy):
        drop_tooth = random.uniform(0, 100)
        if drop_tooth <= TOOTH_DROP_CHANCE:
            self.drop_tooth(enemy)
        else:
            arcade.play_sound(self.enemy_hit_sound)
        enemy.remove_from_sprite_lists()
        self.hit_active = 0
        self.hit_cooldown = 0

    def drop_tooth(self, enemy):
        # Drop golden tooth
        drop_golden_tooth = random.uniform(0, 100)
        if drop_golden_tooth <= TOOTH_GOLDEN_DROP_CHANCE:
            arcade.play_sound(self.tooth_drop_sound)
            tooth = arcade.Sprite(UI_GOLDEN_TOOTH_IMAGE_SOURCE, 0.5)
            tooth.center_x = enemy.center_x + 32  # XXX prevent spawning outside of window
            tooth.center_y = enemy.center_y
            self.tooth_gold_list.append(tooth)

        else:
            arcade.play_sound(self.tooth_drop_sound)
            tooth = arcade.Sprite(UI_TOOTH_IMAGE_SOURCE, 0.5)
            tooth.center_x = enemy.center_x + 32  # XXX prevent spawning outside of window
            tooth.center_y = enemy.center_y
            self.tooth_list.append(tooth)

    def add_enemies(self):
        enemy_count = int(self.score / 5) + 1
        add_enemies = enemy_count - len(self.enemy_list.sprite_list)

        for _ in range(add_enemies):
            self.add_random_enemy()

    def add_random_enemy(self):
        image_sources = [ENEMY_1_IMAGE_SOURCE,
                         ENEMY_2_IMAGE_SOURCE, ENEMY_3_IMAGE_SOURCE]
        enemy_sprite = arcade.Sprite(
            random.choice(image_sources), CHARACTER_SCALING)
        enemy_sprite.center_x = random.randint(64, SCREEN_WIDTH - 64)
        enemy_sprite.center_y = random.randint(
            UI_HEIGHT + 64, SCREEN_HEIGHT - 64)

        collides_with_other_object = arcade.check_for_collision(
            self.player_sprite, enemy_sprite) or arcade.check_for_collision_with_list(enemy_sprite, self.enemy_list)

        if collides_with_other_object:
            self.add_random_enemy()
            return

        self.enemy_list.append(enemy_sprite)


    def enemy_move(self):
        for enemy_sprite in self.enemy_list.sprite_list:
            enemy_sprite.change_y = random.randint(-1, 1)
            enemy_sprite.center_y += enemy_sprite.change_y * 10


    def remove_life(self):
        life = self.life_list.sprite_list[-1]
        life.remove_from_sprite_lists()

        if not self.life_list.sprite_list:
            arcade.play_sound(self.game_over_sound)
            self.window.show_view(GameOverView(self.score))


class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self, score):
        """ This is run once when we switch to this view """
        super().__init__()
        self.score = score
        arcade.set_background_color(arcade.csscolor.BLACK)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_text("GAME OVER", 0, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE_SMOKE, 48, width=SCREEN_WIDTH, align="center")
        arcade.draw_text(f"SCORE: {self.score}", 0, SCREEN_HEIGHT / 2 - 48,
                         arcade.color.WHITE_SMOKE, 24, width=SCREEN_WIDTH, align="center")
        arcade.draw_text("PRESS SPACE TO RESTART", 0, SCREEN_HEIGHT / 2 - 90,
                         arcade.color.WHITE_SMOKE, 14, width=SCREEN_WIDTH, align="center")

    def on_key_release(self, key, _modifiers):
        """ If the user releases the space key, re-start the game. """
        if key == arcade.key.SPACE:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)


class InstructionView(arcade.View):
    """ View to show instructions before the game """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        arcade.set_background_color(arcade.csscolor.BLACK)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_text("DELIRIOUS DENTIST", 0, SCREEN_HEIGHT / 2 + 90,
                         arcade.color.WHITE_SMOKE, 32, width=SCREEN_WIDTH, align="center")
        arcade.draw_text("Press space to perform a root treatment. Collect tooth for your precious roots collection and avoid beeing hit by angry patients", 0, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE_SMOKE, 24, width=SCREEN_WIDTH, align="center")
        arcade.draw_text("PRESS SPACE TO START THE GAME", 0, SCREEN_HEIGHT / 2 - 180,
                         arcade.color.WHITE_SMOKE, 14, width=SCREEN_WIDTH, align="center")

    def on_key_release(self, key, _modifiers):
        """ If the user releases the space key, start the game. """
        if key == arcade.key.SPACE:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)


def main():
    """Main function"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()

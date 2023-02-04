"""
Delirious Dentist
"""
import random
import arcade

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Delirious Dentist"
UI_HEIGHT = 64

# scaling factor for the dentist character
CHARACTER_SCALING = 1
# movement speed of the dentist character
CHARACTER_MOVEMENT_SPEED = 5
# hit timeout (number of updates after hitting space that you can hit an enemy)
CHARACTER_HIT_TIMEOUT = 20


TILE_SCALING = 1


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.player_list = None
        self.wall_list = None
        self.enemy_list = None

        self.hit_active = None

        # Load sounds
        self.enemy_hit_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.enemy_collision_sound = arcade.load_sound(
            ":resources:sounds/coin2.wav")

        # Our physics engine
        self.physics_engine = None

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        """Set up the game here. Call this function to restart the game."""

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.life_list = arcade.SpriteList()

        # Walls use spatial hashing for faster collision detection
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        # Set up the player, specifically placing it at these coordinates.
        image_source = "resources/sprites/dentist.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = UI_HEIGHT
        self.player_list.append(self.player_sprite)

        life_sprite_image_source = ":resources:images/items/star.png"
        for x  in range(5):
            life = arcade.Sprite(life_sprite_image_source, 0.5)
            life.center_x = x * 32 + 32
            life.center_y = UI_HEIGHT - 32
            self.life_list.append(life)


        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, SCREEN_WIDTH + 32, 32):
            wall = arcade.Sprite("resources/sprites/wall.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = UI_HEIGHT
            self.wall_list.append(wall)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.wall_list)

    def on_draw(self):
        """Render the screen."""
        self.clear()
        # Code to draw the screen goes here

        self.player_list.draw()
        self.wall_list.draw()
        self.enemy_list.draw()
        self.life_list.draw()

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

        # Check for collisions with or hits of enemies
        enemy_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.enemy_list)

        if self.hit_active:
            self.hit_active -= 1
            for enemy in enemy_hit_list:
                # XXX add points/tooth roots
                enemy.remove_from_sprite_lists()
                arcade.play_sound(self.enemy_hit_sound)
                self.hit_active = 0
        else:
            for enemy in enemy_hit_list:
                enemy.remove_from_sprite_lists()
                arcade.play_sound(self.enemy_collision_sound)
                self.remove_life();

        self.add_enemies()

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
            self.hit_active = CHARACTER_HIT_TIMEOUT

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

    def add_enemies(self):
        if self.enemy_list.sprite_list:
            # don't add new enemies when there still is one
            return
        # TODO: Prevent spawning over player
        image_source = "resources/sprites/enemy_1.png"
        enemy_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        enemy_sprite.center_x = random.randint(0, SCREEN_WIDTH)
        enemy_sprite.center_y = random.randint(UI_HEIGHT, SCREEN_HEIGHT)
        self.enemy_list.append(enemy_sprite)

    def remove_life(self):
        life = self.life_list.sprite_list[-1]
        life.remove_from_sprite_lists()

        if not self.life_list.sprite_list:
            # XXX GAME OVER SCREEN with highscores!
            raise Exception("GAME OVER!")

def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

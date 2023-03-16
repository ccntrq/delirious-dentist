# Constants
import os
import sys

import version

_IS_BUNDLED = getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")
_RESOURCE_PATH = os.path.join(
    os.path.dirname(__file__), "." if _IS_BUNDLED else "..", "resources"
)

DEBUG = not _IS_BUNDLED

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
SCREEN_TITLE = f"Delirious Dentist (v{version.VERSION})"
UI_HEIGHT = 64


def resource(*paths):
    return os.path.join(_RESOURCE_PATH, *paths)


# Sprite locations
CHARACTER_DENTIST_IMAGE_SOURCE = resource("sprites", "characters", "dentist.png")
CHARACTER_DENTIST_ATTACK_IMAGE_SOURCE = resource(
    "sprites", "characters", "dentist_attack.png"
)
CHARACTER_DENTIST_ATTACK_PLIER_IMAGE_SOURCE = resource(
    "sprites", "characters", "dentist_attack_plier.png"
)
ENEMY_1_IMAGE_SOURCE = resource("sprites", "characters", "enemy_1.png")
ENEMY_2_IMAGE_SOURCE = resource("sprites", "characters", "enemy_2.png")
ENEMY_3_IMAGE_SOURCE = resource("sprites", "characters", "enemy_3.png")
ROOM_TILE_FLOOR_IMAGE_SOURCE = resource("sprites", "room", "tile_floor.png")
ROOM_WINDOW_IMAGE_SOURCE = resource("sprites", "room", "window.png")
ROOM_WINDOW_LEFT_IMAGE_SOURCE = resource("sprites", "room", "window_left.png")
ROOM_WINDOW_RIGHT_IMAGE_SOURCE = resource("sprites", "room", "window_right.png")
ROOM_CHAIR_IMAGE_SOURCE = resource("sprites", "room", "chair.png")
ROOM_PLANT_IMAGE_SOURCE = resource("sprites", "room", "plant.png")
ROOM_XRAY_IMAGE_SOURCE = resource("sprites", "room", "xray.png")
ROOM_VENDING_MACHINE_IMAGE_SOURCE = resource("sprites", "room", "vending_machine.png")
ROOM_WATER_DISPENSER_IMAGE_SOURCE = resource("sprites", "room", "water_dispenser.png")
UI_HEART_IMAGE_SOURCE = resource("sprites", "ui", "heart.png")
UI_TOOTH_IMAGE_SOURCE = resource("sprites", "ui", "tooth.png")
UI_GOLDEN_TOOTH_IMAGE_SOURCE = resource("sprites", "ui", "golden_tooth.png")
UI_PLIER_IMAGE_SOURCE = resource("sprites", "ui", "plier.png")
UI_BOLT_IMAGE_SOURCE = resource("sprites", "ui", "bolt.png")
UI_FLASK_IMAGE_SOURCE = resource("sprites", "ui", "flask.png")
UI_SCOREBOARD_IMAGE_SOURCE = resource("sprites", "ui", "scoreboard.png")

FX_BLOOD_IMAGE_SOURCE_1 = resource("sprites", "fx", "blood1.png")
FX_BLOOD_IMAGE_SOURCE_2 = resource("sprites", "fx", "blood2.png")

SCREEN_MAIN_TITLE_IMAGE_SOURCE = resource("coverart", "main_title.png")

# Sounds
ENEMY_HIT_SOUND_RESOURCE = resource("sounds", "hit_nodrop.wav")
ENEMY_HIT_MISS_SOUND_RESOURCE = resource("sounds", "hit_miss.wav")
ENEMY_HIT_PUNCH_SOUND_RESOURCE = ":resources:sounds/hit3.wav"
ENEMY_HIT_GOLD_PUNCH_SOUND_RESOURCE = ":resources:sounds/hit5.wav"
ENEMY_COLLISION_SOUND_RESOURCE = resource("sounds", "enemy_collision.wav")
GAME_OVER_SOUND_RESOURCE = resource("sounds", "gameover.wav")
GAME_OPENING_SOUND_RESOURCE = resource("sounds", "openingscore.wav")
SPACE_SPAM_SOUND_RESOURCE = resource("sounds", "space_spam.wav")
TOOTH_COLLECT_SOUND_RESOURCE = resource("sounds", "tooth_collect.wav")
TOOTH_GOLD_COLLECT_SOUND_RESOURCE = resource("sounds", "golden_tooth.wav")
TOOTH_DROP_SOUND_RESOURCE = resource("sounds", "tooth_drop.wav")
TOOTH_GOLD_DROP_SOUND_RESOURCE = resource("sounds", "golden_toothdrop.wav")
ITEM_COLLECT_PLIERS_SOUND_RESOURCE = resource("sounds", "pliers.wav")
ITEM_COLLECT_BOLT_SOUND_RESOURCE = resource("sounds", "bolt.wav")
ITEM_COLLECT_GENERIC_SOUND_RESOURCE = resource("sounds", "item_catch.wav")
# MUSIC_SOUND_SOURCE = "resources/sounds/music.wav"


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

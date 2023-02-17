import arcade

import config


class Sound:
    def __init__(self):
        # Load sounds
        self.game_opening_sound = arcade.load_sound(config.GAME_OPENING_SOUND_RESOURCE)
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

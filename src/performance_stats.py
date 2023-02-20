import arcade

import config


class PerfomanceStats:
    def __init__(self):
        self.perf_graph_list = None
        self.frame_count = None

        self.setup()

    def setup(self):
        self.frame_count = 0

    def on_draw(self):
        # Get FPS for the last 60 frames
        text = f"FPS: {arcade.get_fps(60):5.1f}"
        arcade.draw_text(text, 32, config.SCREEN_HEIGHT - 52, arcade.color.BLACK, 22)

    def update(self, delta_time):
        """Update method"""
        self.frame_count += 1

        # Print and clear timings every 60 frames
        if self.frame_count % 60 == 0:
            arcade.print_timings()
            arcade.clear_timings()

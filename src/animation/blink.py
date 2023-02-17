class BlinkAnimation(object):
    def __init__(self, *args, **kwargs):
        super(BlinkAnimation, self).__init__(*args, **kwargs)
        self.items = []

        self.is_blinking = False
        self.since_last_blink = 0
        self.blink_interval = 0.1

    def update_animation(self, delta_time: float = 1 / 60):
        if not self.is_blinking:
            return
        self.since_last_blink += delta_time
        if self.since_last_blink < self.blink_interval:
            return
        self.since_last_blink = 0
        self.visible = not self.visible

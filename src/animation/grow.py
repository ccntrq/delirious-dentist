import types


class GrowAnimation:
    @staticmethod
    def animate(sprite):
        sprite.update_animation = types.MethodType(update_animation, sprite)


def update_animation(self, delta_time: float = 1 / 60):
	# TODO: add parameters for scaling
    self.scale *= 1.2
    maximum_scale = 6
    if self.scale >= maximum_scale:
        self.remove_from_sprite_lists()

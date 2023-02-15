import math


class DirectionUtil:
    @staticmethod
    def towards(start, target):
        x_diff = target.center_x - start.center_x
        y_diff = target.center_y - start.center_y
        angle = math.atan2(y_diff, x_diff)

        return (math.cos(angle), math.sin(angle))

    @staticmethod
    def away_from(start, target):
        return DirectionUtil.towards(target, start)

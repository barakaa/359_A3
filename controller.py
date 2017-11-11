import abc


class Controller(object):
    __metaclass__ = abc.ABCMeta
    RANGE_LOWER = -1
    RANGE_MID = 0
    RANGE_UPPER = 1
    DEAD_ZONE = 0

    def __init__(self):
        Controller.dead_zone = 0

    def translate_range(self, value, old_min, old_max, new_min, new_max):
        old_range = old_max - old_min
        if old_range == 0:
            new_value = new_min
        else:
            new_range = new_max - new_min
            new_value = (((value - old_min) * new_range) / old_range) + new_min
        return new_value

    def format_axis(self, val, bound, u_bound=None):
        if u_bound is None:
            if val < -bound:
                val = -bound
            elif val > bound:
                val = bound
            return round(
                self.translate_range(val, -bound, bound, Controller.RANGE_LOWER, Controller.RANGE_UPPER), 3)
        else:
            if val < bound:
                val = bound
            elif val > u_bound:
                val = u_bound
            return round(
                self.translate_range(val, bound, u_bound, Controller.RANGE_LOWER, Controller.RANGE_UPPER), 3)

    @staticmethod
    def get_dead_zone():
        return Controller.DEAD_ZONE

    @staticmethod
    def set_dead_zone(lower=RANGE_LOWER, upper=RANGE_UPPER, dead_zone_percent=0.15):
        Controller.DEAD_ZONE = ((upper - lower) / 2) * dead_zone_percent

    @abc.abstractmethod
    def click(self):
        raise NotImplementedError("Controller subclass must implement action1()")

    @abc.abstractmethod
    def x_axis(self):
        raise NotImplementedError("Controller subclass must implement x_axis()")

    @abc.abstractmethod
    def y_axis(self):
        raise NotImplementedError("Controller subclass must implement y_axis()")

    @abc.abstractmethod
    def z_axis(self):
        raise NotImplementedError("Controller subclass must implement z_axis()")

    @abc.abstractmethod
    def left(self):
        raise NotImplementedError("Controller subclass must implement left()")

    @abc.abstractmethod
    def right(self):
        raise NotImplementedError("Controller subclass must implement right()")

    @abc.abstractmethod
    def up(self):
        raise NotImplementedError("Controller subclass must implement up()")

    @abc.abstractmethod
    def down(self):
        raise NotImplementedError("Controller subclass must implement down()")

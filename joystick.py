import explorerhat

from controller import *


class Joystick(Controller):
    def __init__(self):
        super(Joystick, self).__init__()
        self.low_volt, self.high_volt = 0, 5
        self.mid_volt = round((self.high_volt - self.low_volt) / 2, 3)
        self.set_dead_zone(self.low_volt, self.high_volt, 0.2)

    def action1(self):
        return explorerhat.input.one.read() == 1

    def x_axis(self):
        one_val = explorerhat.analog.one.read()
        return -self.format_axis(one_val, self.low_volt, self.high_volt)

    def y_axis(self):
        two_val = explorerhat.analog.two.read()
        return -self.format_axis(two_val, self.low_volt, self.high_volt)

    def z_axis(self):
        return Controller.RANGE_MID

    def left(self):
        return explorerhat.analog.one.read() > (self.mid_volt + self.dead_zone)

    def right(self):
        return explorerhat.analog.one.read() < (self.mid_volt - self.dead_zone)

    def up(self):
        return explorerhat.analog.two.read() < (self.mid_volt - self.dead_zone)

    def down(self):
        return explorerhat.analog.two.read() > (self.mid_volt + self.dead_zone)

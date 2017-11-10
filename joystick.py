import explorerhat

from controller import *


class Joystick(Controller):
    def __init__(self):
        super(Joystick, self).__init__()
        self.low_volt, self.high_volt = 0, 5
        self.mid_volt = round((self.high_volt - self.low_volt) / 2, 3)
        Controller.set_dead_zone(self.low_volt, self.high_volt, 0.3)

    def click(self):
        return explorerhat.input.one.read() == 1

    def x_axis(self):
        return -self.format_axis(explorerhat.analog.one.read(), self.low_volt, self.high_volt)

    def y_axis(self):
        return -self.format_axis(explorerhat.analog.two.read(), self.low_volt, self.high_volt)

    def z_axis(self):
        return Controller.RANGE_MID

    def left(self):
        return explorerhat.analog.one.read() > (self.mid_volt + Controller.get_dead_zone())

    def right(self):
        return explorerhat.analog.one.read() < (self.mid_volt - Controller.get_dead_zone())

    def up(self):
        return explorerhat.analog.two.read() < (self.mid_volt - Controller.get_dead_zone())

    def down(self):
        return explorerhat.analog.two.read() > (self.mid_volt + Controller.get_dead_zone())

import explorerhat


class Joystick:
    instance = None

    @staticmethod
    def get_instance():
        if Joystick.instance is None:
            Joystick.instance = Joystick()
        return Joystick.instance

    def button_pressed(self):
        return explorerhat.input.one.read() == 1

    def translate_range(self, value, old_min, old_max, new_min, new_max):
        old_range = old_max - old_min
        if old_range == 0:
            new_value = new_min
        else:
            new_range = new_max - new_min
            new_value = (((value - old_min) * new_range) / old_range) + new_min
        return new_value

    def x_axis(self):
        one_val = explorerhat.analog.one.read()
        return -round(self.translate_range(one_val, 0, 5, -1, 1), 3)

    def y_axis(self):
        return round(explorerhat.analog.two.read(), 1)

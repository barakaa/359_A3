import explorerhat


class Joystick:
    @staticmethod
    def button_pressed():
        return explorerhat.input.one.read() == 1

    @staticmethod
    def translate_range(value, old_min, old_max, new_min, new_max):
        old_range = old_max - old_min
        if old_range == 0:
            new_value = new_min
        else:
            new_range = new_max - new_min
            new_value = (((value - old_min) * new_range) / old_range) + new_min
        return new_value

    @staticmethod
    def x_axis():
        one_val = explorerhat.analog.one.read()
        return -round(Joystick.translate_range(one_val, 0, 5, -1, 1), 3)

    @staticmethod
    def y_axis():
        two_val = explorerhat.analog.two.read()
        return -round(Joystick.translate_range(two_val, 0, 5, -1, 1), 3)

    @staticmethod
    def left():
        return explorerhat.analog.one.read() > 2.7

    @staticmethod
    def right():
        return explorerhat.analog.one.read() < 2.2

    @staticmethod
    def up():
        return explorerhat.analog.two.read() < 2.2

    @staticmethod
    def down():
        return explorerhat.analog.two.read() > 2.7

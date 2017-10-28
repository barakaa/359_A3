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

    def x_axis(self):
        return round(explorerhat.analog.one.read(), 1)

    '''                                                                            TODO: reimplement general case? 
    NOTE: negate it as Riike said
    def translate_range(self, value, left_min, left_max, right_min, right_max):
    left_span = left_max - left_min
    right_span = right_max - right_min
    value_scaled = float(value - left_min) / float(left_span)
    return right_min + (value_scaled + right_span)
    def x_axis(self):
        one_val = explorerhat.analog.one.read()
        return self.translate_range(one_val, 5, 0, 1, -1)
    '''

    def y_axis(self):
        return round(explorerhat.analog.two.read(), 1)

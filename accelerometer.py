from ADXL345 import *
from controller import *
from time import sleep


class Accelerometer(Controller):
    def __init__(self):
        super(Accelerometer, self).__init__()
        self.adxl = None
        self.adxl_range = 256  # value output from ADXL345 accel sensors +/-256 2scomp
        Controller.set_dead_zone()

    def begin(self):
        self.adxl = ADXL345()
        if not self.adxl.begin():  # start ADXL345
            raise RuntimeError("No ADXL345 detected")

    def action1(self):
        '''
        z_vals = []
        pos, neg = False, False
        for i in range(0, 100):
            z_vals.append(self.twos_comp(self.adxl.get_z()))
        # print(z_vals)

        for val in z_vals:
            if val < 0:
                neg = True
            elif val > 0:
                pos = True
        print('p: ', pos, ' n: ', neg)

        return pos and neg
        '''

        z_tap_val = self.adxl.tap_z()
        # print (z_tap_val)
        # return True
        raise NotImplementedError("Accelerometer.action1()")

    def x_axis(self):
        x_val = self.twos_comp(self.adxl.get_x())
        return -self.format_axis(x_val, self.adxl_range)

    def y_axis(self):
        y_val = self.twos_comp(self.adxl.get_y())
        return self.format_axis(y_val, self.adxl_range)

    def z_axis(self):
        z_val = self.twos_comp(self.adxl.get_z())
        return self.format_axis(z_val, self.adxl_range)

    def left(self):
        return self.x_axis() > (Controller.RANGE_MID + Controller.get_dead_zone()) and \
               self.z_axis() < (Controller.RANGE_UPPER - Controller.get_dead_zone())

    def right(self):
        return self.x_axis() < -(Controller.RANGE_MID + Controller.get_dead_zone()) and \
               self.z_axis() < (Controller.RANGE_UPPER - Controller.get_dead_zone())

    def up(self):
        return self.y_axis() < -(Controller.RANGE_MID + Controller.get_dead_zone()) and \
               self.z_axis() < (Controller.RANGE_UPPER - Controller.get_dead_zone())

    def down(self):
        return self.y_axis() > (Controller.RANGE_MID + Controller.get_dead_zone()) and \
               self.z_axis() < (Controller.RANGE_UPPER - Controller.get_dead_zone())


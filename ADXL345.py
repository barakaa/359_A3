import smbus


class ADXL345:
    ADXL345_ADDRESS = 0x53  # Assumes ALT address pin low
    ADXL345_REG_DEVID = 0x00  # Device ID
    ADXL345_REG_POWER_CTL = 0x2D  # Power-saving features control
    ADXL345_REG_DATAX0 = 0x32  # X-axis data 0
    ADXL345_REG_DATAY0 = 0x34  # Y-axis data 0
    ADXL345_REG_DATAZ0 = 0x36  # Z-axis data 0

    def __init__(self):
        self.bus = smbus.SMBus()
        self.BUS_ID = 1
        self.range = 0

    def begin(self):
        # check connection
        device_id = self.read_register(self.ADXL345_REG_DEVID)
        if device_id != 0xE5:
            # No ADXL345 detected ... return false
            print(format(device_id, '02x'))
            return False
        # enable measurements
        self.write_register(self.ADXL345_REG_POWER_CTL, 0x08)
        return True

    def write_register(self, reg, value):
        self.bus.open(self.BUS_ID)
        self.bus.write_byte_data(self.ADXL345_ADDRESS, reg, value)
        self.bus.close()

    def read_register(self, reg):
        self.bus.open(self.BUS_ID)
        reply = self.bus.read_byte_data(self.ADXL345_ADDRESS, reg)
        self.bus.close()
        return reply

    def read_16(self, reg):
        self.bus.open(self.BUS_ID)
        reply = self.bus.read_word_data(self.ADXL345_ADDRESS, reg)
        self.bus.close()
        return reply

    def get_x(self):
        return self.read_16(self.ADXL345_REG_DATAX0)

    def get_y(self):
        return self.read_16(self.ADXL345_REG_DATAY0)

    def get_z(self):
        return self.read_16(self.ADXL345_REG_DATAZ0)

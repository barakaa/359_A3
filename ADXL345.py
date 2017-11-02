import smbus

class ADXL345:
    ADXL345_ADDRESS = 0x53  # Assumes ALT address pin low

    ADXL345_REG_DEVID = 0x00  # Device ID
    ADXL345_REG_THRESH_TAP = 0x1D  # Tap threshold
    ADXL345_REG_OFSX = 0x1E  # X-axis offset
    ADXL345_REG_OFSY = 0x1F  # Y-axis offset
    ADXL345_REG_OFSZ = 0x20  # Z-axis offset
    ADXL345_REG_DUR = 0x21  # Tap duration
    ADXL345_REG_LATENT = 0x22  # Tap latency
    ADXL345_REG_WINDOW = 0x23  # Tap window
    ADXL345_REG_THRESH_ACT = 0x24  # Activity threshold
    ADXL345_REG_THRESH_INACT = 0x25  # Inactivity threshold
    ADXL345_REG_TIME_INACT = 0x26  # Inactivity time
    ADXL345_REG_ACT_INACT_CTL = 0x27  # Axis enable control for activity and inactivity detection
    ADXL345_REG_THRESH_FF = 0x28  # Free-fall threshold
    ADXL345_REG_TIME_FF = 0x29  # Free-fall time
    ADXL345_REG_TAP_AXES = 0x2A  # Axis control for single/double tap
    ADXL345_REG_ACT_TAP_STATUS = 0x2B  # Source for single/double tap
    ADXL345_REG_BW_RATE = 0x2C  # Data rate and power mode control
    ADXL345_REG_POWER_CTL = 0x2D  # Power-saving features control
    ADXL345_REG_INT_ENABLE = 0x2E  # Interrupt enable control
    ADXL345_REG_INT_MAP = 0x2F  # Interrupt mapping control
    ADXL345_REG_INT_SOURCE = 0x30  # Source of interrupts
    ADXL345_REG_DATA_FORMAT = 0x31  # Data format control
    ADXL345_REG_DATAX0 = 0x32  # X-axis data 0
    ADXL345_REG_DATAX1 = 0x33  # X-axis data 1
    ADXL345_REG_DATAY0 = 0x34  # Y-axis data 0
    ADXL345_REG_DATAY1 = 0x35  # Y-axis data 1
    ADXL345_REG_DATAZ0 = 0x36  # Z-axis data 0
    ADXL345_REG_DATAZ1 = 0x37  # Z-axis data 1
    ADXL345_REG_FIFO_CTL = 0x38  # FIFO control
    ADXL345_REG_FIFO_STATUS = 0x39  # FIFO status
    ADXL345_MG2G_MULTIPLIER = 0.004

    GRAVITY = float(9.80665)

    def __init__(self):
        self.bus = smbus.SMBus()
        self.BUS_ID = 1
        self.range = 0

    def begin(self):
        # check connection
        device_id = self.get_device_id()
        if device_id != 0xE5:
            # No ADXL345 detected ... return false
            print(format(device_id, '02x'))
            return False
        # enable measurements
        self.write_register(self.ADXL345_REG_POWER_CTL, 0x08)

        self.write_register(self.ADXL345_REG_THRESH_TAP, 0b01000000)  # 0x20 = 32 = 2g
        self.write_register(self.ADXL345_REG_DUR, 0b00110000)  # 0x20 = 32 = 32ms
        self.write_register(self.ADXL345_REG_TAP_AXES, 0b00000111) # enable tap on X/Y/Z axes

        return True

    #######################################################

    def get_device_id(self):
        return self.read_register(self.ADXL345_REG_DEVID)

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

    #######################################################

    def get_x(self):
        return self.read_16(self.ADXL345_REG_DATAX0)

    def get_y(self):
        return self.read_16(self.ADXL345_REG_DATAY0)

    def get_z(self):
        return self.read_16(self.ADXL345_REG_DATAZ0)

    def tap_z(self):
        val = self.read_register(self.ADXL345_REG_INT_SOURCE)
        print(format(val, '08b'))

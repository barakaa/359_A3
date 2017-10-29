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

    ADXL345_DATARATE_3200_HZ = 0b1111  # 1600Hz Bandwidth   140µA IDD
    ADXL345_DATARATE_1600_HZ = 0b1110  # 800Hz Bandwidth    90µA IDD
    ADXL345_DATARATE_800_HZ = 0b1101  # 400Hz Bandwidth   140µA IDD
    ADXL345_DATARATE_400_HZ = 0b1100  # 200Hz Bandwidth   140µA IDD
    ADXL345_DATARATE_200_HZ = 0b1011  # 100Hz Bandwidth   140µA IDD
    ADXL345_DATARATE_100_HZ = 0b1010  # 50Hz Bandwidth   140µA IDD
    ADXL345_DATARATE_50_HZ = 0b1001  # 25Hz Bandwidth    90µA IDD
    ADXL345_DATARATE_25_HZ = 0b1000  # 12.5Hz Bandwidth    60µA IDD
    ADXL345_DATARATE_12_5_HZ = 0b0111  # 6.25Hz Bandwidth    50µA IDD
    ADXL345_DATARATE_6_25HZ = 0b0110  # 3.13Hz Bandwidth    45µA IDD
    ADXL345_DATARATE_3_13_HZ = 0b0101  # 1.56Hz Bandwidth    40µA IDD
    ADXL345_DATARATE_1_56_HZ = 0b0100  # 0.78Hz Bandwidth    34µA IDD
    ADXL345_DATARATE_0_78_HZ = 0b0011  # 0.39Hz Bandwidth    23µA IDD
    ADXL345_DATARATE_0_39_HZ = 0b0010  # 0.20Hz Bandwidth    23µA IDD
    ADXL345_DATARATE_0_20_HZ = 0b0001  # 0.10Hz Bandwidth    23µA IDD
    ADXL345_DATARATE_0_10_HZ = 0b0000  # 0.05Hz Bandwidth    23µA IDD (default value)

    ADXL345_RANGE_16_G = 0b11  # +/- 16g
    ADXL345_RANGE_8_G = 0b10  # +/- 8g
    ADXL345_RANGE_4_G = 0b01  # +/- 4g
    ADXL345_RANGE_2_G = 0b00  # +/- 2g (default value)

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
        return True

    def set_range(self, range_val):
        range_format = self.read_register(self.ADXL345_REG_DATA_FORMAT)
        range_format &= ~0x0F
        range_format |= range_val

        range_format |= 0x08

        self.write_register(self.ADXL345_REG_DATA_FORMAT, range_format)

        self.range = range_val

    def get_range(self):
        return self.read_register(self.ADXL345_REG_DATA_FORMAT) & 0x03

    def set_data_rate(self, data_rate):
        self.write_register(self.ADXL345_REG_BW_RATE, data_rate)

    def get_data_rate(self):
        return self.read_register(self.ADXL345_REG_BW_RATE) & 0x0F

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

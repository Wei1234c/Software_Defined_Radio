import struct

from universal_serial_bus.orm.usb20 import USBdevice


FREQ_ONE_MHZ = 1000 * 1000



class VendorRequest:
    SET_TRANSCEIVER_MODE = 1
    MAX2837_WRITE = 2
    MAX2837_READ = 3
    SI5351C_WRITE = 4
    SI5351C_READ = 5
    SAMPLE_RATE_SET = 6
    BASEBAND_FILTER_BANDWIDTH_SET = 7
    RFFC5071_WRITE = 8
    RFFC5071_READ = 9
    SPIFLASH_ERASE = 10
    SPIFLASH_WRITE = 11
    SPIFLASH_READ = 12
    CPLD_WRITE = 13
    BOARD_ID_READ = 14
    VERSION_STRING_READ = 15
    SET_FREQ = 16
    AMP_ENABLE = 17
    BOARD_PARTID_SERIALNO_READ = 18
    SET_LNA_GAIN = 19
    SET_VGA_GAIN = 20
    SET_TXVGA_GAIN = 21



class Constants:
    REQUEST_TYPE_OUT = 0x40
    REQUEST_TYPE_IN = 0xC0
    VENDOR_ID = 0x1D50
    PRODUCT_ID = 0x6089
    SUCCESS = 0
    # Python defaults to returning none
    ERROR = None



class TranscieverMode:
    OFF = 0
    RECEIVE = 1
    TRANSMIT = 2



class HackRf(USBdevice):
    VERSIONS = ['Jellybean', 'Jawbreaker', 'HackRF One']


    def __init__(self, vid = Constants.VENDOR_ID, pid = Constants.PRODUCT_ID, address = None):
        super().__init__(vid, pid, address)

        self.max2837 = Max2837(self)
        self.si5351c = SI5351C(self)
        self.rffc5071 = RFFC5071(self)
        board_id = self.get_board_id()
        assert isinstance(board_id, int), 'Invalid board_id: {}'.format(board_id)
        self.name = self.VERSIONS[board_id]
        self.baseband_filter_bandwidth = None
        self.freq_hz = None
        self.lna_gain = None
        self.mode = None


    def get_board_id(self):
        board_id = self.ctrl_transfer(Constants.REQUEST_TYPE_IN, VendorRequest.BOARD_ID_READ, 0, 0, 2)[0]
        assert board_id >= 1, 'Failed to get Board Id'
        return board_id


    def get_version_string(self):
        version = self.ctrl_transfer(Constants.REQUEST_TYPE_IN, VendorRequest.VERSION_STRING_READ, 0, 0, 100)
        assert len(version) > 0, 'Failed to get Version String'
        return version.tobytes().decode()


    def get_board_serial_number(self):
        number = self.ctrl_transfer(Constants.REQUEST_TYPE_IN, VendorRequest.BOARD_PARTID_SERIALNO_READ, 0, 0, 100)
        assert len(number) > 12, 'Failed to get Serial Number'
        # Only get relevant bytes
        serial = number[8:]
        # Get bytes in the right order
        serial.reverse()

        serial_one = serial[12:].tobytes().hex().upper()
        serial_two = serial[8:12].tobytes().hex().upper()
        serial_three = serial[4:8].tobytes().hex().upper()
        serial_four = serial[:4].tobytes().hex().upper()

        return serial_one, serial_two, serial_three, serial_four


    def set_baseband_filter_bandwidth(self, bandwidth_hz):
        """
        Set baseband filter bandwidth in MHz.
            Possible values: 1.75/2.5/3.5/5/5.5/6/7/8/9/10/12/14/15/20/24/28MHz,
            default < sample_rate_hz.
        """
        assert isinstance(bandwidth_hz, int), \
            'Failed to set Baseband Filter Bandwidth, bandwidth_hz should be of type INT or LONG'

        result = self.ctrl_transfer(Constants.REQUEST_TYPE_OUT,
                                    VendorRequest.BASEBAND_FILTER_BANDWIDTH_SET,
                                    bandwidth_hz & 0xffff,
                                    bandwidth_hz >> 16)
        assert result == 0, 'Failed to set Baseband Filter Bandwidth with value [{}]'.format(bandwidth_hz)
        self.baseband_filter_bandwidth = bandwidth_hz
        return Constants.SUCCESS


    def set_frequency(self, freq_hz):
        assert isinstance(freq_hz, int), 'Error setting frequency, value should be of type INT or LONG'

        l_freq_mhz = int(freq_hz / FREQ_ONE_MHZ)
        l_freq_hz = int(freq_hz - (l_freq_mhz * FREQ_ONE_MHZ))
        # For some reason we switch endain from freq to sample
        p = struct.pack('<II', l_freq_mhz, l_freq_hz)
        result = self.ctrl_transfer(Constants.REQUEST_TYPE_OUT, VendorRequest.SET_FREQ, 0, 0, p, len(p))
        assert result == len(p), 'Error setting frequency with value [{}]'.format(freq_hz)
        self.freq_hz = freq_hz
        return Constants.SUCCESS


    def set_sample_rate(self, freq, div):
        assert isinstance(freq, int) and isinstance(div, int), \
            'Error setting Sample Rate, Frequency and Divider should be of type INT or LONG'

        # Make a C struct with the values
        p = struct.pack('>II', freq, div)
        result = self.ctrl_transfer(Constants.REQUEST_TYPE_OUT, VendorRequest.SAMPLE_RATE_SET, 0, 0, p, len(p))
        assert result == len(p), 'Error setting Sample Rate with Frequency [{}] and Divider [{}]'.format(freq, div)
        return Constants.SUCCESS


    def set_lna_gain(self, gain):
        """Sets the LNA gain, in 8db steps, maximum value of 40 """
        assert isinstance(gain, int) and int(gain) <= 40, \
            'Failed to set LNA gain, gain should be of type INT and less than 41'

        result = self.ctrl_transfer(Constants.REQUEST_TYPE_IN, VendorRequest.SET_LNA_GAIN, 0, gain, 1)
        assert result[0] != 1, 'Failed to set LNA gain to [{}]'.format(gain)
        self.lna_gain = gain
        return Constants.SUCCESS


    def set_vga_gain(self, gain):
        """Sets the vga gain, in 2db steps, maximum value of 62 """
        assert isinstance(gain, int) and int(gain) <= 62, 'VGA gain should be of type INT and less than 63'

        result = self.ctrl_transfer(Constants.REQUEST_TYPE_IN, VendorRequest.SET_VGA_GAIN, 0, gain, 1)
        assert result[0] == 1, 'Failed to set VGA gain to [{}]'.format(gain)
        return Constants.SUCCESS


    def set_txvga_gain(self, gain):
        """Sets the txvga gain, in 1db steps, maximum value of 47 """
        assert isinstance(gain, int) and int(gain) <= 47, 'TXVGA gain should be of type INT and ess than 48'

        result = self.ctrl_transfer(Constants.REQUEST_TYPE_IN, VendorRequest.SET_TXVGA_GAIN, 0, gain, 1)
        assert result[0] == 1, 'Failed to set TXVGA gain to [{}]'.format(gain)
        return Constants.SUCCESS


    def enable_amp(self):
        result = self.ctrl_transfer(Constants.REQUEST_TYPE_OUT, VendorRequest.AMP_ENABLE, 1, 0)
        assert result == 0, 'Failed to enable Amp'
        return Constants.SUCCESS


    def disable_amp(self):
        result = self.ctrl_transfer(Constants.REQUEST_TYPE_OUT, VendorRequest.AMP_ENABLE, 0, 0)
        assert result == 0, 'Failed to disable Amp'
        return Constants.SUCCESS


    def set_rx_mode(self):
        """This sets the HackRf in receive mode """
        result = self.ctrl_transfer(Constants.REQUEST_TYPE_OUT,
                                    VendorRequest.SET_TRANSCEIVER_MODE,
                                    TranscieverMode.RECEIVE, 0)
        assert result == 0, 'Failed to set HackRf in Receive Mode'
        self.mode = TranscieverMode.RECEIVE
        return Constants.SUCCESS


    def set_tx_mode(self):
        result = self.ctrl_transfer(Constants.REQUEST_TYPE_OUT,
                                    VendorRequest.SET_TRANSCEIVER_MODE,
                                    TranscieverMode.TRANSMIT, 0)
        assert result == 0, 'Failed to set HackRf in Transmit Mode'
        self.mode = TranscieverMode.TRANSMIT
        return Constants.SUCCESS



class IC:
    REGISTERS_COUNT = 0
    REQUEST_WRITE = 0
    REQUEST_READ = 0


    def __init__(self, hackRf):
        self.hackRf = hackRf


    def write_register(self, register_number, value):
        assert register_number in range(self.REGISTERS_COUNT), 'Invalid Register Number {}'.format(register_number)
        self.hackRf.ctrl_transfer(Constants.REQUEST_TYPE_OUT, self.REQUEST_WRITE, value, register_number)


    def read_register(self, register_number):
        assert register_number in range(self.REGISTERS_COUNT), 'Invalid Register Number {}'.format(register_number)
        return struct.unpack('<H',
                             self.hackRf.ctrl_transfer(Constants.REQUEST_TYPE_IN, self.REQUEST_READ, 0,
                                                       register_number, 2))[0]


    def display_registers(self, count = None):
        count = self.REGISTERS_COUNT if count is None else count
        for register in range(count):
            value = self.read_register(register)
            print("Register {} Value {}".format(register, value))



class Max2837(IC):
    REGISTERS_COUNT = 32
    REQUEST_WRITE = VendorRequest.MAX2837_WRITE
    REQUEST_READ = VendorRequest.MAX2837_READ



class RFFC5071(IC):
    REGISTERS_COUNT = 31
    REQUEST_WRITE = VendorRequest.RFFC5071_WRITE
    REQUEST_READ = VendorRequest.RFFC5071_READ



class SI5351C(IC):
    REGISTERS_COUNT = 255
    REQUEST_WRITE = VendorRequest.SI5351C_WRITE
    REQUEST_READ = VendorRequest.SI5351C_READ


    def read_register(self, register_number):
        assert register_number in range(self.REGISTERS_COUNT), 'Invalid Register Number {}'.format(register_number)
        return self.hackRf.ctrl_transfer(Constants.REQUEST_TYPE_IN, self.REQUEST_READ, 0, register_number, 2)[0]

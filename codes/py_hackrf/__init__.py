import logging
import struct

from universal_serial_bus.orm.usb20 import USBdevice


logging.basicConfig()
logger = logging.getLogger('HackRf')
logger.setLevel(logging.DEBUG)



def byte_array_to_string(array):
    """This is used to convert a array() of bytes into a string """
    return "".join(map(chr, array))



def get_serial(serial_array):
    result = ''
    for byte in serial_array:
        result += '%0.2X' % byte
    return result



def print_bytes(structure):
    print("".join(["/x%02x" % ord(c) for c in structure]))  #



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
    """This is the base object for the HackRf Device, and interaction with it """
    NAME_LIST = ['Jellybean', 'Jawbreaker', 'One']


    def __init__(self, vid = Constants.VENDOR_ID, pid = Constants.PRODUCT_ID, address = None):
        super().__init__(vid, pid, address)

        self.max2837 = Max2837(self)
        self.si5351c = SI5351C(self)
        self.rffc5071 = RFFC5071(self)
        board_id = self.get_board_id()
        assert isinstance(board_id, int), 'Invalid board_id: {}'.format(board_id)
        self.name = self.NAME_LIST[board_id]


    def get_board_id(self):
        """Gets the board's id number """
        board_id = self.ctrl_transfer(
            Constants.REQUEST_TYPE_IN,
            VendorRequest.BOARD_ID_READ,
            0,
            0,
            2)[0]
        if board_id < 1:
            logger.error('Failed to get Board Id')
        else:
            logger.debug('Successfully got Board Id')
            return board_id


    def get_version_string(self):
        """Returns the version string from the hackrf board """
        version = byte_array_to_string(self.ctrl_transfer(
            Constants.REQUEST_TYPE_IN,
            VendorRequest.VERSION_STRING_READ,
            0,
            0,
            100))
        if len(version) < 0:
            logger.error('Failed to get Version String')
        else:
            logger.debug('Successfully got HackRf Version String')
            return version


    def get_board_serial_number(self):
        """Gets the board serial number """
        number = self.ctrl_transfer(
            Constants.REQUEST_TYPE_IN,
            VendorRequest.BOARD_PARTID_SERIALNO_READ,
            0,
            0,
            100)
        if len(number) > 12:
            # Only get relevant bytes
            serial = number[8:]
            # Get bytes in the right order
            serial.reverse()

            serial_one = get_serial(serial[12:])
            serial_two = get_serial(serial[8:12])
            serial_three = get_serial(serial[4:8])
            serial_four = get_serial(serial[:4])
            logger.debug('Successfully got the HackRf Board Serial Number')
            return serial_one, serial_two, serial_three, serial_four
        else:
            logger.error('Failed to get Serial Number')


    def set_baseband_filter_bandwidth(self, bandwidth_hz):
        """
        Set baseband filter bandwidth in MHz.
            Possible values: 1.75/2.5/3.5/5/5.5/6/7/8/9/10/12/14/15/20/24/28MHz,
            default < sample_rate_hz.
        """
        if isinstance(bandwidth_hz, int):
            result = self.ctrl_transfer(Constants.REQUEST_TYPE_OUT,
                                        VendorRequest.BASEBAND_FILTER_BANDWIDTH_SET,
                                        bandwidth_hz & 0xffff,
                                        bandwidth_hz >> 16)
            if result != 0:
                logger.error('Failed to set Baseband Filter Bandwidth with value [%d]', bandwidth_hz)
            else:
                logger.debug('Successfully set Baseband Filter Bandwidth with value [%d]', bandwidth_hz)
                return Constants.SUCCESS
        else:
            logger.error('Failed to set Baseband Filter Bandwidth, bandwidth_hz should be of type INT or LONG')


    def set_frequency(self, freq_hz):
        """Sets the frequency in hz """
        if isinstance(freq_hz, int):
            l_freq_mhz = int(freq_hz / FREQ_ONE_MHZ)
            l_freq_hz = int(freq_hz - (l_freq_mhz * FREQ_ONE_MHZ))

            logger.debug('Frequency [%d] Mhz | [%d] Hz', l_freq_mhz, l_freq_hz)

            # For some reason we switch endain from freq to sample
            p = struct.pack(
                '<II',
                l_freq_mhz,
                l_freq_hz)
            result = self.ctrl_transfer(Constants.REQUEST_TYPE_OUT,
                                        VendorRequest.SET_FREQ,
                                        0,
                                        0,
                                        p,
                                        len(p))
            if result < len(p):
                logger.error('Error setting frequency with value [%d]', freq_hz)
            else:
                logger.debug('Successfully set frequency with value [%d]', freq_hz)
                return Constants.SUCCESS
        else:
            logger.error('Error setting frequency, value should be of type INT or LONG')


    def set_sample_rate(self, freq, div):
        """Sets the sample rate of the hack rf device """
        if isinstance(freq, int) and isinstance(div, int):
            # Make a C struct with the values
            p = struct.pack('>II', freq, div)

            result = self.ctrl_transfer(Constants.REQUEST_TYPE_OUT,
                                        VendorRequest.SAMPLE_RATE_SET,
                                        0,
                                        0,
                                        p,
                                        len(p))
            if result < len(p):
                logger.error('Error setting Sample Rate with Frequency [%d] and Divider [%d]', freq, div)
            else:
                logger.debug('Successfully set Sample Rate with Frequency [%d] and Divider [%d]', freq, div)
                return Constants.SUCCESS
        else:
            logger.error('Error setting Sample Rate, Frequency and Divider should be of type INT or LONG')


    def set_lna_gain(self, gain):
        """Sets the LNA gain, in 8Db steps, maximum value of 40 """
        if isinstance(gain, int):
            if int(gain) <= 40:
                result = self.ctrl_transfer(Constants.REQUEST_TYPE_IN,
                                            VendorRequest.SET_LNA_GAIN,
                                            0,
                                            gain,
                                            1)
                if result[0] != 1:
                    logger.debug('Successfully set LNA gain to [%d]', gain)
                    return Constants.SUCCESS
                else:
                    logger.error('Failed to set LNA gain to [%d]', gain)
            else:
                logger.error('Failed to set LNA gain, value must be less than 41')
        else:
            logger.error('Failed to set LNA gain, gain should be of type INT or LONG')


    def set_vga_gain(self, gain):
        """Sets the vga gain, in 2db steps, maximum value of 62 """
        if isinstance(gain, int):
            if int(gain) <= 62:
                result = self.ctrl_transfer(Constants.REQUEST_TYPE_IN,
                                            VendorRequest.SET_VGA_GAIN,
                                            0,
                                            gain,
                                            1)
                if result[0] == 1:
                    logger.debug('Successfully set VGA gain to [%d]', gain)
                    return Constants.SUCCESS
                else:
                    logger.error('Failed to set VGA gain to [%d]', gain)
            else:
                logger.error('Failed to set VGA gain, value must be less than 63')
        else:
            logger.error('Failed to set VGA gain, gain should be of type INT or LONG')


    def set_txvga_gain(self, gain):
        """Sets the txvga gain, in 1db steps, maximum value of 47 """
        if isinstance(gain, int):
            if int(gain) <= 47:
                result = self.ctrl_transfer(Constants.REQUEST_TYPE_IN,
                                            VendorRequest.SET_TXVGA_GAIN,
                                            0,
                                            gain,
                                            1)
                if result[0] == 1:
                    logger.debug('Successfully set TXVGA gain to [%d]', gain)
                    return Constants.SUCCESS
                else:
                    logger.error('Failed to set TXVGA gain to [%d]', gain)
            else:
                logger.error('Failed to set TXVGA gain, value must be less than 48')
        else:
            logger.error('Failed to set TXVGA gain, gain should be of type INT or LONG')


    def enable_amp(self):
        """Turns on the amp for the hackrf device """
        result = self.ctrl_transfer(Constants.REQUEST_TYPE_OUT,
                                    VendorRequest.AMP_ENABLE,
                                    1,
                                    0)
        if result == 0:
            logger.debug('Successfully enabled Amp')
            return Constants.SUCCESS
        else:
            logger.error('Failed to enable Amp')


    def disable_amp(self):
        """Disable the amp for the hackrf device """
        result = self.ctrl_transfer(Constants.REQUEST_TYPE_OUT,
                                    VendorRequest.AMP_ENABLE,
                                    0,
                                    0)
        if result == 0:
            logger.debug('Successfully disabled Amp')
            return Constants.SUCCESS
        else:
            logger.error('Failed to disable Amp')


    def set_rx_mode(self):
        """This sets the HackRf in receive mode """
        result = self.ctrl_transfer(Constants.REQUEST_TYPE_OUT,
                                    VendorRequest.SET_TRANSCEIVER_MODE,
                                    TranscieverMode.RECEIVE, 0)
        if result == 0:
            logger.debug('Successfully set HackRf in Recieve Mode')
            return Constants.SUCCESS
        else:
            logger.error('Failed to set HackRf in Recieve Mode')


    def set_tx_mode(self):
        """This sets the HackRf in tranfer mode """
        result = self.ctrl_transfer(Constants.REQUEST_TYPE_OUT,
                                    VendorRequest.SET_TRANSCEIVER_MODE,
                                    TranscieverMode.TRANSMIT, 0)
        if result == 0:
            logger.debug('Successfully set HackRf in Transfer Mode')
            return Constants.SUCCESS
        else:
            logger.error('Failed to set HackRf in Transfer Mode')



class IC:
    REGISTERS_COUNT = 0
    REQUEST_WRITE = 0
    REQUEST_READ = 0


    def __init__(self, hackRf):
        self.hackRf = hackRf


    def write_register(self, register_number, value):
        assert register_number in range(self.REGISTERS_COUNT), 'Invalid Register Number {}'.format(register_number)

        self.hackRf.ctrl_transfer(Constants.REQUEST_TYPE_OUT,
                                  self.REQUEST_WRITE,
                                  value,
                                  register_number)


    def read_register(self, register_number):
        assert register_number in range(self.REGISTERS_COUNT), 'Invalid Register Number {}'.format(register_number)
        return struct.unpack('<H',
                             self.hackRf.ctrl_transfer(Constants.REQUEST_TYPE_IN,
                                                       self.REQUEST_READ,
                                                       0,
                                                       register_number,
                                                       2))[0]


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
        return self.hackRf.ctrl_transfer(Constants.REQUEST_TYPE_IN,
                                         self.REQUEST_READ,
                                         0,
                                         register_number,
                                         2)[0]

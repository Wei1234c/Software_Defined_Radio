import unittest

from software_defined_radio.devices.sdr.hackrf import HackRf, Constants



class TestHackRf(unittest.TestCase):

    def setUp(self):
        self.hackrf = HackRf()
        self.assertNotEqual(self.hackrf, None)
        self.assertNotEqual(self.hackrf.name, None)
        self.assertNotEqual(self.hackrf.max2837, None)
        self.assertNotEqual(self.hackrf.si5351c, None)
        self.assertNotEqual(self.hackrf.rffc5071, None)


    def test_get_board_id(self):
        bid = self.hackrf.get_board_id()
        self.assertTrue(bid >= 1)


    def test_get_version_string(self):
        version = self.hackrf.get_version_string()
        self.assertTrue(len(version) > 0)


    def test_get_board_serial_number(self):
        result = self.hackrf.get_board_serial_number()
        self.assertTrue(len(result) == 4)


    def test_set_baseband_filter_bandwidth(self):
        result = self.hackrf.set_baseband_filter_bandwidth(500000)
        self.assertTrue(result == Constants.SUCCESS)


    def test_set_frequency(self):
        result = self.hackrf.set_frequency(10000000)
        self.assertTrue(result == Constants.SUCCESS)


    def test_set_sample_rate(self):
        result = self.hackrf.set_sample_rate(10000000, 1)
        self.assertTrue(result == Constants.SUCCESS)


    def test_set_lna_gain(self):
        result = self.hackrf.set_lna_gain(14)
        self.assertTrue(result == Constants.SUCCESS)


    def test_set_vga_gain(self):
        result = self.hackrf.set_vga_gain(42)
        self.assertTrue(result == Constants.SUCCESS)


    def test_set_txvga_gain(self):
        result = self.hackrf.set_txvga_gain(14)
        self.assertTrue(result == Constants.SUCCESS)


    def test_disable_amp(self):
        result = self.hackrf.disable_amp()
        self.assertTrue(result == Constants.SUCCESS)


    def test_enable_amp(self):
        result = self.hackrf.enable_amp()
        self.assertTrue(result == Constants.SUCCESS)


    def test_set_rx_mode(self):
        result = self.hackrf.set_rx_mode()
        self.assertTrue(result == Constants.SUCCESS)


    def test_set_tx_mode(self):
        result = self.hackrf.set_tx_mode()
        self.assertTrue(result == Constants.SUCCESS)

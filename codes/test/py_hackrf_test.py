import unittest

from software_defined_radio.devices.hackrf.py_hackrf.test import TestHackRf


suite = unittest.TestLoader().loadTestsFromTestCase(TestHackRf)
unittest.TextTestRunner(verbosity = 2).run(suite)

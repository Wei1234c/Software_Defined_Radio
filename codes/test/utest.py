import unittest

from py_hackrf.test import TestHackRf


suite = unittest.TestLoader().loadTestsFromTestCase(TestHackRf)
unittest.TextTestRunner(verbosity = 2).run(suite)

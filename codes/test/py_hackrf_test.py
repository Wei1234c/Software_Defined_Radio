# suite = unittest.TestLoader().loadTestsFromTestCase(TestHackRf)
# unittest.TextTestRunner(verbosity = 2).run(suite)
import pyximport
pyximport.install()

from software_defined_radio.devices.sdr.hackrf import HackRf


# with HackRf() as hackrf:
#     print(hackrf.get_board_id())


hackrf = HackRf()
print(hackrf.get_board_id())

hackrf.close()

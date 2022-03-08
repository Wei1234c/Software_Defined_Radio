# import pyximport
#
#
# pyximport.install()

from urh.dev.native.lib import hackrf

from urh.dev.native.HackRF import HackRF
hfc = HackRF(433.92e6, 1e6, 1e6, 20)
hfc.start_rx_mode()
#
# from urh.dev.native.RTLSDR import RTLSDR
# rtlsdr = RTLSDR(433.92e6, 20, 2e6, device_number=0)
# rtlsdr.start_rx_mode()

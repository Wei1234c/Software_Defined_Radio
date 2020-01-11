import pyximport
pyximport.install()

from urh.dev.native.lib import hackrf
from urh.dev.native.lib import rtlsdr
from urh.dev.native.lib import airspy
from urh.dev.native.lib import usrp

from urh.dev.native.HackRF import HackRF
from urh.dev.native.RTLSDR import RTLSDR

hfc = HackRF(433.92e6, 1e6, 1e6, 20)
hfc.start_rx_mode()

rtlsdr_class = RTLSDR(433.92e6, 20, 2e6, device_number=0)
rtlsdr_class.start_rx_mode()
print(rtlsdr.get_device_list())
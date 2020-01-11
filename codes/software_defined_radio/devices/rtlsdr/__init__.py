from universal_serial_bus.orm.usb20 import USBdevice
from . import interface



class rtlsdr(USBdevice, interface.rtlsdr):
    pass

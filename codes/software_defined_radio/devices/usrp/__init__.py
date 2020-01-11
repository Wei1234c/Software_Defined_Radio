from universal_serial_bus.orm.usb20 import USBdevice
from . import interface



class usrp(USBdevice, interface.usrp):
    pass

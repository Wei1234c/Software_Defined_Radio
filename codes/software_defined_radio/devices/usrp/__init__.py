from universal_serial_bus.orm.usb20 import USBdevice
from . import interface



class usrp(USBdevice, interface.usrp):

    def close(*args, **kwargs):
        pass


    def destroy_stream(*args, **kwargs):
        pass


    def find_devices(*args, **kwargs):
        pass


    def get_antenna(*args, **kwargs):
        pass


    def get_antennas(*args, **kwargs):
        pass


    def get_device_representation(*args, **kwargs):
        pass


    def get_last_error(*args, **kwargs):
        pass


    def open(*args, **kwargs):
        pass


    def recv_stream(*args, **kwargs):
        pass


    def send_stream(*args, **kwargs):
        pass


    def setup_stream(*args, **kwargs):
        pass


    def set_antenna(*args, **kwargs):
        pass


    def set_bandwidth(*args, **kwargs):
        pass


    def set_center_freq(*args, **kwargs):
        pass


    def set_channel(*args, **kwargs):
        pass


    def set_rf_gain(*args, **kwargs):
        """
        Normalized gain must be between 0 and 1
            :param normalized_gain:
            :return:
        """
        pass


    def set_sample_rate(*args, **kwargs):
        pass


    def set_subdevice(*args, **kwargs):
        pass


    def set_tx(*args, **kwargs):
        pass


    def start_stream(*args, **kwargs):
        pass


    def stop_stream(*args, **kwargs):
        pass

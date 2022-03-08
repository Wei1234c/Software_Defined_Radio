from universal_serial_bus.orm.usb20 import USBdevice
from . import interface



class usrp(USBdevice, interface.usrp):

    @staticmethod
    def close(*args, **kwargs):
        raise NotImplementedError()


    @staticmethod
    def destroy_stream(*args, **kwargs):
        raise NotImplementedError()


    @staticmethod
    def find_devices(*args, **kwargs):
        raise NotImplementedError()


    @staticmethod
    def get_antenna(*args, **kwargs):
        raise NotImplementedError()


    @staticmethod
    def get_antennas(*args, **kwargs):
        raise NotImplementedError()


    @staticmethod
    def get_device_representation(*args, **kwargs):
        raise NotImplementedError()


    @staticmethod
    def get_last_error(*args, **kwargs):
        raise NotImplementedError()


    @staticmethod
    def open(*args, **kwargs):
        raise NotImplementedError()


    @staticmethod
    def recv_stream(*args, **kwargs):
        raise NotImplementedError()


    @staticmethod
    def send_stream(*args, **kwargs):
        raise NotImplementedError()


    @staticmethod
    def setup_stream(*args, **kwargs):
        raise NotImplementedError()


    @staticmethod
    def set_antenna(*args, **kwargs):
        raise NotImplementedError()


    @staticmethod
    def set_bandwidth(*args, **kwargs):
        raise NotImplementedError()


    @staticmethod
    def set_center_freq(*args, **kwargs):
        raise NotImplementedError()


    @staticmethod
    def set_channel(*args, **kwargs):
        raise NotImplementedError()


    @staticmethod
    def set_rf_gain(*args, **kwargs):
        """
        Normalized gain must be between 0 and 1
            :param normalized_gain:
            :return:
        """
        raise NotImplementedError()


    @staticmethod
    def set_sample_rate(*args, **kwargs):
        raise NotImplementedError()


    @staticmethod
    def set_subdevice(*args, **kwargs):
        raise NotImplementedError()


    @staticmethod
    def set_tx(*args, **kwargs):
        raise NotImplementedError()


    @staticmethod
    def start_stream(*args, **kwargs):
        raise NotImplementedError()


    @staticmethod
    def stop_stream(*args, **kwargs):
        raise NotImplementedError()

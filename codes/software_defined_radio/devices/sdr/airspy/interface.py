# from urh.dev.native.lib import airspy

class airspy:

    def close(*args, **kwargs):
        pass


    def error_name(*args, **kwargs):
        pass


    def get_sample_rates(*args, **kwargs):
        pass


    def open(*args, **kwargs):
        pass


    def open_by_serial(*args, **kwargs):
        pass


    def set_baseband_gain(*args, **kwargs):
        """ Shall be between 0 and 15 """
        pass


    def set_center_frequency(*args, **kwargs):
        """ Parameter freq_hz shall be between 24000000(24MHz) and 1750000000(1.75GHz) """
        pass


    def set_if_rx_gain(*args, **kwargs):
        """ Shall be between 0 and 15 """
        pass


    def set_rf_gain(*args, **kwargs):
        """ Shall be between 0 and 15 """
        pass


    def set_sample_rate(*args, **kwargs):
        """ Parameter samplerate can be either the index of a samplerate or directly its value in Hz within the list """
        pass


    def start_rx(*args, **kwargs):
        pass


    def stop_rx(*args, **kwargs):
        pass

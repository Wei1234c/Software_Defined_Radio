# from urh.dev.native.lib import hackrf


class hackrf:

    def board_id_read(*args, **kwargs):
        pass


    def close(*args, **kwargs):
        pass


    def exit(*args, **kwargs):
        pass


    def get_device_list(*args, **kwargs):
        pass


    def has_multi_device_support(*args, **kwargs):
        pass


    def init(*args, **kwargs):
        pass


    def is_streaming(*args, **kwargs):
        pass


    def open(*args, **kwargs):
        pass


    def setup(*args, **kwargs):
        """
        Convenience method for init + open. This one is used by HackRF class.
            :return:
        """
        pass


    def set_amp_enable(*args, **kwargs):
        pass


    def set_baseband_filter_bandwidth(*args, **kwargs):
        pass


    def set_baseband_gain(*args, **kwargs):
        """ Sets the vga gain, in 2db steps, maximum value of 62 """
        pass


    def set_freq(*args, **kwargs):
        pass


    def set_if_rx_gain(*args, **kwargs):
        """ Sets the LNA gain, in 8Db steps, maximum value of 40 """
        pass


    def set_if_tx_gain(*args, **kwargs):
        """ Sets the txvga gain, in 1db steps, maximum value of 47 """
        pass


    def set_rf_gain(*args, **kwargs):
        """ Enable or disable RF amplifier """
        pass


    def set_sample_rate(*args, **kwargs):
        pass


    def start_rx_mode(*args, **kwargs):
        pass


    def start_tx_mode(*args, **kwargs):
        pass


    def stop_rx_mode(*args, **kwargs):
        pass


    def stop_tx_mode(*args, **kwargs):
        pass


    def version_string_read(*args, **kwargs):
        pass

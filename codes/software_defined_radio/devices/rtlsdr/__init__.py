from universal_serial_bus.orm.usb20 import USBdevice
from . import interface



class rtlsdr(USBdevice, interface.rtlsdr):

    def bandwidth_is_adjustable(*args, **kwargs):
        pass


    def cancel_async(*args, **kwargs):
        """
        Cancel all pending asynchronous operations on the device.

            :return: 0 on success
        """
        pass


    def close(*args, **kwargs):
        pass


    def get_center_freq(*args, **kwargs):
        """
        Get actual frequency the device is tuned to.

            :return: 0 on error, frequency in Hz otherwise
        """
        pass


    def get_device_count(*args, **kwargs):
        pass


    def get_device_list(*args, **kwargs):
        pass


    def get_device_name(*args, **kwargs):
        pass


    def get_device_usb_strings(*args, **kwargs):
        """
        :param index: index of the device
            :return: manufacturer name, product name, serial serial number on success else None, None, None
        """
        pass


    def get_direct_sampling(*args, **kwargs):
        """
        Get state of the direct sampling mode

            :return: -1 on error, 0 means disabled, 1 I-ADC input enabled, 2 Q-ADC input enabled
        """
        pass


    def get_freq_correction(*args, **kwargs):
        """
        Get actual frequency correction value of the device.

            :return: correction value in parts per million (ppm)
        """
        pass


    def get_index_by_serial(*args, **kwargs):
        """
        Get device index by USB serial string descriptor.

            :param serial: serial string of the device
            :return: device index of first device where the name matched
                     -1 if name is NULL
                     -2 if no devices were found at all
                     -3 if devices were found, but none with matching name
        """
        pass


    def get_offset_tuning(*args, **kwargs):
        """
        Get state of the offset tuning mode

            :return: -1 on error, 0 means disabled, 1 enabled
        """
        pass


    def get_sample_rate(*args, **kwargs):
        """
        Get actual sample rate the device is configured to.
            :return: 0 on error, sample rate in Hz otherwise
        """
        pass


    def get_tuner_gain(*args, **kwargs):
        """
        Get actual gain the device is configured to.

            :return: 0 on error, gain in tenths of a dB, 115 means 11.5 dB.
        """
        pass


    def get_tuner_gains(*args, **kwargs):
        """
        Get a list of gains supported by the tuner.
            NOTE: The gains argument must be preallocated by the caller. If NULL is
            being given instead, the number of available gain values will be returned.

            :return: gains array of gain values. In tenths of a dB, 115 means 11.5 dB.
        """
        pass


    def get_tuner_type(*args, **kwargs):
        """
        Get the tuner type.

            :return: RTLSDR_TUNER_UNKNOWN on error, tuner type otherwise
        """
        pass


    def get_usb_strings(*args, **kwargs):
        pass


    def get_xtal_freq(*args, **kwargs):
        """
        Get crystal oscillator frequencies used for the RTL2832 and the tuner IC.
            Usually both ICs use the same clock.

            :return: rtl_freq frequency value used to clock the RTL2832 in Hz,
                     tuner_freq frequency value used to clock the tuner IC in Hz
        """
        pass


    def open(*args, **kwargs):
        pass


    def read_async(*args, **kwargs):
        """
        Read samples from the device asynchronously. This function will block until
            it is being canceled using rtlsdr_cancel_async()
            read_bytes_async
            :return: 0 on success
        """
        pass


    def read_sync(*args, **kwargs):
        """
        The raw, captured IQ data is 8 bit unsigned data.

            :return:
        """
        pass


    def reset_buffer(*args, **kwargs):
        pass


    def set_agc_mode(*args, **kwargs):
        """
        Enable or disable the internal digital Automatic Gain Control of the RTL2832.

            :param on: digital AGC mode, 1 means enabled, 0 disabled
            :return: 0 on success
        """
        pass


    def set_center_freq(*args, **kwargs):
        pass


    def set_direct_sampling(*args, **kwargs):
        """
        Enable or disable the direct sampling mode. When enabled, the IF mode
            of the RTL2832 is activated, and rtlsdr_set_center_freq() will control
            the IF-frequency of the DDC, which can be used to tune from 0 to 28.8 MHz
            (xtal frequency of the RTL2832).

            :param on: 0 means disabled, 1 I-ADC input enabled, 2 Q-ADC input enabled
            :return: 0 on success
        """
        pass


    def set_freq_correction(*args, **kwargs):
        """
        Set the frequency correction value for the device.

            :param ppm: ppm correction value in parts per million (ppm)
            :return: 0 on success
        """
        pass


    def set_offset_tuning(*args, **kwargs):
        """
        Enable or disable offset tuning for zero-IF tuners, which allows to avoid
            problems caused by the DC offset of the ADCs and 1/f noise.

            :param on: 0 means disabled, 1 enabled
            :return: 0 on success
        """
        pass


    def set_sample_rate(*args, **kwargs):
        """
        Set the sample rate for the device, also selects the baseband filters
            according to the requested sample rate for tuners where this is possible.

            :param sample_rate: the sample rate to be set, possible values are:
                        225001 - 300000 Hz
                        900001 - 3200000 Hz
                        sample loss is to be expected for rates > 2400000
            :return:
        """
        pass


    def set_tuner_bandwidth(*args, **kwargs):
        """
        Set the bandwidth for the device.

                :param bw: bandwidth in Hz. Zero means automatic BW selection.
                :return 0 on success
        """
        pass


    def set_tuner_gain(*args, **kwargs):
        """
        Set the gain for the device.
            Manual gain mode must be enabled for this to work.

            Valid gain values (in tenths of a dB) for the E4000 tuner:
            -10, 15, 40, 65, 90, 115, 140, 165, 190,
            215, 240, 290, 340, 420, 430, 450, 470, 490

            Valid gain values may be queried with rtlsdr_get_tuner_gains function.

            :param gain: gain in tenths of a dB, 115 means 11.5 dB.
            :return: 0 on success
        """
        pass


    def set_tuner_gain_mode(*args, **kwargs):
        """
        Set the gain mode (automatic/manual) for the device.
            Manual gain mode must be enabled for the gain setter function to work.

            :param manual: 1 means manual gain mode shall be enabled.
            :return: 0 on success
        """
        pass


    def set_tuner_if_gain(*args, **kwargs):
        """
        Set the intermediate frequency gain for the device.

            :param stage: intermediate frequency gain stage number (1 to 6 for E4000)
            :param gain: in tenths of a dB, -30 means -3.0 dB.
            :return: 0 on success
        """
        pass


    def set_xtal_freq(*args, **kwargs):
        """
        Set crystal oscillator frequencies used for the RTL2832 and the tuner IC.

            Usually both ICs use the same clock. Changing the clock may make sense if
            you are applying an external clock to the tuner or to compensate the
            frequency (and samplerate) error caused by the original (cheap) crystal.

            NOTE: Call this function only if you fully understand the implications.

            :param rtl_freq: frequency value used to clock the RTL2832 in Hz
            :param tuner_freq: frequency value used to clock the tuner IC in Hz
            :return: 0 on success
        """
        pass

import struct


class NasaSignal(object):
    def __init__(self):
        self.header = None
        self.value = None

    def serialize(self):
        value_type = (self.header & 0x0F00) >> 8

        if value_type == 0 or value_type == 1:
            return struct.pack('>HB', self.header, self.value)
        elif value_type == 2:
            return struct.pack('>HH', self.header, self.value)
        # elif value_type == 4:
        #     return struct.pack('>HH', self.header, self.value)
        else:
            raise Exception('Unknown data type')

    def get_is_state(self):
        return (self.header & 0x8000) > 0

    def get_is_command(self):
        return (self.header & 0x4000) > 0

    def get_data_type(self):
        return (self.header & 0x0F00) >> 8

    def get_signal(self):
        return self.header & 0x0FFF

    is_state = property(get_is_state)
    is_command = property(get_is_command)
    data_type = property(get_data_type)
    signal = property(get_signal)

    def deserialize(buf, offset):
        signal = NasaSignal()
        signal.header = (buf[offset] << 8) | buf[offset + 1]
        offset += 2

        if signal.data_type == 0 or signal.data_type == 1:
            signal.value = buf[offset]
            offset += 1
        elif signal.data_type == 2:
            signal.value = (buf[offset] << 8) | buf[offset + 1]
            offset += 2
        elif signal.data_type == 4:
            signal.value = 0

            for i in range(8):
                signal.value <<= 8
                signal.value |= buf[offset]
                offset += 1
        elif signal.data_type == 6:
            signal.value = bytes(buf[offset:offset + 20])
            offset += 20

        else:
            raise Exception(f'unknown data type, data type = {signal.data_type}')

        return signal, offset

    def __repr__(self):
        repr = f'{self.signal :02X} = {self.value}'
        return repr

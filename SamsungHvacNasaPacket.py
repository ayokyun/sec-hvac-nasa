import struct
from enum import IntEnum

import crc

from NasaSignal import NasaSignal


class SamsungHvacNasaPacket(object):
    start = 0x32
    end = 0x34

    class PacketType(IntEnum):
        Control = 0xC013
        Report = 0xC014
        Ack = 0xC016

    def __init__(self):
        self.length = None
        self.source = None
        self.destination = None
        self.packetType = None
        self.sequence = None
        self.numOfSignals = None
        self.signals = None
        self.checksum = None  # XMODEM

        crc_configuration = crc.Configuration(width=16, polynomial=0x1021, init_value=0x0000, reverse_input=False,
                                              reverse_output=False, final_xor_value=0x0000)
        self.crcCalculator = crc.Calculator(crc_configuration)

    def serialize(self):
        header_buffer = struct.pack('>BH', SamsungHvacNasaPacket.start, self.length)

        self.numOfSignals = len(self.signals)

        data_buffer = struct.pack('>3B3BHBB', (self.source >> 16) & 0xFF, (self.source >> 8) & 0xFF, self.source & 0xFF,
                                  (self.destination >> 16) & 0xFF, (self.destination >> 8) & 0xFF,
                                  self.destination & 0xFF,
                                  self.packetType.value, self.sequence,
                                  self.numOfSignals)
        for command in self.signals:
            data_buffer += command.serialize()

        self.checksum = self.crcCalculator.checksum(data_buffer)
        tail_buffer = struct.pack('>HB', self.checksum, SamsungHvacNasaPacket.end)

        return header_buffer + data_buffer + tail_buffer

    def deserialize(buf, offset=0):
        packet = SamsungHvacNasaPacket()

        # 시작 마커
        offset += 1

        # 헤더 부분 처리
        packet.length = (buf[offset] << 8) | buf[offset + 1]
        offset += 2

        packet.source = (buf[offset] << 16) | (buf[offset + 1] << 8) | buf[offset + 2]
        offset += 3

        packet.destination = (buf[offset] << 16) | (buf[offset + 1] << 8) | buf[offset + 2]
        offset += 3

        packet.packetType = SamsungHvacNasaPacket.PacketType((buf[offset] << 8) | buf[offset + 1])
        offset += 2

        packet.sequence = buf[offset]
        offset += 1

        packet.numOfSignals = buf[offset]
        offset += 1

        # 개별 커맨드 처리
        packet.signals = []
        for i in range(packet.numOfSignals):
            command, offset = NasaSignal.deserialize(buf, offset)
            packet.signals.append(command)

        return packet, offset

    def __repr__(self):
        repr = f'{self.source:06X} -> {self.destination:06X}, {self.packetType.name}, {self.sequence}, '

        for signal in self.signals:
            repr += f'[{signal.__repr__()}]  '
        return repr


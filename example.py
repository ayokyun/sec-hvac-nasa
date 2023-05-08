from Commands import OnOffCommand, SetTemperatureCommand
from SamsungHvacNasaPacket import SamsungHvacNasaPacket
from utils import hexify

if __name__ == '__main__':
    packet = SamsungHvacNasaPacket()
    packet.length = 0x11
    packet.source = 0x620000
    packet.destination = 0x200000
    packet.packetType = SamsungHvacNasaPacket.PacketType.Control
    packet.sequence = 0xA8
    packet.signals = [OnOffCommand(on=True), SetTemperatureCommand(28.0)]

    buf = packet.serialize()
    print(hexify(buf))

    new_packet, _ = SamsungHvacNasaPacket.deserialize(buf, 0)
    print(hexify(new_packet.serialize()))

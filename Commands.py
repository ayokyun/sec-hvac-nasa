from NasaSignal import NasaSignal


class OnOffCommand(NasaSignal):
    def __init__(self, on):
        super().__init__()

        self.header = 0x4000
        self.value = 1 if on else 0


class SetTemperatureCommand(NasaSignal):
    def __init__(self, target_temperature):
        super().__init__()

        self.header = 0x4201
        self.value = int(target_temperature * 10)

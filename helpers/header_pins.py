from enum import Enum
from typing import List, Optional


class HeaderPinConfigDataModel:
    header_pin_number: int
    gpio_pin_number: int | None
    type: str
    voltage: str | None

    def to_dict(self):
        return {
            "header_pin_number": self.header_pin_number,
            "gpio_pin_number": self.gpio_pin_number,
            "type": self.type,
            "voltage": self.voltage
        }


class HeaderPinType(Enum):
    POWER = "POWER"
    GPIO = "GPIO"
    GROUND = "GROUND"


class Voltage(Enum):
    FIVE = "5v"
    THREE = "3v3"


class HeaderPinConfig:
    def __init__(self, header_pin_number: int, type: HeaderPinType,
                 gpio_pin_number: Optional[int] = None, voltage: Optional[Voltage] = None):
        self.header_pin_number = header_pin_number
        self.gpio_pin_number = gpio_pin_number
        self.type = type
        self.voltage = voltage

    def get_data(self):
        header_pin_config = HeaderPinConfigDataModel()
        header_pin_config.header_pin_number = self.header_pin_number
        header_pin_config.gpio_pin_number = self.gpio_pin_number
        header_pin_config.type = self.type.value
        header_pin_config.voltage = self.voltage.value if self.voltage is not None else None
        return header_pin_config


pin_header_config: List[HeaderPinConfig] = [
    HeaderPinConfig(header_pin_number=1,
                    type=HeaderPinType.POWER, voltage=Voltage.THREE),
    HeaderPinConfig(header_pin_number=2,
                    type=HeaderPinType.POWER, voltage=Voltage.FIVE),
    HeaderPinConfig(header_pin_number=3,
                    type=HeaderPinType.GPIO, gpio_pin_number=2),
    HeaderPinConfig(header_pin_number=4,
                    type=HeaderPinType.POWER, voltage=Voltage.FIVE),
    HeaderPinConfig(header_pin_number=5,
                    type=HeaderPinType.GPIO, gpio_pin_number=3),
    HeaderPinConfig(header_pin_number=6, type=HeaderPinType.GROUND),
    HeaderPinConfig(header_pin_number=7,
                    type=HeaderPinType.GPIO, gpio_pin_number=4),
    HeaderPinConfig(header_pin_number=8,
                    type=HeaderPinType.GPIO, gpio_pin_number=14),
    HeaderPinConfig(header_pin_number=9, type=HeaderPinType.GROUND),
    HeaderPinConfig(header_pin_number=10,
                    type=HeaderPinType.GPIO, gpio_pin_number=15),
    HeaderPinConfig(header_pin_number=11,
                    type=HeaderPinType.GPIO, gpio_pin_number=17),
    HeaderPinConfig(header_pin_number=12,
                    type=HeaderPinType.GPIO, gpio_pin_number=18),
    HeaderPinConfig(header_pin_number=13,
                    type=HeaderPinType.GPIO, gpio_pin_number=27),
    HeaderPinConfig(header_pin_number=14, type=HeaderPinType.GROUND),
    HeaderPinConfig(header_pin_number=15,
                    type=HeaderPinType.GPIO, gpio_pin_number=22),
    HeaderPinConfig(header_pin_number=16,
                    type=HeaderPinType.GPIO, gpio_pin_number=23),
    HeaderPinConfig(header_pin_number=17,
                    type=HeaderPinType.POWER, voltage=Voltage.THREE),
    HeaderPinConfig(header_pin_number=18,
                    type=HeaderPinType.GPIO, gpio_pin_number=24),
    HeaderPinConfig(header_pin_number=19,
                    type=HeaderPinType.GPIO, gpio_pin_number=10),
    HeaderPinConfig(header_pin_number=20, type=HeaderPinType.GROUND),
    HeaderPinConfig(header_pin_number=21,
                    type=HeaderPinType.GPIO, gpio_pin_number=9),
    HeaderPinConfig(header_pin_number=22,
                    type=HeaderPinType.GPIO, gpio_pin_number=25),
    HeaderPinConfig(header_pin_number=23,
                    type=HeaderPinType.GPIO, gpio_pin_number=11),
    HeaderPinConfig(header_pin_number=24,
                    type=HeaderPinType.GPIO, gpio_pin_number=8),
    HeaderPinConfig(header_pin_number=25, type=HeaderPinType.GROUND),
    HeaderPinConfig(header_pin_number=26,
                    type=HeaderPinType.GPIO, gpio_pin_number=7),
    HeaderPinConfig(header_pin_number=27,
                    type=HeaderPinType.GPIO, gpio_pin_number=0),
    HeaderPinConfig(header_pin_number=28,
                    type=HeaderPinType.GPIO, gpio_pin_number=1),
    HeaderPinConfig(header_pin_number=29,
                    type=HeaderPinType.GPIO, gpio_pin_number=5),
    HeaderPinConfig(header_pin_number=30, type=HeaderPinType.GROUND),
    HeaderPinConfig(header_pin_number=31,
                    type=HeaderPinType.GPIO, gpio_pin_number=6),
    HeaderPinConfig(header_pin_number=32,
                    type=HeaderPinType.GPIO, gpio_pin_number=12),
    HeaderPinConfig(header_pin_number=33,
                    type=HeaderPinType.GPIO, gpio_pin_number=13),
    HeaderPinConfig(header_pin_number=34, type=HeaderPinType.GROUND),
    HeaderPinConfig(header_pin_number=35,
                    type=HeaderPinType.GPIO, gpio_pin_number=19),
    HeaderPinConfig(header_pin_number=36,
                    type=HeaderPinType.GPIO, gpio_pin_number=16),
    HeaderPinConfig(header_pin_number=37,
                    type=HeaderPinType.GPIO, gpio_pin_number=26),
    HeaderPinConfig(header_pin_number=38,
                    type=HeaderPinType.GPIO, gpio_pin_number=20),
    HeaderPinConfig(header_pin_number=39, type=HeaderPinType.GROUND),
    HeaderPinConfig(header_pin_number=40,
                    type=HeaderPinType.GPIO, gpio_pin_number=21),
]

from enum import Enum, unique


@unique
class SlideType(Enum):
    MCD = 1,
    OMETIFF = 2
    TXT = 3,

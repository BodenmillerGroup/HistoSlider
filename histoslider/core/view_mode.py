from enum import Enum, unique


@unique
class ViewMode(Enum):
    GREYSCALE = 'Greyscale'
    RGB = 'RGB'

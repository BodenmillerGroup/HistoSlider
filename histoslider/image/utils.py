from enum import Enum, unique
from typing import Tuple

import numpy as np
import cv2


@unique
class Color(Enum):
    RED = (1, 0, 0)
    GREEN = (0, 1, 0)
    BLUE = (0, 0, 1)
    YELLOW = (1, 1, 0)
    CYAN = (1, 0, 1)
    MAGENTA = (0, 1, 1)


def colorize(image: np.ndarray, color: Color):
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    image = image * color.value
    return image


def hue_colorize(image: np.ndarray, hue, saturation=1):
    """ Add color of the given hue to an RGB image.

    By default, set the saturation to 1 so that the colors pop!
    """
    # rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    # hsv = rgb2hsv(rgb)
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    hsv[:, :, 1] = saturation
    hsv[:, :, 0] = hue
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    # return hsv2rgb(hsv)


def scale_image(image: np.ndarray, scale: float, levels: Tuple[float, float]):
    result = image * (scale / (levels[1] - levels[0]))
    return result

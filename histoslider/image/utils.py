from typing import Tuple

import numpy as np
import cv2


COLOR_MULTIPLIERS = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1))


def colorize(image: np.ndarray, color_index: int):
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    # image = np.stack((image,) * 3, axis=-1)
    image = image * COLOR_MULTIPLIERS[color_index]
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

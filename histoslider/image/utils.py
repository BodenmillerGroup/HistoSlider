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


def colorize_mask(mask: np.ndarray, saturation=1):
    unique_values = np.unique(mask)
    hue_rotations = np.linspace(0, 360, len(unique_values), dtype=np.uint8)
    rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    hsv[:, :, 1] = saturation
    hsv[:, :, 0] = hue_rotations[mask[:, :]]
    return hue_rotations


def apply_mask(image: np.ndarray, mask: np.ndarray):
    # image = image.astype(np.uint8)
    mask = mask.astype(np.uint8)
    img = np.zeros(image.shape, image.dtype)
    if len(img.shape) == 3:
        img[:, :] = (0, 0, 255)
    blue_mask = cv2.bitwise_and(img, img, mask=mask)
    # im_color = cv2.applyColorMap(mask, cv2.COLORMAP_JET)
    # result = cv2.add(image, blue_mask)
    result = cv2.addWeighted(image, 0.8, blue_mask, 0.2, 0)
    return result


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
    minL, maxL = levels
    if maxL <= minL:
        return image
    result = image * (scale / (maxL - minL))
    return result

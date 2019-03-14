from typing import Tuple

import numpy as np
import cv2


def colorize(image: np.ndarray, hue, saturation=1):
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
    # scale = self.settings.max
    # result = rescaleData(self._image, 255.0/(self.settings.levels[1] - self.settings.levels[0]), 0)
    # result = self._image * (scale/(self.settings.levels[1] - self.settings.levels[0]))
    result = image * (scale / (levels[1] - levels[0]))
    # result = cv2.convertScaleAbs(self.image, alpha=(scale / (maxL - minL)))
    return result.astype(dtype=np.float32)

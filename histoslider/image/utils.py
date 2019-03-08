from numpy.core.multiarray import ndarray
from skimage.color import rgb2hsv, hsv2rgb


def colorize(image: ndarray, hue, saturation=1):
    """ Add color of the given hue to an RGB image.

    By default, set the saturation to 1 so that the colors pop!
    """
    hsv = rgb2hsv(image)
    hsv[:, :, 1] = saturation
    hsv[:, :, 0] = hue
    return hsv2rgb(hsv)

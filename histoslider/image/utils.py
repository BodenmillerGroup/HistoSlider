from numpy.core.multiarray import ndarray
from skimage.color import grey2rgb, rgb2hsv, hsv2rgb


def colorize(image: ndarray, hue, saturation=1):
    """ Add color of the given hue to an RGB image.

    By default, set the saturation to 1 so that the colors pop!
    """
    rgb = grey2rgb(image)
    hsv = rgb2hsv(rgb)
    hsv[:, :, 1] = saturation
    hsv[:, :, 0] = hue
    return hsv2rgb(hsv)

import numpy as np
from pyqtgraph import ImageItem

from histoslider.models.channel import Channel


class ChannelImageItem(ImageItem):
    def __init__(self, image: np.ndarray, channel: Channel, **kargs):
        ImageItem.__init__(self, image, levels=channel.settings.levels, **kargs)
        self.channel = channel
        self.setPxMode(False)
        self.setAutoDownsample(False)

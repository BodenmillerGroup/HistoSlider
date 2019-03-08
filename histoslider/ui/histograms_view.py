from typing import List

from pyqtgraph import GraphicsView, GraphicsLayout

from histoslider.image.channel_image_item import ChannelImageItem
from histoslider.ui.histogram_view import HistogramView


class HistogramsView(GraphicsView):
    def __init__(self, parent=None):
        GraphicsView.__init__(self, parent)
        self.layout = GraphicsLayout()
        self.setCentralItem(self.layout)

    def set_channels(self, items: List[ChannelImageItem]):
        self.layout.clear()
        for item in items:
            histogram_view = HistogramView(item)
            self.layout.addItem(histogram_view)

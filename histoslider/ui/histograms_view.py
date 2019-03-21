from pyqtgraph import GraphicsView, GraphicsLayout

from histoslider.core.message import ChannelImagesChangedMessage
from histoslider.ui.histogram_view import HistogramView


class HistogramsView(GraphicsView):
    def __init__(self, parent=None, blend_view=None):
        GraphicsView.__init__(self, parent)
        self.blend_view = blend_view

        self.layout = GraphicsLayout()
        self.setCentralItem(self.layout)

    def clear(self):
        self.layout.clear()

    def set_channels(self, message: ChannelImagesChangedMessage):
        self.clear()
        for item in message.images:
            histogram_view = HistogramView(item, self.blend_view)
            self.layout.addItem(histogram_view)
            self.layout.nextRow()

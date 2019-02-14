from PyQt5.QtWidgets import QWidget
from pyqtgraph import GraphicsView, GraphicsLayout, ViewBox

from histoslider.core.hub_listener import HubListener
from histoslider.core.message import TreeViewCurrentItemChangedMessage, SlideRemovedMessage, ShowItemChangedMessage
from histoslider.image.tile_image_view import TileImageView
from histoslider.models.channel_data import ChannelData
from histoslider.models.data_manager import DataManager
from histoslider.models.slide_data import SlideData


class TileView(GraphicsView, HubListener):
    def __init__(self, parent: QWidget):
        GraphicsView.__init__(self, parent)
        HubListener.__init__(self)
        self.register_to_hub(DataManager.hub)
        self.layout = GraphicsLayout()
        self.setCentralItem(self.layout)
        self.tiles = {}

    def register_to_hub(self, hub):
        hub.subscribe(self, TreeViewCurrentItemChangedMessage, self._on_current_item_changed)
        hub.subscribe(self, SlideRemovedMessage, self._on_slide_removed)
        hub.subscribe(self, ShowItemChangedMessage, self._on_show_item_changed)

    def _on_slide_removed(self, message: SlideRemovedMessage):
        self.layout.clear()

    def _on_current_item_changed(self, message: TreeViewCurrentItemChangedMessage):
        pass

    def _on_show_item_changed(self, message: ShowItemChangedMessage):
        item = message.item
        if isinstance(item, SlideData) or isinstance(item, ChannelData):
            if item.checked:
                if not item.name in self.tiles:
                    tile_image_view = TileImageView(self.layout, item)
                    self.layout.addItem(tile_image_view)
                    for name, tile in self.tiles.items():
                        tile_image_view.linkView(ViewBox.XAxis, tile)
                        tile_image_view.linkView(ViewBox.YAxis, tile)
                    self.tiles[item.name] = tile_image_view
            else:
                if item.name in self.tiles:
                    tile_image_view = self.tiles[item.name]
                    self.layout.removeItem(tile_image_view)
                    del self.tiles[item.name]

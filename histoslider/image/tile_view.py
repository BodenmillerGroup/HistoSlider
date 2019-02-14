from typing import Dict

from PyQt5.QtWidgets import QWidget
from pyqtgraph import GraphicsView, GraphicsLayout, ViewBox, LabelItem

from histoslider.core.hub_listener import HubListener
from histoslider.core.message import TreeViewCurrentItemChangedMessage, SlideRemovedMessage, ShowItemChangedMessage
from histoslider.image.image_item import ImageItem
from histoslider.image.slide_type import SlideType
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
                    tile = TileImageView(self.layout, item)
                    self.layout.addItem(tile)
                    self.tiles[item.name] = tile
            else:
                if item.name in self.tiles:
                    tile = self.tiles[item.name]
                    self.layout.removeItem(tile)
                    del self.tiles[item.name]

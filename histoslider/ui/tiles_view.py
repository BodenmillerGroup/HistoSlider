from typing import Dict

from PyQt5.QtWidgets import QWidget
from pyqtgraph import GraphicsView, GraphicsLayout, ViewBox

from histoslider.core.data_manager import DataManager
from histoslider.core.hub_listener import HubListener
from histoslider.core.message import TreeViewCurrentItemChangedMessage, SlideRemovedMessage, ShowItemChangedMessage, \
    SlideUnloadedMessage
from histoslider.models.channel import Channel
from histoslider.models.slide import Slide
from histoslider.ui.tile_view import TileView


class TilesView(GraphicsView, HubListener):
    def __init__(self, parent: QWidget):
        GraphicsView.__init__(self, parent)
        HubListener.__init__(self)
        self.register_to_hub(DataManager.hub)

        self.layout = GraphicsLayout()
        self.setCentralItem(self.layout)

        self.tiles: Dict[str, TileView] = dict()

    def register_to_hub(self, hub):
        hub.subscribe(self, TreeViewCurrentItemChangedMessage, self._on_current_item_changed)
        hub.subscribe(self, SlideRemovedMessage, self._on_slide_removed)
        hub.subscribe(self, SlideUnloadedMessage, self._on_slide_unloaded)
        hub.subscribe(self, ShowItemChangedMessage, self._on_show_item_changed)

    def _on_slide_removed(self, message: SlideRemovedMessage):
        self.layout.clear()
        self.tiles.clear()

    def _on_slide_unloaded(self, message: SlideUnloadedMessage):
        self.layout.clear()
        self.tiles.clear()

    def _on_current_item_changed(self, message: TreeViewCurrentItemChangedMessage):
        pass

    def get_cell(self, i: int):
        l = len(self.tiles.keys())
        if l > 4:
            rows = (0, 0, 0, 1, 1, 1, 2, 2, 2)
            cols = (0, 1, 2, 0, 1, 2, 0, 1, 2)
        else:
            rows = (0, 0, 1, 1)
            cols = (0, 1, 0, 1)
        return rows[i], cols[i]

    def _on_show_item_changed(self, message: ShowItemChangedMessage):
        item = message.item
        if isinstance(item, Slide) or isinstance(item, Channel):
            self.layout.clear()
            if item.checked:
                if item.name not in self.tiles:
                    tile_image_view = TileView(self.layout, item)
                    self.tiles[item.name] = tile_image_view
            else:
                if item.name in self.tiles:
                    self.tiles.pop(item.name)

            if len(self.tiles) > 0:
                i = 0
                first_tile = self.tiles[list(self.tiles.keys())[0]]
                for tile in self.tiles.values():
                    if first_tile is not tile:
                        tile.linkView(ViewBox.XAxis, first_tile)
                        tile.linkView(ViewBox.YAxis, first_tile)
                    cell = self.get_cell(i)
                    self.layout.addItem(tile, cell[0], cell[1])
                    i = i + 1

    def fit_all_tiles(self):
        for name, tile in self.tiles.items():
            tile.autoRange()

from typing import Dict

from PyQt5.QtWidgets import QWidget
from pyqtgraph import GraphicsView, GraphicsLayout, ViewBox

from histoslider.core.data_manager import DataManager
from histoslider.core.hub_listener import HubListener
from histoslider.core.message import SlideRemovedMessage, CheckedChannelChangedMessage, SlideUnloadedMessage, \
    SelectedChannelsChangedMessage
from histoslider.models.channel import Channel
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
        hub.subscribe(self, SlideRemovedMessage, self._on_slide_removed)
        hub.subscribe(self, SlideUnloadedMessage, self._on_slide_unloaded)
        hub.subscribe(self, CheckedChannelChangedMessage, self._on_checked_channel_changed)
        hub.subscribe(self, SelectedChannelsChangedMessage, self._on_selected_channels_changed)

    def clear(self):
        self.layout.clear()
        self.tiles.clear()

    def _on_slide_removed(self, message: SlideRemovedMessage):
        self.clear()

    def _on_slide_unloaded(self, message: SlideUnloadedMessage):
        self.clear()

    def get_cell(self, i: int):
        l = len(self.tiles.keys())
        if l > 9:
            rows = (0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3)
            cols = (0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3)
        elif l > 4:
            rows = (0, 0, 0, 1, 1, 1, 2, 2, 2)
            cols = (0, 1, 2, 0, 1, 2, 0, 1, 2)
        else:
            rows = (0, 0, 1, 1)
            cols = (0, 1, 0, 1)
        return rows[i], cols[i]

    def _on_selected_channels_changed(self, message: SelectedChannelsChangedMessage):
        if len()
        self.clear()
        if len(message.channels) > 0:
            for channel in message.channels.values():
                tile = TileView(self.layout, channel)
                self.tiles[channel.name] = tile

            first_tile = self.tiles[list(self.tiles.keys())[0]]
            for i, tile in enumerate(self.tiles.values()):
                if first_tile is not tile:
                    tile.linkView(ViewBox.XAxis, first_tile)
                    tile.linkView(ViewBox.YAxis, first_tile)
                cell = self.get_cell(i)
                self.layout.addItem(tile, cell[0], cell[1])


    def _on_checked_channel_changed(self, message: CheckedChannelChangedMessage):
        channel = message.channel
        if isinstance(channel, Channel):
            self.layout.clear()
            if channel.checked:
                if channel.name not in self.tiles:
                    tile_image_view = TileView(self.layout, channel)
                    self.tiles[channel.name] = tile_image_view
            else:
                if channel.name in self.tiles:
                    self.tiles.pop(channel.name)

            if len(self.tiles) > 0:
                first_tile = self.tiles[list(self.tiles.keys())[0]]
                for i, tile in enumerate(self.tiles.values()):
                    if first_tile is not tile:
                        tile.linkView(ViewBox.XAxis, first_tile)
                        tile.linkView(ViewBox.YAxis, first_tile)
                    cell = self.get_cell(i)
                    self.layout.addItem(tile, cell[0], cell[1])

    def fit_all_tiles(self):
        for name, tile in self.tiles.items():
            tile.autoRange()

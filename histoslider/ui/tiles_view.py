from typing import Dict

from PyQt5.QtWidgets import QWidget
from pyqtgraph import GraphicsView, GraphicsLayout, ViewBox

from histoslider.models.channel import Channel
from histoslider.ui.tile_view import TileView


class TilesView(GraphicsView):
    def __init__(self, parent: QWidget):
        GraphicsView.__init__(self, parent)

        self.layout = GraphicsLayout()
        self.setCentralItem(self.layout)

        self.tiles: Dict[str, TileView] = dict()

    def clear(self):
        self.layout.clear()
        self.tiles.clear()

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

    def set_channels(self, channels: Dict[str, Channel]):
        self.clear()
        if len(channels) > 0:
            for channel in channels.values():
                tile = TileView(self.layout, channel)
                self.tiles[channel.name] = tile

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

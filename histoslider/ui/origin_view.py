from PyQt5.QtWidgets import QWidget
from pyqtgraph import ImageView, ScaleBar

from histoslider.core.data_manager import DataManager
from histoslider.core.hub_listener import HubListener
from histoslider.core.message import SelectedTreeNodeChangedMessage, SlideRemovedMessage, SlideUnloadedMessage
from histoslider.models.channel import Channel


class OriginView(ImageView, HubListener):
    def __init__(self, parent: QWidget):
        ImageView.__init__(self, parent, "OriginView")
        HubListener.__init__(self)
        self.register_to_hub(DataManager.hub)
        histogram_lut_item = self.getHistogramWidget().item
        histogram_lut_item.sigLevelsChanged.connect(self._on_levels_changed)
        histogram_lut_item.sigLookupTableChanged.connect(self._on_lookup_table_changed)
        self.getHistogramWidget().hide()

        self.scale = ScaleBar(size=10, suffix='μm')
        self.scale.setParentItem(self.getView())
        self.scale.anchor((1, 1), (1, 1), offset=(-40, -40))
        self.scale.hide()

        self.channel: Channel = None
        self.lut = None

    # FIX: https://stackoverflow.com/questions/50722238/pyqtgraph-imageview-and-color-images
    def updateImage(self, autoHistogramRange=True):
        super().updateImage(autoHistogramRange)
        self.getImageItem().setLookupTable(self.lut)

    def setLookupTable(self, lut):
        self.lut = lut
        self.updateImage()

    def register_to_hub(self, hub):
        hub.subscribe(self, SelectedTreeNodeChangedMessage, self._on_selected_tree_node_changed)
        hub.subscribe(self, SlideRemovedMessage, self._on_slide_removed)
        hub.subscribe(self, SlideUnloadedMessage, self._on_slide_unloaded)

    def _on_levels_changed(self):
        if self.channel is None or self.getImageItem() is None:
            return
        if self.channel.settings.levels is None:
            self.autoLevels()
        self.channel.settings.levels = self.getHistogramWidget().item.getLevels()

    def _on_lookup_table_changed(self):
        if self.channel is None or self.getImageItem() is None:
            return
        lut = self.getHistogramWidget().item.getLookupTable(n=int(self.channel.settings.levels[1]), alpha=0.5)
        self.channel.settings.lut = lut

    def _on_slide_removed(self, message: SlideRemovedMessage):
        self.getHistogramWidget().hide()
        self.clear()

    def _on_slide_unloaded(self, message: SlideUnloadedMessage):
        self.getHistogramWidget().hide()
        self.clear()

    def _on_selected_tree_node_changed(self, message: SelectedTreeNodeChangedMessage):
        if not isinstance(message.node, Channel):
            return
        self.channel = message.node

        self.setImage(self.channel.image, levels=self.channel.settings.levels)
        self.getImageItem().setLookupTable(self.channel.settings.lut)
        self.getHistogramWidget().show()

    def show_scale_bar(self, state: bool):
        if state:
            self.scale.show()
        else:
            self.scale.hide()

    def clear(self):
        self.channel = None
        super().clear()

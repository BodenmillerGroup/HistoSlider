from pyqtgraph import DataTreeWidget

from histoslider.core.data_manager import DataManager
from histoslider.core.hub_listener import HubListener
from histoslider.core.message import SelectedChannelChangedMessage, SlideRemovedMessage, SlideUnloadedMessage


class InfoWidget(DataTreeWidget, HubListener):
    def __init__(self, parent):
        DataTreeWidget.__init__(self, parent)
        HubListener.__init__(self)
        self.register_to_hub(DataManager.hub)

    def register_to_hub(self, hub):
        hub.subscribe(self, SelectedChannelChangedMessage, self._on_selected_channel_changed)
        hub.subscribe(self, SlideRemovedMessage, self._on_slide_removed)
        hub.subscribe(self, SlideUnloadedMessage, self._on_slide_unloaded)

    def _on_slide_removed(self, message: SlideRemovedMessage):
        self.getHistogramWidget().hide()
        self.clear()

    def _on_slide_unloaded(self, message: SlideUnloadedMessage):
        self.getHistogramWidget().hide()
        self.clear()

    def _on_selected_channel_changed(self, message: SelectedChannelChangedMessage):
        self.setData(message.channel)

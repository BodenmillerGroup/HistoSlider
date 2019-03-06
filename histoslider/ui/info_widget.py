from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

from histoslider.core.data_manager import DataManager
from histoslider.core.hub_listener import HubListener
from histoslider.core.message import SelectedTreeNodeChangedMessage, SlideRemovedMessage, SlideUnloadedMessage


class InfoWidget(QTableWidget, HubListener):
    def __init__(self, parent):
        QTableWidget.__init__(self, parent)
        HubListener.__init__(self)

        # self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(10);
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(('Key', 'Value'))
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)

        self.register_to_hub(DataManager.hub)

    def register_to_hub(self, hub):
        hub.subscribe(self, SelectedTreeNodeChangedMessage, self._on_selected_tree_node_changed)
        hub.subscribe(self, SlideRemovedMessage, self._on_slide_removed)
        hub.subscribe(self, SlideUnloadedMessage, self._on_slide_unloaded)

    def _on_slide_removed(self, message: SlideRemovedMessage):
        self.clearContents()

    def _on_slide_unloaded(self, message: SlideUnloadedMessage):
        self.clearContents()

    def set_data(self, data: dict):
        self.clearContents()
        self.setRowCount(len(data))
        for index, (key, value) in enumerate(data.items()):
            self.setItem(index, 0, QTableWidgetItem(key))
            self.setItem(index, 1, QTableWidgetItem(str(value)))

    def _on_selected_tree_node_changed(self, message: SelectedTreeNodeChangedMessage):
        if message.node.meta is not None:
            self.set_data(message.node.meta)
        else:
            self.clearContents()

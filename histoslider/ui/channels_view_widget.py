from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolBar, QAction
from imctools.io.mcdxmlparser import Acquisition

from histoslider.core.data_manager import DataManager
from histoslider.core.hub_listener import HubListener
from histoslider.core.message import SelectedTreeNodeChangedMessage
from histoslider.r.r_manager import RManager
from histoslider.ui.channels_table_view import ChannelsTableView


class ChannelsViewWidget(QWidget, HubListener):
    def __init__(self, parent: QWidget):
        QWidget.__init__(self, parent)
        HubListener.__init__(self)

        self.channels_view = ChannelsTableView(self)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.channels_view)

        self.register_to_hub(DataManager.hub)

    def register_to_hub(self, hub):
        hub.subscribe(self, SelectedTreeNodeChangedMessage, self._on_selected_tree_node_changed)

    def _on_selected_tree_node_changed(self, message: SelectedTreeNodeChangedMessage):
        item = message.node
        if isinstance(item, Acquisition):
            acquisition: Acquisition = item
            self.channels_view.set_channels(item.get_channels())

    def fit_all_tiles(self):
        r = RManager()

    @property
    def toolbar(self) -> QToolBar:
        toolbar = QToolBar(self)

        fit_all_tiles_action = QAction(QIcon(":/icons/grid.png"), "Fit All Tiles", self)
        fit_all_tiles_action.triggered.connect(self.fit_all_tiles)
        toolbar.addAction(fit_all_tiles_action)

        return toolbar

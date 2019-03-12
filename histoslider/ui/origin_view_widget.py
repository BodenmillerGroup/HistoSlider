from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolBar, QAction

from histoslider.core.hub_listener import HubListener
from histoslider.core.manager import Manager
from histoslider.core.message import SelectedTreeNodeChangedMessage, SlideRemovedMessage, SlideUnloadedMessage
from histoslider.models.channel import Channel
from histoslider.ui.origin_view import OriginView


class OriginViewWidget(QWidget, HubListener):
    def __init__(self, parent: QWidget):
        QWidget.__init__(self, parent)
        HubListener.__init__(self)
        self.register_to_hub(Manager.hub)

        self.origin_view = OriginView(self)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.origin_view)

    def register_to_hub(self, hub):
        hub.subscribe(self, SelectedTreeNodeChangedMessage, self._on_selected_tree_node_changed)
        hub.subscribe(self, SlideRemovedMessage, self._on_slide_removed)
        hub.subscribe(self, SlideUnloadedMessage, self._on_slide_unloaded)

    def _on_slide_removed(self, message: SlideRemovedMessage):
        self.origin_view.clear()

    def _on_slide_unloaded(self, message: SlideUnloadedMessage):
        self.origin_view.clear()

    def _on_selected_tree_node_changed(self, message: SelectedTreeNodeChangedMessage):
        if not isinstance(message.node, Channel):
            return
        self.origin_view.set_channel(message.node)

    def show_scale_bar(self, state: bool):
        self.origin_view.show_scale_bar(state)

    @property
    def toolbar(self) -> QToolBar:
        toolbar = QToolBar(self)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        show_scale_bar_action = QAction(QIcon(":/icons/icons8-ruler-16.png"), "Scale Bar", self)
        show_scale_bar_action.triggered.connect(self.show_scale_bar)
        show_scale_bar_action.setCheckable(True)
        toolbar.addAction(show_scale_bar_action)

        return toolbar

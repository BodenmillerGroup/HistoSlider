from inspect import getmembers, isfunction

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolBar, QAction, QLabel, QComboBox

from histoslider.core.hub_listener import HubListener
from histoslider.core.manager import Manager
from histoslider.core.message import SlideRemovedMessage, SlideUnloadedMessage, \
    BlendModeChangedMessage, ChannelImagesChangedMessage, SelectedMaskChangedMessage
from histoslider.libs import blend_modes
from histoslider.ui.blend_view import BlendView
from histoslider.ui.mask_view import MaskView


class MaskViewWidget(QWidget, HubListener):
    def __init__(self, parent: QWidget):
        QWidget.__init__(self, parent)
        HubListener.__init__(self)
        self.register_to_hub(Manager.hub)

        self.mask_view = MaskView(self)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.mask_view)

    def register_to_hub(self, hub):
        hub.subscribe(self, SelectedMaskChangedMessage, self._on_selected_mask_changed)
        hub.subscribe(self, SlideRemovedMessage, self._on_slide_removed)
        hub.subscribe(self, SlideUnloadedMessage, self._on_slide_unloaded)

    def clear(self):
        self.mask_view.clear()

    def _on_selected_mask_changed(self, message: SelectedMaskChangedMessage):
        self.mask_view.set_mask(message.mask)

    def _on_slide_removed(self, message: SlideRemovedMessage):
        self.clear()

    def _on_slide_unloaded(self, message: SlideUnloadedMessage):
        self.clear()

    @property
    def toolbar(self) -> QToolBar:
        toolbar = QToolBar(self)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        return toolbar

from inspect import getmembers, isfunction

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolBar, QAction, QLabel, QComboBox

from histoslider.core.hub_listener import HubListener
from histoslider.core.manager import Manager
from histoslider.core.message import SlideRemovedMessage, SlideUnloadedMessage, \
    BlendModeChangedMessage, ChannelImagesChangedMessage
from histoslider.ui.merge_view import MergeView


class MergeViewWidget(QWidget, HubListener):
    def __init__(self, parent: QWidget):
        QWidget.__init__(self, parent)
        HubListener.__init__(self)
        self.register_to_hub(Manager.hub)

        self.merge_view = MergeView(self)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.merge_view)

    def register_to_hub(self, hub):
        hub.subscribe(self, ChannelImagesChangedMessage, self._on_channel_images_changed)
        hub.subscribe(self, SlideRemovedMessage, self._on_slide_removed)
        hub.subscribe(self, SlideUnloadedMessage, self._on_slide_unloaded)

    def clear(self):
        self.merge_view.clear()

    def _on_channel_images_changed(self, message: ChannelImagesChangedMessage):
        self.merge_view.set_images(message.images)

    def _on_slide_removed(self, message: SlideRemovedMessage):
        self.clear()

    def _on_slide_unloaded(self, message: SlideUnloadedMessage):
        self.clear()

    def _blend_current_text_changed(self, text: str):
        self.merge_view.set_blend_mode(text)

    @property
    def toolbar(self) -> QToolBar:
        toolbar = QToolBar(self)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        label = QLabel("Blend:")
        toolbar.addWidget(label)

        blend_combo_box = QComboBox()
        modes_list = [o for o in getmembers(QPainter) if o[0].startswith('CompositionMode_')]
        blend_combo_box.addItems([f[0] for f in modes_list])
        blend_combo_box.currentTextChanged.connect(self._blend_current_text_changed)
        toolbar.addWidget(blend_combo_box)

        return toolbar

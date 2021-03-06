from inspect import getmembers

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolBar, QAction, QLabel, QComboBox

from histoslider.core.hub_listener import HubListener
from histoslider.core.manager import Manager
from histoslider.core.message import SlideRemovedMessage, SlideUnloadedMessage, \
    ChannelImagesChangedMessage
from histoslider.ui.blend_view import BlendView


class BlendViewWidget(QWidget, HubListener):
    def __init__(self, parent: QWidget):
        QWidget.__init__(self, parent)
        HubListener.__init__(self)
        self.register_to_hub(Manager.hub)

        self.blend_view = BlendView(self)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.blend_view)

    def register_to_hub(self, hub):
        hub.subscribe(self, ChannelImagesChangedMessage, self._on_channel_images_changed)
        hub.subscribe(self, SlideRemovedMessage, self._on_slide_removed)
        hub.subscribe(self, SlideUnloadedMessage, self._on_slide_unloaded)

    def clear(self):
        self.blend_view.clear()

    def _on_channel_images_changed(self, message: ChannelImagesChangedMessage):
        self.blend_view.set_images(message.images)

    def _on_slide_removed(self, message: SlideRemovedMessage):
        self.clear()

    def _on_slide_unloaded(self, message: SlideUnloadedMessage):
        self.clear()

    def _show_scale_bar(self, state: bool):
        self.blend_view.show_scale_bar(state)

    def _show_mask(self, state: bool):
        self.blend_view.show_mask(state)

    def _blend_current_text_changed(self, text: str):
        self.blend_view.set_blend_mode(text)

    @property
    def toolbar(self) -> QToolBar:
        toolbar = QToolBar(self)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        label = QLabel("Blend:")
        toolbar.addWidget(label)

        blend_combo_box = QComboBox()
        modes_list = [o for o in getmembers(QPainter) if o[0].startswith('CompositionMode_')]
        blend_combo_box.addItems([f[0].replace('CompositionMode_', '') for f in modes_list])
        blend_combo_box.setCurrentText('Screen')
        blend_combo_box.currentTextChanged.connect(self._blend_current_text_changed)
        toolbar.addWidget(blend_combo_box)

        toolbar.addSeparator()

        show_scale_bar_action = QAction(QIcon(":/icons/icons8-ruler-16.png"), "Scale Bar", self)
        show_scale_bar_action.triggered.connect(self._show_scale_bar)
        show_scale_bar_action.setCheckable(True)
        toolbar.addAction(show_scale_bar_action)

        show_mask_action = QAction(QIcon(":/icons/icons8-ruler-16.png"), "Mask", self)
        show_mask_action.triggered.connect(self._show_mask)
        show_mask_action.setCheckable(True)
        toolbar.addAction(show_mask_action)

        return toolbar

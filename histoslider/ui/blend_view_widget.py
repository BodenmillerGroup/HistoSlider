from inspect import getmembers, isfunction

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolBar, QAction, QLabel, QComboBox

from histoslider.core.hub_listener import HubListener
from histoslider.core.manager import Manager
from histoslider.core.message import SelectedChannelsChangedMessage, SlideRemovedMessage, SlideUnloadedMessage, \
    BlendModeChangedMessage
from histoslider.image.channel_image_item import ChannelImageItem
from histoslider.libs import blend_modes
from histoslider.ui.blend_view import BlendView
from histoslider.ui.histograms_view import HistogramsView


class BlendViewWidget(QWidget, HubListener):
    def __init__(self, parent: QWidget):
        QWidget.__init__(self, parent)
        HubListener.__init__(self)
        self.register_to_hub(Manager.hub)

        self.blend_view = BlendView(self)
        # self.histograms_view = HistogramsView(self)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.blend_view)
        # self.verticalLayout.addWidget(self.histograms_view)

    def register_to_hub(self, hub):
        hub.subscribe(self, SelectedChannelsChangedMessage, self._on_selected_channels_changed)
        hub.subscribe(self, SlideRemovedMessage, self._on_slide_removed)
        hub.subscribe(self, SlideUnloadedMessage, self._on_slide_unloaded)

    def _on_selected_channels_changed(self, message: SelectedChannelsChangedMessage):
        items = []
        for channel in message.channels.values():
            items.append(ChannelImageItem(channel))
        self.blend_view.set_channels(items)
        # self.histograms_view.set_channels(items)

    def _on_slide_removed(self, message: SlideRemovedMessage):
        self.blend_view.clear()

    def _on_slide_unloaded(self, message: SlideUnloadedMessage):
        self.blend_view.clear()

    def _show_scale_bar(self, state: bool):
        self.blend_view.show_scale_bar(state)

    def _blend_current_text_changed(self, text: str):
        Manager.hub.broadcast(BlendModeChangedMessage(self, text))

    @property
    def toolbar(self) -> QToolBar:
        toolbar = QToolBar(self)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        label = QLabel("Blend:")
        toolbar.addWidget(label)

        blend_combo_box = QComboBox()
        functions_list = [o for o in getmembers(blend_modes) if isfunction(o[1]) and not o[0].startswith('_')]
        print(functions_list)
        blend_combo_box.addItems([f[0] for f in functions_list])
        blend_combo_box.currentTextChanged.connect(self._blend_current_text_changed)
        toolbar.addWidget(blend_combo_box)

        toolbar.addSeparator()

        show_scale_bar_action = QAction(QIcon(":/icons/icons8-ruler-16.png"), "Scale Bar", self)
        show_scale_bar_action.triggered.connect(self._show_scale_bar)
        show_scale_bar_action.setCheckable(True)
        toolbar.addAction(show_scale_bar_action)

        return toolbar

import os
from typing import Dict

import gc
from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QPixmapCache
from pyqtgraph import BusyCursor

from histoslider.core.hub import Hub
from histoslider.core.hub_listener import HubListener
from histoslider.core.message import SelectedChannelsChangedMessage, SelectedAcquisitionChangedMessage, \
    SlideImportedMessage, SlideLoadedMessage, SlideUnloadedMessage, SlideRemovedMessage, ViewModeChangedMessage
from histoslider.core.view_mode import ViewMode
from histoslider.image.slide_type import SlideType
from histoslider.loaders.mcd.mcd_loader import McdLoader
from histoslider.loaders.ome_tiff.ome_tiff_loader import OmeTiffLoader
from histoslider.loaders.txt.txt_loader import TxtLoader
from histoslider.models.acquisition import Acquisition
from histoslider.models.channel import Channel
from histoslider.models.slide import Slide
from histoslider.models.workspace_model import WorkspaceModel


class Data(HubListener):
    def __init__(self, hub: Hub):
        HubListener.__init__(self)
        self.hub = hub
        self.register_to_hub(self.hub)
        self.workspace_model = WorkspaceModel()

        self.view_mode = ViewMode.GREYSCALE
        self.selected_acquisition: Acquisition = None
        self.selected_channels: Dict[str, Channel] = None

    def register_to_hub(self, hub):
        hub.subscribe(self, SelectedAcquisitionChangedMessage, self._on_selected_acquisition_changed)
        hub.subscribe(self, SelectedChannelsChangedMessage, self._on_selected_channels_changed)
        hub.subscribe(self, ViewModeChangedMessage, self._on_view_mode_changed)

    def _on_selected_acquisition_changed(self, message: SelectedAcquisitionChangedMessage) -> None:
        self.selected_acquisition = message.acquisition

    def _on_selected_channels_changed(self, message: SelectedChannelsChangedMessage) -> None:
        self.selected_channels = message.channels

    def load_workspace(self, path: str) -> None:
        with BusyCursor():
            self.selected_acquisition = None
            self.selected_channels = None
            self.workspace_model.beginResetModel()
            self.workspace_model.load_workspace(path)
            self.workspace_model.endResetModel()

    def save_workspace(self, path: str) -> None:
        with BusyCursor():
            self.workspace_model.save_workspace(path)

    def import_slide(self, file_path: str) -> None:
        with BusyCursor():
            filename, file_extension = os.path.splitext(file_path)
            file_name = os.path.basename(file_path)
            file_extension = file_extension.lower()
            if file_extension == '.mcd':
                slide = Slide(file_name, file_path, SlideType.MCD, McdLoader)
            elif file_extension == '.tiff' or file_extension == '.tif':
                if filename.endswith('.ome'):
                    slide = Slide(file_name, file_path, SlideType.OMETIFF, OmeTiffLoader)
            elif file_extension == '.txt':
                slide = Slide(file_name, file_path, SlideType.TXT, TxtLoader)

            if slide is not None:
                self.workspace_model.beginResetModel()
                self.workspace_model.workspace_data.add_slide(slide)
                self.workspace_model.endResetModel()
                QPixmapCache.clear()
                self.hub.broadcast(SlideImportedMessage(self))

    def load_slides(self, indexes: [QModelIndex]) -> None:
        with BusyCursor():
            self.workspace_model.beginResetModel()
            for index in indexes:
                if index.isValid():
                    item = index.model().getItem(index)
                    item.load()
            self.workspace_model.endResetModel()
            self.hub.broadcast(SlideLoadedMessage(self))

    def close_slides(self, indexes: [QModelIndex]) -> None:
        with BusyCursor():
            self.workspace_model.beginResetModel()
            for index in indexes:
                if index.isValid():
                    item = index.model().getItem(index)
                    item.close()
            self.workspace_model.endResetModel()
            self.hub.broadcast(SlideUnloadedMessage(self))
            QPixmapCache.clear()
            gc.collect()

    def remove_slides(self, indexes: [QModelIndex]) -> None:
        self.workspace_model.beginResetModel()
        for index in indexes:
            self.workspace_model.removeRow(index.row(), parent=index.parent())
        self.workspace_model.endResetModel()
        self.hub.broadcast(SlideRemovedMessage(self))
        QPixmapCache.clear()
        gc.collect()

    def _on_view_mode_changed(self, message: ViewModeChangedMessage):
        self.view_mode = message.mode

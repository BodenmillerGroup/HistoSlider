import os
from typing import Dict

import gc
from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QPixmapCache
from pyqtgraph import BusyCursor

from histoslider.core.decorators import catch_error
from histoslider.core.hub import Hub
from histoslider.core.message import CheckedChannelChangedMessage, SlideImportedMessage, SlideRemovedMessage, \
    SlideUnloadedMessage, SlideLoadedMessage, CheckedChannelsChangedMessage
from histoslider.models.channel import Channel
from histoslider.slides.mcd.mcd_slide import McdSlide
from histoslider.models.workspace_model import WorkspaceModel
from histoslider.slides.ome_tiff.ome_tiff_slide import OmeTiffSlide
from histoslider.slides.tiff.tiff_slide import TiffSlide


class DataManager:
    workspace_model: WorkspaceModel = None
    hub: Hub = None
    checked_channels: Dict[str, Channel] = dict()

    def __init__(self):
        if DataManager.workspace_model and DataManager.hub:
            return
        DataManager.workspace_model = WorkspaceModel()
        DataManager.hub = Hub()
        DataManager.workspace_model.show_item_changed.connect(DataManager._on_show_item_changed)

    @staticmethod
    def load_workspace(path: str) -> None:
        with BusyCursor():
            DataManager.checked_channels.clear()
            DataManager.workspace_model.beginResetModel()
            DataManager.workspace_model.load_workspace(path)
            DataManager.workspace_model.endResetModel()

    @staticmethod
    def save_workspace(path: str) -> None:
        with BusyCursor():
            DataManager.workspace_model.save_workspace(path)

    @staticmethod
    def _on_show_item_changed(item: Channel) -> None:
        if item.checked:
            if item.name not in DataManager.checked_channels:
                DataManager.checked_channels[item.name] = item
        else:
            if item.name in DataManager.checked_channels:
                DataManager.checked_channels.pop(item.name)
        DataManager.hub.broadcast(CheckedChannelChangedMessage(DataManager, item))
        DataManager.hub.broadcast(CheckedChannelsChangedMessage(DataManager, DataManager.checked_channels))

    @staticmethod
    # @catch_error("Could not import slide")
    def import_slide(file_path: str) -> None:
        with BusyCursor():
            filename, file_extension = os.path.splitext(file_path)
            if file_extension == '.mcd':
                slide = McdSlide(file_path)
            elif file_extension == '.tiff' or file_extension == '.tif':
                if filename.endswith('.ome'):
                    slide = OmeTiffSlide(file_path)
                else:
                    slide = TiffSlide(file_path)
            else:
                slide = TiffSlide(file_path)
            DataManager.workspace_model.beginResetModel()
            DataManager.workspace_model.workspace_data.add_slide(slide)
            DataManager.workspace_model.endResetModel()
            DataManager.checked_channels.clear()
            QPixmapCache.clear()
            DataManager.hub.broadcast(SlideImportedMessage(DataManager))

    @staticmethod
    # @catch_error("Could not load slide")
    def load_slides(indexes: [QModelIndex]) -> None:
        with BusyCursor():
            DataManager.workspace_model.beginResetModel()
            for index in indexes:
                if index.isValid():
                    item = index.model().getItem(index)
                    item.load()
            DataManager.workspace_model.endResetModel()
            DataManager.hub.broadcast(SlideLoadedMessage(DataManager))

    @staticmethod
    @catch_error("Could not unload slide")
    def unload_slides(indexes: [QModelIndex]) -> None:
        with BusyCursor():
            DataManager.workspace_model.beginResetModel()
            for index in indexes:
                if index.isValid():
                    item = index.model().getItem(index)
                    item.unload()
            DataManager.workspace_model.endResetModel()
            DataManager.hub.broadcast(SlideUnloadedMessage(DataManager))
            DataManager.checked_channels.clear()
            QPixmapCache.clear()
            gc.collect()

    @staticmethod
    @catch_error("Could not delete slide(s)")
    def delete_slides(indexes: [QModelIndex]) -> None:
        DataManager.workspace_model.beginResetModel()
        for index in indexes:
            DataManager.workspace_model.removeRow(index.row(), parent=index.parent())
        DataManager.workspace_model.endResetModel()
        DataManager.hub.broadcast(SlideRemovedMessage(DataManager))
        DataManager.checked_channels.clear()
        QPixmapCache.clear()
        gc.collect()

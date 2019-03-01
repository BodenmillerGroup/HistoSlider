from functools import partial

from PyQt5.QtCore import Qt, QModelIndex, QItemSelection
from PyQt5.QtWidgets import QTreeView, QWidget, QAbstractItemView, QMenu

from histoslider.core.message import TreeViewCurrentItemChangedMessage
from histoslider.core.data_manager import DataManager
from histoslider.models.slide import Slide


class WorkspaceTreeView(QTreeView):
    def __init__(self, parent: QWidget = None):
        QTreeView.__init__(self, parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setModel(DataManager.workspace_model)
        self.customContextMenuRequested.connect(self._open_menu)
        self.selectionModel().selectionChanged.connect(self._treeview_selection_changed)
        self.selectionModel().currentChanged.connect(self._treeview_current_changed)
        self.doubleClicked.connect(self._treeview_double_clicked)

    def _open_menu(self, position):
        indexes = self.selectedIndexes()

        level = None
        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1

        menu = QMenu(self)

        if level == 1:
            action = menu.addAction("Load slide")
            action.triggered.connect(partial(self._load_slides, indexes))

            action = menu.addAction("Unload slide")
            action.triggered.connect(partial(self._unload_slides, indexes))

            action = menu.addAction("Delete slide")
            action.triggered.connect(partial(self._delete_slides, indexes))
        elif level == 2:
            menu.addAction("Edit object/container")
        elif level == 3:
            menu.addAction("Edit object")

        menu.exec_(self.viewport().mapToGlobal(position))

    def _unload_slides(self, indexes: [QModelIndex]):
        DataManager.unload_slides(indexes)

    def _load_slides(self, indexes: [QModelIndex]):
        DataManager.load_slides(indexes)

    def _delete_slides(self, indexes: [QModelIndex]):
        DataManager.delete_slides(indexes)

    def _treeview_current_changed(self, current: QModelIndex, previous: QModelIndex):
        if current.isValid():
            item = current.model().getItem(current)
            DataManager.hub.broadcast(TreeViewCurrentItemChangedMessage(self, item))

    def _treeview_selection_changed(self, selected: QItemSelection, deselected: QItemSelection):
        indexes = selected.indexes()

    def _treeview_double_clicked(self, index: QModelIndex):
        if index.isValid():
            item = index.model().getItem(index)
            if isinstance(item, Slide) and not item.loaded:
                DataManager.load_slides([index])

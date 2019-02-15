from functools import partial

from PyQt5.QtCore import Qt, QModelIndex, QItemSelection
from PyQt5.QtWidgets import QTreeView, QWidget, QAbstractItemView, QMenu, QAction

from histoslider.core.message import TreeViewCurrentItemChangedMessage
from histoslider.core.data_manager import DataManager


class WorkspaceTreeView(QTreeView):
    def __init__(self, parent: QWidget = None):
        QTreeView.__init__(self, parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setModel(DataManager.workspace_model)
        self.customContextMenuRequested.connect(self.open_menu)
        self.selectionModel().selectionChanged.connect(self._treeview_selection_changed)
        self.selectionModel().currentChanged.connect(self._treeview_current_changed)

    def open_menu(self, position):
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
            action = QAction("Delete slide", menu)
            action.triggered.connect(partial(self.delete_slides, indexes))
            menu.addAction(action)
        elif level == 2:
            menu.addAction("Edit object/container")
        elif level == 3:
            menu.addAction("Edit object")

        menu.exec_(self.viewport().mapToGlobal(position))

    def delete_slides(self, indexes: [QModelIndex]):
        DataManager.delete_slides(indexes)

    def _treeview_current_changed(self, current: QModelIndex, previous: QModelIndex):
        if current.isValid():
            item = current.model().getItem(current)
            DataManager.hub.broadcast(TreeViewCurrentItemChangedMessage(self, item))

    def _treeview_selection_changed(self, selected: QItemSelection, deselected: QItemSelection):
        indexes = selected.indexes()

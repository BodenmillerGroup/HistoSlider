import os

import psutil
from PyQt5.QtCore import Qt, QTimer, QSettings, QByteArray
from PyQt5.QtGui import QPixmapCache
from PyQt5.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QLabel,
    QApplication,
    QDialog)

from histoslider.core.decorators import catch_error
from histoslider.core.message import SlideImportedMessage
from histoslider.image.mcd_loader import McdLoader
from histoslider.image.slide_image_view import SlideImageView
from histoslider.image.tiff_loader import TiffLoader
from histoslider.models.data_manager import DataManager
from histoslider.ui.main_window_ui import Ui_MainWindow
from histoslider.ui.workspace_tree_view import WorkspaceTreeView


class MainWindow(QMainWindow, Ui_MainWindow):
    """Main Window."""

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.process = psutil.Process(os.getpid())
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.ui_timer = QTimer(self)
        self.ui_timer.timeout.connect(self.update_memory_usage)
        self.ui_timer.start(1000)

        self.memory_usage_label = QLabel()
        self.statusBar.addPermanentWidget(self.memory_usage_label)

        self.workspace_tree_view = WorkspaceTreeView(self.dockWidgetContentsOverview)
        self.verticalLayoutOverview.addWidget(self.workspace_tree_view)

        self.viewer = SlideImageView(self)

        self.tabWidget.addTab(self.viewer, "Blend")

        self.actionImportSlide.triggered.connect(self.import_slide_dialog)
        self.actionOpenWorkspace.triggered.connect(self.load_workspace_dialog)
        self.actionSaveWorkspace.triggered.connect(self.save_workspace_dialog)
        self.actionExit.triggered.connect(lambda: QApplication.exit())

        self.load_settings()

    def load_settings(self):
        settings = QSettings()
        self.restoreGeometry(settings.value("MainWindow/Geometry", QByteArray()))
        self.restoreState(settings.value("MainWindow/State", QByteArray()))

    def save_settings(self):
        settings = QSettings()
        settings.setValue("MainWindow/Geometry", self.saveGeometry())
        settings.setValue("MainWindow/State", self.saveState())

    def load_workspace_dialog(self):
        options = QFileDialog.Options()
        file_ext = "*.json"
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Workspace",
            "",
            "Workspace Files ({})".format(file_ext),
            options=options,
        )
        if file_path:
            DataManager.load_workspace(file_path)

    def save_workspace_dialog(self):
        file_ext = "*.json"
        dialog = QFileDialog(self)
        dialog.setDefaultSuffix(".json")
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setWindowTitle("Save Workspace")
        dialog.setNameFilter("Workspace Files ({})".format(file_ext))
        if dialog.exec() == QDialog.Accepted:
            DataManager.save_workspace(dialog.selectedFiles()[0])

    def update_memory_usage(self):
        # return the memory usage in MB
        mem = self.process.memory_info()[0] / float(2 ** 20)
        self.memory_usage_label.setText(f"Memory usage: {mem:.2f} Mb")

    @catch_error("Could not import slide")
    def import_slide(self, file_path: str):
        filename, file_extension = os.path.splitext(file_path)
        if file_extension == '.mcd':
            loader = McdLoader(file_path)
            slide = loader.load()
        elif file_extension == '.tiff' or file_extension == '.tif':
            loader = TiffLoader(file_path)
            slide = loader.load()
        else:
            loader = TiffLoader(file_path)
            slide = loader.load()
        DataManager.workspace_model.beginResetModel()
        DataManager.workspace_model.workspace_data.add_slide(slide)
        DataManager.workspace_model.endResetModel()
        QPixmapCache.clear()
        DataManager.hub.broadcast(SlideImportedMessage(self))

    def import_slide_dialog(self):
        options = QFileDialog.Options()
        file_ext_strings = ["*.mcd", "*.tiff", "*.tif"]
        file_ext_string = " ".join(file_ext_strings)
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select whole-slide image to view",
            "",
            "Whole-slide images ({});;".format(file_ext_string),
            options=options,
        )
        if file_path:
            self.import_slide(file_path)

    @property
    def okToQuit(self):
        return True

    def closeEvent(self, event):
        if self.okToQuit:
            self.save_settings()

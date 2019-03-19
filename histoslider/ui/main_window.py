import os

import psutil
from PyQt5.QtCore import Qt, QTimer, QSettings, QByteArray
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QLabel,
    QApplication,
    QDialog, QComboBox)

from histoslider.core.manager import Manager
from histoslider.core.message import ViewModeChangedMessage
from histoslider.core.view_mode import ViewMode
from histoslider.ui.blend_view_widget import BlendViewWidget
from histoslider.ui.channels_view_widget import ChannelsViewWidget
from histoslider.ui.histograms_view import HistogramsView
from histoslider.ui.info_widget import InfoWidget
from histoslider.ui.main_window_ui import Ui_MainWindow
from histoslider.ui.origin_view_widget import OriginViewWidget
from histoslider.ui.settings_widget import SettingsWidget
from histoslider.ui.tiles_view_widget import TilesViewWidget
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

        self.info_widget = InfoWidget(self.dockWidgetContentsOverview)
        self.verticalLayoutInfo.addWidget(self.info_widget)

        self.channels_view_widget = ChannelsViewWidget(self.dockWidgetContentsChannels)
        self.verticalLayoutChannels.addWidget(self.channels_view_widget)

        # self.origin_view_widget = OriginViewWidget(self)
        # self.tabWidget.addTab(self.origin_view_widget, QIcon(":/icons/icons8-eukaryotic-cells-16.png"), "Origin")

        self.blend_view_widget = BlendViewWidget(self)
        self.tabWidget.addTab(self.blend_view_widget, QIcon(":/icons/icons8-eukaryotic-cells-16.png"), "Blend")

        self.tiles_view_widget = TilesViewWidget(self)
        self.tabWidget.addTab(self.tiles_view_widget, QIcon(":/icons/icons8-medium-icons-16.png"), "Tiles")

        self.settings_widget = SettingsWidget(self.dockWidgetContentsSettings, self.blend_view_widget.blend_view)
        self.verticalLayoutSettings.addWidget(self.settings_widget)

        self.actionImportSlide.triggered.connect(self.import_slide_dialog)
        self.actionOpenWorkspace.triggered.connect(self.load_workspace_dialog)
        self.actionSaveWorkspace.triggered.connect(self.save_workspace_dialog)
        self.actionExit.triggered.connect(lambda: QApplication.exit())

        label = QLabel("Mode:")
        self.toolBar.addWidget(label)

        mode_combo_box = QComboBox()
        mode_combo_box.addItems([e.value for e in ViewMode])
        mode_combo_box.currentTextChanged.connect(self._mode_current_text_changed)
        self.toolBar.addWidget(mode_combo_box)

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
        file_ext = "*.workspace"
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Workspace",
            "",
            "Workspace Files ({})".format(file_ext),
            options=options,
        )
        if file_path:
            Manager.load_workspace(file_path)

    def save_workspace_dialog(self):
        file_ext = "*.workspace"
        dialog = QFileDialog(self)
        dialog.setDefaultSuffix(".workspace")
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setWindowTitle("Save Workspace")
        dialog.setNameFilter("Workspace Files ({})".format(file_ext))
        if dialog.exec() == QDialog.Accepted:
            Manager.save_workspace(dialog.selectedFiles()[0])

    def update_memory_usage(self):
        # return the memory usage in MB
        mem = self.process.memory_info()[0] / float(2 ** 20)
        self.memory_usage_label.setText(f"Memory usage: {mem:.2f} Mb")

    def import_slide(self, file_path: str):
        Manager.import_slide(file_path)

    def import_slide_dialog(self):
        options = QFileDialog.Options()
        file_ext_strings = ["*.mcd", "*.tiff", "*.tif", "*.txt"]
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

    def _mode_current_text_changed(self, text: str):
        Manager.hub.broadcast(ViewModeChangedMessage(self, ViewMode(text)))

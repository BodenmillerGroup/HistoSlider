# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/anton/bblab/HistoSlider/histoslider/ui/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(845, 631)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayoutCentral = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayoutCentral.setObjectName("verticalLayoutCentral")
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayoutCentral.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 845, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.dockWidgetOverview = QtWidgets.QDockWidget(MainWindow)
        self.dockWidgetOverview.setObjectName("dockWidgetOverview")
        self.dockWidgetContentsOverview = QtWidgets.QWidget()
        self.dockWidgetContentsOverview.setObjectName("dockWidgetContentsOverview")
        self.verticalLayoutOverview = QtWidgets.QVBoxLayout(self.dockWidgetContentsOverview)
        self.verticalLayoutOverview.setObjectName("verticalLayoutOverview")
        self.dockWidgetOverview.setWidget(self.dockWidgetContentsOverview)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidgetOverview)
        self.dockWidgetSettings = QtWidgets.QDockWidget(MainWindow)
        self.dockWidgetSettings.setObjectName("dockWidgetSettings")
        self.dockWidgetContentsSettings = QtWidgets.QWidget()
        self.dockWidgetContentsSettings.setObjectName("dockWidgetContentsSettings")
        self.verticalLayoutSettings = QtWidgets.QVBoxLayout(self.dockWidgetContentsSettings)
        self.verticalLayoutSettings.setObjectName("verticalLayoutSettings")
        self.dockWidgetSettings.setWidget(self.dockWidgetContentsSettings)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidgetSettings)
        self.dockWidgetChannels = QtWidgets.QDockWidget(MainWindow)
        self.dockWidgetChannels.setObjectName("dockWidgetChannels")
        self.dockWidgetContentsChannels = QtWidgets.QWidget()
        self.dockWidgetContentsChannels.setObjectName("dockWidgetContentsChannels")
        self.verticalLayoutChannels = QtWidgets.QVBoxLayout(self.dockWidgetContentsChannels)
        self.verticalLayoutChannels.setObjectName("verticalLayoutChannels")
        self.dockWidgetChannels.setWidget(self.dockWidgetContentsChannels)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidgetChannels)
        self.actionExit = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon)
        self.actionExit.setShortcutVisibleInContextMenu(False)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionImportSlide = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/open.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionImportSlide.setIcon(icon1)
        self.actionImportSlide.setObjectName("actionImportSlide")
        self.actionOpenWorkspace = QtWidgets.QAction(MainWindow)
        self.actionOpenWorkspace.setIcon(icon1)
        self.actionOpenWorkspace.setObjectName("actionOpenWorkspace")
        self.actionSaveWorkspace = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons8-save-16.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSaveWorkspace.setIcon(icon2)
        self.actionSaveWorkspace.setObjectName("actionSaveWorkspace")
        self.dockWidgetSettings.raise_()
        self.dockWidgetChannels.raise_()
        self.menuFile.addAction(self.actionOpenWorkspace)
        self.menuFile.addAction(self.actionSaveWorkspace)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionImportSlide)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionImportSlide)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HistoSlider"))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menuHelp.setTitle(_translate("MainWindow", "&Help"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.dockWidgetOverview.setWindowTitle(_translate("MainWindow", "Overview"))
        self.dockWidgetSettings.setWindowTitle(_translate("MainWindow", "Settings"))
        self.dockWidgetChannels.setWindowTitle(_translate("MainWindow", "Channels"))
        self.actionExit.setText(_translate("MainWindow", "E&xit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionImportSlide.setText(_translate("MainWindow", "Import Slide"))
        self.actionImportSlide.setToolTip(_translate("MainWindow", "Import slide..."))
        self.actionOpenWorkspace.setText(_translate("MainWindow", "Open Workspace"))
        self.actionOpenWorkspace.setToolTip(_translate("MainWindow", "Open workspace..."))
        self.actionSaveWorkspace.setText(_translate("MainWindow", "Save Workspace"))
        self.actionSaveWorkspace.setToolTip(_translate("MainWindow", "Save workspace..."))


import resources_rc

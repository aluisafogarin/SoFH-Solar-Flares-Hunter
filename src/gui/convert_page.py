
from PyQt5.QtWidgets import (
    QApplication, QWidget, QAction, QCheckBox,
    QHBoxLayout, QGridLayout, QMenuBar, QVBoxLayout, QLabel,
    QFileDialog, QPushButton, QMenu, QMainWindow, QToolBar, QToolButton, QPlainTextEdit, QProgressBar, QTextEdit)

from PyQt5 import QtGui
from PyQt5.Qt import *

import sys
import os


class ConvertWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Layout
        self.main_layout = QVBoxLayout()
        self.grid = QGridLayout()

        # self.paths = path_mapper.PathMapper()

        self.setWindowTitle("Convert Images")

        self.resize(1000, 650)

        self.createToolBar()
        self.createMenuBar()
        self.createCentralWidget()

        text = QLabel("Convert Images")
        text.setStyleSheet("font-size: 16px; font-weight: bold")
        self.grid.addWidget(text, 0, 0)

        button_images = QToolButton()
        button_images.clicked.connect(self.getImagesToConvert)
        self.createSelectImagesConvert(1, 0)
        self.grid.addWidget(button_images, 1, 1)

        self.createFolderNameField(2, 0)
        button_folder = QToolButton()
        button_folder.clicked.connect(self.getOutputFolderDirectory)
        self.grid.addWidget(button_folder, 2, 1)

        self.main_layout.addLayout(self.grid)

    def createCentralWidget(self):
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)

        self.setCentralWidget(central_widget)

    # TODO Refactor menu bar
    def createMenuBar(self):
        self.menu_bar = self.menuBar()

        file_menu = self.menu_bar.addMenu("File")
        settings_menu = self.menu_bar.addMenu("Settings")
        about_menu = self.menu_bar.addMenu("About")

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+E")
        exit_action.triggered.connect(lambda: QApplication.Quit())

        file_menu.addAction(exit_action)

    def createToolBar(self):
        tool_bar = self.addToolBar("Download")

        button_download = QToolButton()
        # button_download.setIcon(QtGui.QIcon(
        #     self.paths.generate_icon_path("download.png")))

        button_convert = QToolButton()
        # button_convert.setIcon(QtGui.QIcon(
        #     self.paths.generate_icon_path("convert.png")))
        # button_convert.connect()

        tool_bar.addWidget(button_download)
        tool_bar.addWidget(button_convert)

    def createSelectImagesConvert(self, x, y):
        self.images_convert = QTextEdit()
        self.images_convert.setReadOnly(True)
        self.images_convert.setFixedSize(200, 25)

        self.grid.addWidget(self.images_convert, x, y)

    def getImagesToConvert(self):
        images = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select images",
            directory=os.getcwd(),
            filter="FITS File (*.fits)",
            initialFilter="FITS File (*.fits)"
        )
        print(self.images[0])
        self.images_convert.setText(self.images[0])

    def getOutputFolderDirectory(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            caption="Select a folder to save the images"
        )

        self.folder_field.setText(directory)

        # TODO Create folder with none was selected
        if(directory.__len__() == 0):
            directory = os.getcwd()
            print(directory)

        return directory

    def createFolderNameField(self, x, y):

        self.folder_field = QTextEdit()
        self.folder_field.setReadOnly(True)
        self.folder_field.setFixedSize(200, 25)

        self.grid.addWidget(self.folder_field, x, y)

        return self.folder_field


app = QApplication(sys.argv)

window = ConvertWindow()
window.show()
sys.exit(app.exec_())

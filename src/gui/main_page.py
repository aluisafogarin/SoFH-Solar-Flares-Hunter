import os
import sys

from util import path_mapper

from model import enum

from PyQt5.QtWidgets import (
    QApplication, QWidget, QAction, QCheckBox,
    QHBoxLayout, QGridLayout, QMenuBar, QVBoxLayout, QLabel,
    QFileDialog, QPushButton, QMenu, QMainWindow, QToolBar, QToolButton, QPlainTextEdit, QProgressBar, QTextEdit)

from PyQt5 import QtGui
from PyQt5.Qt import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.paths = path_mapper.PathMapper()

        self.main_layout = QVBoxLayout()
        self.grid = QGridLayout()

        self.setWindowTitle("Software TCC")
        self.setWindowIcon(QtGui.QIcon(
            self.paths.generate_icon_path("sun_icon.png")))

        self.resize(1000, 650)

        self.createMenuBar()
        self.createCentralWidget()

        # --------------- Column 0 ---------------
        text = QLabel("Configurations")
        text.setStyleSheet("font-size: 16px; font-weight: bold")
        self.grid.addWidget(text, 0, 0)

        self.createWavelengthGroupBox(1, 0)
        self.createOutputImageGroupBox(2, 0)

        # Data file
        self.grid.addWidget(QLabel("Data file"), 3, 0, alignment=Qt.AlignTop)
        self.createFileNameField(4, 0)

        button_file = self.createIconButtonGrid("csv_file.png")
        button_file.clicked.connect(self.getFileName)

        # Output folder
        self.grid.addWidget(QLabel("Output folder"), 5,
                            0, alignment=Qt.AlignTop)
        self.createFolderNameField(6, 0)
        button_folder = self.createIconButtonGrid("folder.png")
        button_folder.clicked.connect(self.getDownloadImagesDirectory)

        # --------------- Column 1 ---------------
        self.createLogArea(3, 1)
        self.grid.addWidget(button_file, 4, 1, alignment=Qt.AlignLeft)
        self.createProgressBar(5, 1)
        self.grid.addWidget(button_folder, 6, 1, alignment=Qt.AlignLeft)

        self.createToolBar()
        self.main_layout.addLayout(self.grid)

    def createCentralWidget(self):
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)

        self.setCentralWidget(central_widget)

    def createIconButtonGrid(self, icon):
        button = QToolButton()
        button.setIcon(QtGui.QIcon(self.paths.generate_icon_path(icon)))

        return button

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
        button_download.setIcon(QtGui.QIcon(
            self.paths.generate_icon_path("download.png")))

        button_convert = QToolButton()
        button_convert.setIcon(QtGui.QIcon(
            self.paths.generate_icon_path("convert.png")))

        tool_bar.addWidget(button_download)
        tool_bar.addWidget(button_convert)

    def createWavelengthGroupBox(self, x, y):
        layout = QVBoxLayout()

        label = QLabel()
        label.setText("Wavelengths:")
        layout.addWidget(label)

        for wavelength in enum.Wavelenghts:
            wavelength_group_box = QCheckBox(wavelength.value)
            layout.addWidget(wavelength_group_box)
        self.grid.addLayout(layout, x, y)

    def createOutputImageGroupBox(self, x, y):
        layout = QVBoxLayout()

        label = QLabel()
        label.setText("Image format:")
        layout.addWidget(label)

        for extension in enum.ExtensionImages:
            extension_group_box = QCheckBox(extension.value)
            layout.addWidget(extension_group_box)
        self.grid.addLayout(layout, x, y)

    def getFileName(self):
        file_filter = "Data File (*.csv)"
        file = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select a csv file",
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter=file_filter
        )
        print(file[0])
        return file[0]

    def createFileNameField(self, x, y):

        folder_field = QTextEdit()
        folder_field.setReadOnly(True)
        folder_field.setFixedSize(200, 25)

        self.grid.addWidget(folder_field, x, y)

        return folder_field

    def getDownloadImagesDirectory(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            caption="Select a folder"
        )

        print(directory)
        return directory

    def createFolderNameField(self, x, y):

        folder_field = QTextEdit()
        folder_field.setReadOnly(True)
        folder_field.setFixedSize(200, 25)

        self.grid.addWidget(folder_field, x, y)

        return folder_field

    def getConvertImagesDirectory(self):
        pass

    def createLogArea(self, x, y):
        text_area = QPlainTextEdit()
        text_area.insertPlainText("Log information")
        text_area.setReadOnly(True)
        text_area.setFixedSize(450, 300)
        self.grid.addWidget(text_area, x, y, alignment=Qt.AlignCenter)

    def createProgressBar(self, x, y):
        progress_bar = QProgressBar()
        progress_bar.setFixedWidth(450)
        self.grid.addWidget(progress_bar, x, y, alignment=Qt.AlignCenter)


app = QApplication(sys.argv)

window = MainWindow()
window.show()
sys.exit(app.exec_())

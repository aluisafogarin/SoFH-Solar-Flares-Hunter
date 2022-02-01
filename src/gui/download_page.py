import os
import sys

from util import path_mapper

from model import enum

from util import download_images

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

        # Layout
        self.main_layout = QVBoxLayout()
        self.grid = QGridLayout()

        # General configurations
        self.setWindowTitle("Software TCC")
        self.setWindowIcon(QtGui.QIcon(
            self.paths.generate_icon_path("sun_icon.png")))
        self.resize(1000, 650)

        # Tool bar and menu
        self.createToolBar()
        self.createMenuBar()
        self.createCentralWidget()

        # Configurations of download
        text = QLabel("Configurations")
        text.setStyleSheet("font-size: 16px; font-weight: bold")
        self.grid.addWidget(text, 0, 0)

        self.createWavelengthGroupBox(1, 0)

        self.createOutputImageGroupBox(2, 0)

        # Data file
        self.grid.addWidget(QLabel("Data file"), 4, 0, alignment=Qt.AlignTop)
        self.createFileNameField(5, 0)

        button_file = self.createIconButtonGrid("csv_file.png")
        button_file.clicked.connect(self.getFileName)
        self.grid.addWidget(button_file, 5, 1, alignment=Qt.AlignLeft)

        # Output folder
        self.grid.addWidget(QLabel("Output folder"), 6,
                            0, alignment=Qt.AlignTop)
        self.createFolderNameField(7, 0)
        button_folder = self.createIconButtonGrid("folder.png")
        button_folder.clicked.connect(self.getDownloadImagesDirectory)
        self.grid.addWidget(button_folder, 7, 1, alignment=Qt.AlignLeft)

        # Download button
        button_download = QPushButton("Start download", self)
        #button_download.clicked.connect(downloadImages("teste.csv", ))

        self.grid.addWidget(button_download, 8, 0)

        # Control buttons
        button_play_pause = self.createIconButtonGrid("play_pause.png")
        button_cancel = self.createIconButtonGrid("cancel.png")

        self.grid.addWidget(button_play_pause, 8, 2)
        self.grid.addWidget(button_cancel, 8, 3)

        # Log and progress bar
        self.createProgressBar(8, 1)
        self.createLogArea(9, 1)

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
        vbox = QVBoxLayout()

        groupbox = QGroupBox("Wavelenghts:")
        groupbox.setLayout(vbox)

        self.wavelenght_checkbox = []

        for wavelenght in enum.Wavelenghts:
            self.wavelenght_checkbox.append(QCheckBox(wavelenght.value))

        for checkbox in self.wavelenght_checkbox:
            checkbox.clicked.connect(self.wavelenghtSelected)
            vbox.addWidget(checkbox)

        self.grid.addWidget(groupbox, x, y)

    def wavelenghtSelected(self):
        for checkbox in self.wavelenght_checkbox:
            if(checkbox.isChecked()):
                print(checkbox.text())

    def createOutputImageGroupBox(self, x, y):
        vbox = QVBoxLayout()

        groupbox = QGroupBox("Image format:")
        groupbox.setLayout(vbox)

        self.output_image_checkbox = []

        for extension in enum.ExtensionImages:
            self.output_image_checkbox.append(
                QCheckBox(extension.value))

        for checkbox in self.output_image_checkbox:
            checkbox.clicked.connect(self.outputImageSelected)
            vbox.addWidget(checkbox)

        self.grid.addWidget(groupbox, x, y)

    def outputImageSelected(self):
        for checkbox in self.output_image_checkbox:
            if(checkbox.isChecked()):
                print(checkbox.text())

    def getFileName(self):
        file_filter = "Data File (*.csv)"
        file = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select a csv file",
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter=file_filter
        )

        self.file_field.setText(file[0])

        return file[0]

    def createFileNameField(self, x, y):

        self.file_field = QTextEdit()
        self.file_field.setReadOnly(True)
        self.file_field.setFixedSize(200, 25)

        self.grid.addWidget(self.file_field, x, y)

        return self.file_field

    def getDownloadImagesDirectory(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            caption="Select a folder"
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

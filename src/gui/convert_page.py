import os
import sys

from util import path_mapper

from model import enum

from util import convert_images

import logging

from PyQt5.QtWidgets import (
    QApplication, QWidget, QAction, QCheckBox,
    QHBoxLayout, QGridLayout, QMenuBar, QVBoxLayout, QLabel,
    QFileDialog, QPushButton, QMenu, QMainWindow, QToolBar, QToolButton, QPlainTextEdit, QProgressBar, QTextEdit)

from PyQt5 import QtGui
from PyQt5.Qt import *

import sys
import os


class ConvertWorker(QObject):
    finished = pyqtSignal()
    logging = pyqtSignal(int)
    error = pyqtSignal(str)
    warning = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(ConvertWorker, self).__init__()
        self.args = args
        self.kwargs = kwargs

    def run(self):
        c = convert_images.Convert()
        c.convert_images(self.args[0])


class ConvertWindow(QMainWindow):
    def __init__(self, configuration, parent=None):
        super(ConvertWindow, self).__init__(parent)

        self.paths = path_mapper.PathMapper()
        self.configuration = configuration.ConfigurationConversion()
        self.control = configuration.ControlConversion()

        # Layout
        self.main_layout = QVBoxLayout()
        self.grid = QGridLayout()

        # General configurations
        self.setWindowTitle("Software TCCs")
        self.setWindowIcon(QtGui.QIcon(
            self.paths.generate_icon_path("sun_icon.png")))
        self.resize(1000, 650)

        # Tool bar and menu bar
        self.create_tool_bar()
        self.create_menu_bar()
        self.create_central_widget()

        # Conversion configurations
        text = QLabel("Configurations")
        text.setStyleSheet("font-size: 16px; font-weight: bold")
        self.grid.addWidget(text, 0, 0)

        # Select images
        self.grid.addWidget(
            QLabel("Define image(s) to convert"), 1, 0, alignment=Qt.AlignTop)
        self.create_select_images_convert(2, 0)

        button_images = self.create_icon_button_grid("images.png")
        button_images.clicked.connect(self.get_images_to_convert)
        self.grid.addWidget(button_images, 2, 1, alignment=Qt.AlignLeft)

        # Select output folder
        self.grid.addWidget(QLabel("Output folder"), 3,
                            0, alignment=Qt.AlignTop)
        self.create_folder_name_field(4, 0)
        button_folder = self.create_icon_button_grid("folder.png")
        button_folder.clicked.connect(self.get_output_folder_directory)
        self.grid.addWidget(button_folder, 4, 1, alignment=Qt.AlignLeft)

        # Image format
        self.create_image_format_combo_box(5, 0)
        self.create_wavelength_group_box(6, 0)

        self.button_load_images = QPushButton("Load Images", self)
        self.button_load_images.clicked.connect(self.load_images)
        self.grid.addWidget(self.button_load_images, 7, 0)

        self.create_images_area(8, 1)

        self.button_convert_images = QPushButton("Convert Images", self)
        self.button_convert_images.clicked.connect(self.convert_images)
        self.grid.addWidget(self.button_convert_images, 9, 1)

        self.main_layout.addLayout(self.grid)

    def create_central_widget(self):
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)

        self.setCentralWidget(central_widget)

    # TODO Refactor menu bar
    def create_menu_bar(self):
        self.menu_bar = self.menuBar()

        file_menu = self.menu_bar.addMenu("File")
        settings_menu = self.menu_bar.addMenu("Settings")
        about_menu = self.menu_bar.addMenu("About")

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+E")
        exit_action.triggered.connect(lambda: QApplication.Quit())

        file_menu.addAction(exit_action)

    def create_tool_bar(self):
        tool_bar = self.addToolBar("Download")

        button_download = QToolButton()
        button_download.setIcon(QtGui.QIcon(
            self.paths.generate_icon_path("download.png")))

        button_convert = QToolButton()
        button_convert.setIcon(QtGui.QIcon(
            self.paths.generate_icon_path("convert.png")))

        tool_bar.addWidget(button_download)
        tool_bar.addWidget(button_convert)

    def create_select_images_convert(self, x, y):
        self.images_convert = QTextEdit()
        self.images_convert.setReadOnly(True)
        self.images_convert.setFixedSize(200, 25)

        self.grid.addWidget(self.images_convert, x, y)

    def get_images_to_convert(self):
        images = QFileDialog.getOpenFileNames(
            parent=self,
            caption="Select images",
            directory=os.getcwd(),
            filter="FITS File (*.fits)",
            initialFilter="FITS File (*.fits)"
        )

        for image in images[0]:
            self.configuration.load_images[os.path.basename(image)] = image

    def get_output_folder_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            caption="Select a folder to save the images"
        )

        self.configuration.path_save_images = directory
        self.folder_field.setText(directory)

        # TODO Create folder with none was selected
        if(directory.__len__() == 0):
            directory = os.getcwd()
            print(directory)

        return directory

    def create_folder_name_field(self, x, y):

        self.folder_field = QTextEdit()
        self.folder_field.setReadOnly(True)
        self.folder_field.setFixedSize(200, 25)

        self.grid.addWidget(self.folder_field, x, y)

        return self.folder_field

    def create_icon_button_grid(self, icon):
        button = QToolButton()
        button.setIcon(QtGui.QIcon(self.paths.generate_icon_path(icon)))

        return button

    def create_image_format_combo_box(self, x, y):
        vbox = QVBoxLayout()

        groupbox = QGroupBox("Image format")
        groupbox.setLayout(vbox)

        self.output_image_checkbox = []

        for image_format in enum.Conversion:
            self.output_image_checkbox.append(
                QCheckBox(image_format.value))

        for checkbox in self.output_image_checkbox:
            checkbox.clicked.connect(self.extension_selected)
            vbox.addWidget(checkbox)

        self.grid.addWidget(groupbox, x, y)

    def extension_selected(self):
        for checkbox in self.output_image_checkbox:
            if(checkbox.isChecked() and checkbox.text() not in self.configuration.extensions):
                self.configuration.extensions.append(checkbox.text())
            elif(not checkbox.isChecked() and checkbox.text() in self.configuration.extensions):
                self.configuration.extensions.remove(checkbox.text())

    def create_wavelength_group_box(self, x, y):
        vbox = QVBoxLayout()

        groupbox = QGroupBox("Wavelenghts:")
        groupbox.setLayout(vbox)

        self.wavelenght_checkbox = []

        for wavelenght in enum.Wavelenghts:
            self.wavelenght_checkbox.append(QCheckBox(wavelenght.value))

        for checkbox in self.wavelenght_checkbox:
            checkbox.clicked.connect(self.wavelenght_selected)
            vbox.addWidget(checkbox)

        self.grid.addWidget(groupbox, x, y)

    def wavelenght_selected(self):
        for checkbox in self.wavelenght_checkbox:
            if(checkbox.isChecked() and checkbox.text() not in self.configuration.wavelenghts):
                self.configuration.wavelenghts.append(checkbox.text())
            elif(not checkbox.isChecked() and checkbox.text() in self.configuration.wavelenghts):
                self.configuration.wavelenghts.remove(
                    checkbox.text())

    def create_images_area(self, x, y):
        vbox = QVBoxLayout()

        groupbox = QGroupBox("Images")
        groupbox.setLayout(vbox)

        self.images_checkbox = []

        if self.configuration.load_images:
            self.check_box_all = QCheckBox("Select All")
            self.check_box_all.setChecked(False)
            self.check_box_all.stateChanged.connect(self.on_sellect_all)
            self.images_checkbox.append(self.check_box_all)

        for image in self.configuration.load_images.keys():
            self.images_checkbox.append(QCheckBox(image))

        for checkbox in self.images_checkbox:
            checkbox.clicked.connect(self.image_selected)
            vbox.addWidget(checkbox)

        self.grid.addWidget(groupbox, x, y)

    def on_sellect_all(self, state):
        for checkbox in self.images_checkbox:
            checkbox.setCheckState(state)

    def image_selected(self):
        for checkbox in self.images_checkbox:
            if(checkbox.isChecked() and checkbox.text() not in self.configuration.convert_images_dict and checkbox.text() != "Select All"):
                self.configuration.convert_images_dict[checkbox.text(
                )] = self.configuration.load_images.get(checkbox.text())
            elif(not checkbox.isChecked() and checkbox.text() in self.configuration.convert_images_dict):
                del self.configuration.convert_images_dict[checkbox.text()]

    def load_images(self):
        self.create_images_area(7, 1)

    def convert_images(self):
        missing_parameters = []

        # TODO Add missing parameters errors/ Errors comming from convert

        self.thread = QThread()
        self.worker = ConvertWorker(self.configuration)

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

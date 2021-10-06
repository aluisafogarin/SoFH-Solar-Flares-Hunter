import os
import sys

from model import enum

from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QAction, QGroupBox, QCheckBox,
    QHBoxLayout, QGridLayout, QMenuBar, QVBoxLayout, QLabel)
from PyQt5 import QtGui


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.grid = QGridLayout()

        self.setLayout(self.grid)
        self.setWindowIcon(QtGui.QIcon("icons/sun_icon.png"))
        self.setWindowTitle("Software TCC")
        self.resize(1000, 650)

        self.createMenuBar()

        self.grid.addWidget(self.menu_bar, 0, 0)
        self.createWavelengthGroupBox()
        self.createOutputImageGroupBox()


# TODO Refactor menu bar

    def createMenuBar(self):
        self.menu_bar = QMenuBar()

        file_menu = self.menu_bar.addMenu('File')
        settings_menu = self.menu_bar.addMenu('Settings')

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+E')
        exit_action.triggered.connect(lambda: QApplication.Quit())

        file_menu.addAction(exit_action)

    def createWavelengthGroupBox(self):
        layout = QVBoxLayout()

        label = QLabel()
        label.setText("Wavelengths:")
        layout.addWidget(label)

        for wavelength in enum.Wavelenghts:
            wavelength_group_box = QCheckBox(wavelength.value)
            layout.addWidget(wavelength_group_box)
        self.grid.addLayout(layout, 1, 0)

    def createOutputImageGroupBox(self):
        layout = QVBoxLayout()

        label = QLabel()
        label.setText("Image format:")
        layout.addWidget(label)

        for extension in enum.ExtensionImages:
            extension_group_box = QCheckBox(extension.value)
            layout.addWidget(extension_group_box)
        self.grid.addLayout(layout, 2, 0)

    def createLabel(self, text):
        self.label = QLabel()
        self.label.setText(text)


# root = QApplication(sys.argv)
app = QApplication(sys.argv)
win = MainWindow()
# app = Window()
win.show()
sys.exit(app.exec_())

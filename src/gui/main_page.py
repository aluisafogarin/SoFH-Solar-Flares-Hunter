import os
import sys

from model import enum

from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QAction, QGroupBox, QCheckBox, QHBoxLayout, QGridLayout, QMenuBar, QVBoxLayout)
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
        # self.grid.addWidget(self.wavelength_group_box, 1, 0)

    def createMenuBar(self):
        self.menu_bar = QMenuBar()

        file_menu = self.menu_bar.addMenu('File')
        settings_menu = self.menu_bar.addMenu('Settings')

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+E')
        exit_action.triggered.connect(lambda: QApplication.Quit())

        file_menu.addAction(exit_action)

    def createWavelengthGroupBox(self):
        layout = QHBoxLayout()
        x = 2

        for wavelength in enum.Wavelenghts:
            self.wavelength_group_box = QCheckBox(wavelength.value)
            self.grid.addWidget(self.wavelength_group_box, x, 0)
            x += 1


# root = QApplication(sys.argv)
app = QApplication(sys.argv)
win = MainWindow()
# app = Window()
win.show()
sys.exit(app.exec_())

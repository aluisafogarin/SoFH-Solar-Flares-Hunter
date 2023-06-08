import os
import sys
import logging

from PyQt5.QtWidgets import (
    QApplication, QWidget, QAction, QCheckBox, QGridLayout, QVBoxLayout, QLabel, QGroupBox, QListView,
    QFileDialog, QPushButton, QMainWindow, QToolButton, QPlainTextEdit, QTextEdit, QMessageBox, QScrollArea, QListWidget, QListWidgetItem)

from PyQt5 import QtGui, QtCore
from PyQt5.Qt import Qt
from PyQt5.QtCore import QObject, QThread, pyqtSignal


from util import path_mapper
from model import enum
from util import convert_images
from gui import download_page
from util.util import clear_log


class ConvertWorker(QObject):
    """
    Multi-thread conversion
    """

    finished = pyqtSignal()
    logging = pyqtSignal(int)
    error = pyqtSignal(str)
    warning = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(ConvertWorker, self).__init__()
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """
        Run thread
        """

        convert = convert_images.Convert()
        convert.convert_images(self.args[0], self)


class ConvertWindow(QMainWindow):
    """
    Creates main window conversion
    """

    def __init__(self, configuration, parent=None):
        """ Class constructor """
        super(ConvertWindow, self).__init__(parent)

        self.logger = logging.getLogger(enum.Files.LOG_CONVERT.value)

        # Control
        self.paths = path_mapper.PathMapper()
        self.obj_configuration = configuration
        self.configuration = configuration.ConfigurationConversion()
        self.control = configuration.ControlConversion()

        # General configurations
        self.setWindowTitle("Solar Flares Hunter (SoFH)")
        self.setWindowIcon(QtGui.QIcon(self.paths.generate_icon_path("sun_icon.png")))
        self.resize(1000, 650)
        
        # Layout
        self.main_layout = QVBoxLayout()
        self.grid = QGridLayout()

        # Tool bar and menu bar
        self.create_tool_bar()
        self.create_menu_bar()
        self.create_central_widget()

        # Conversion configurations
        text = QLabel("Configurations")
        text.setStyleSheet("font-size: 16px; font-weight: bold")
        self.grid.addWidget(text, 0, 0, alignment=Qt.AlignTop)

        # Log area
        self.create_log_area(0, 2)

        button_clear_log = QPushButton("Clear log", self)
        button_clear_log.setFixedWidth(150)
        button_clear_log.clicked.connect(self.trigger_clear_log)
        
        self.grid.addWidget(button_clear_log, 4, 2, alignment=Qt.AlignHCenter)

        # Select images
        self.button_select_images = QPushButton("Select file(s) to convert", self)
        self.button_select_images.clicked.connect(self.get_images_to_convert)
        self.grid.addWidget(self.button_select_images, 1, 0, alignment=Qt.AlignTop)
        
        # Image format
        self.button_load_images = QPushButton("Load Images", self)
        self.button_load_images.setDisabled(True)
        self.button_load_images.clicked.connect(self.load_images)
        self.grid.addWidget(self.button_load_images, 2, 0, alignment=Qt.AlignTop)
        
        # Select output folder
        self.grid.addWidget(QLabel("Output folder"), 3, 0)
        self.create_folder_name_field(4, 0)
        button_folder = self.create_icon_button_grid("folder.png")
        button_folder.clicked.connect(self.get_output_folder_directory)
        self.grid.addWidget(button_folder, 4, 1, alignment=Qt.AlignLeft)
        
        # Convert images
        self.button_convert_images = QPushButton("Convert Images", self)
        self.button_convert_images.setDisabled(True)
        self.button_convert_images.clicked.connect(self.selection_changed)
        self.button_convert_images.clicked.connect(self.convert_images)
        self.grid.addWidget(self.button_convert_images, 6, 2)
        
        # Image area
        self.list_widget = QListWidget()
        self.list_widget.setFixedSize(450, 250)
        vbox = QVBoxLayout()
        vbox.addWidget(self.list_widget)
        self.grid.addWidget(self.list_widget, 5, 2)
        
        self.main_layout.addLayout(self.grid)
    
    def selection_changed(self): 
        """ Saves when image is selected to be converted """
        
        for index in range(len(self.configuration.load_images.keys())):
            if self.list_widget.item(index).checkState() == Qt.Checked and self.list_widget.item(index).text() not in self.configuration.images_to_convert:
                self.configuration.images_to_convert[self.list_widget.item(index).text()] = self.configuration.load_images.get(self.list_widget.item(index).text())
            elif self.list_widget.item(index).checkState() == Qt.Unchecked and self.list_widget.item(index).text() in self.configuration.images_to_convert:
                del self.configuration.images_to_convert[self.list_widget.item(index).text()]
        
        
    def add_image_to_list(self):
        """ Add image to QListWidget """
            
        for image in self.configuration.load_images.keys():
            item = QListWidgetItem(image)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.list_widget.addItem(item)

    def create_log_area(self, x, y):
        """
        Creates log widget

        Args:
            x (int): Position of widget in axis x
            y (int): Position of widget axis y
        """

        self.log_area = QPlainTextEdit()
        self.log_area.insertPlainText(self.load_log_file())
        self.log_area.setReadOnly(True)
        self.log_area.setFixedSize(450, 300)
        self.grid.addWidget(self.log_area, x, y, 4, 3)
        
    def trigger_clear_log(self):
        """ Triggers clear log off util class to clear log file and reload on screen"""
        
        clear_log(enum.Files.LOG_CONVERT.value)
        self.update_log()

    def load_log_file(self):
        """ Read log file """

        try:
            with open(enum.Files.LOG_CONVERT.value, 'r', encoding="utf8") as log_file:
                log = log_file.read()
                return log
        except OSError as exception:
            self.convert_log.critical(exception)

    def create_central_widget(self):
        """ Creates central widget """

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)

        self.setCentralWidget(central_widget)

    def create_menu_bar(self):
        """ Creates menu bar widget """

        self.menu_bar = self.menuBar()

        file_menu = self.menu_bar.addMenu("File")

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+E")
        exit_action.triggered.connect(lambda: QApplication.Quit())

        file_menu.addAction(exit_action)

    def create_tool_bar(self):
        """ Creates tool bar widget """

        tool_bar = self.addToolBar("Download")

        button_download = QToolButton()
        button_download.setIcon(QtGui.QIcon(
            self.paths.generate_icon_path("download.png")))
        button_download.clicked.connect(
            self.open_download_window)

        button_convert = QToolButton()
        button_convert.setIcon(QtGui.QIcon(
            self.paths.generate_icon_path("convert.png")))

        tool_bar.addWidget(button_download)
        tool_bar.addWidget(button_convert)

    def open_download_window(self):
        """ Open download window action """

        self.new_window = download_page.DownloadWindow(self.obj_configuration)
        self.new_window.show()

    def create_select_images_convert(self, x, y):
        """ Creates select image area

        Args:
            x (int): Position of widget in axis x
            y (int): Position of widget axis y
        """

        self.images_convert = QTextEdit()
        self.images_convert.setReadOnly(True)
        self.images_convert.setFixedSize(200, 25)

        self.grid.addWidget(self.images_convert, x, y)

    def get_images_to_convert(self):
        """ Gets paths of images to convert """

        images = QFileDialog.getOpenFileNames(
            parent=self,
            caption="Select images",
            directory=os.getcwd(),
            filter="FITS File (*.fits)",
            initialFilter="FITS File (*.fits)"
        )

        for image in images[0]:
            self.configuration.load_images[os.path.basename(image)] = image
            
        if self.configuration.load_images.__sizeof__() > 0:
            self.button_load_images.setDisabled(False)

    def get_output_folder_directory(self):
        """ Get output folder name 

            Returns:
                directory (string): Output folder path
        """

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
        """ Creates folder name field widget

        Args:
            x (int): Position of widget in axis x
            y (int): Position of widget axis y
        """

        self.folder_field = QTextEdit()
        self.folder_field.setReadOnly(True)
        self.folder_field.setFixedSize(200, 25)

        self.grid.addWidget(self.folder_field, x, y)

        return self.folder_field

    def create_icon_button_grid(self, icon):
        """ Creates icon button

            Args:
                icon (string): Name of image icon

            Returns:
                button (object): QToolButton
        """

        button = QToolButton()
        button.setIcon(QtGui.QIcon(self.paths.generate_icon_path(icon)))

        return button

    def on_sellect_all(self, state):
        """ Creates sellect all action """

        for checkbox in self.images_checkbox:
            checkbox.setCheckState(state)

    def load_images(self):
        """ Creates image area after loading images """

        self.add_image_to_list()
        self.button_convert_images.setDisabled(False)

    def convert_images(self):
        """ Calls convert_images.py using multi-thread """
        
        self.list_widget.itemSelectionChanged.connect(self.selection_changed)

        missing_parameters = []
        

        if not self.configuration.path_save_images:
            missing_parameters.append("Path to save images")
        if not self.configuration.load_images:
            missing_parameters.append("Load images")
        if not self.configuration.images_to_convert:
            missing_parameters.append("Select images to convert")

        if missing_parameters:
            self.create_error_pop_up(
                "Missing parameters!", "Please, insert or select the following parameters: " + str(missing_parameters)[1:-1])

        # TODO Add missing parameters errors/ Errors comming from convert

        self.thread = QThread()
        self.worker = ConvertWorker(self.configuration)

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.logging.connect(self.update_log)

        self.worker.error.connect(
            lambda msg: self.create_error_pop_up("Error!", msg))

        self.worker.finished.connect(
            lambda: self.create_info_pop_up("Download complete!",
                                            "Your download was successful."))

        self.thread.start()

    def update_log(self):
        """ Read log file and update log area """

        self.log_area.clear()
        log = self.load_log_file()
        self.log_area.insertPlainText(log)
        self.log_area.verticalScrollBar().setValue(
            self.log_area.verticalScrollBar().maximum())

    def create_error_pop_up(self, title, text):
        """ Creates error pop up

        Args:
            title (string): Title of message box
            text (string): Text of message box
        """

        msg = QMessageBox()

        msg.setIcon(QMessageBox.Critical)

        msg.setWindowTitle(title)
        msg.setText(text)

        msg.exec_()

    def create_warning_pop_up(self, title, text):
        """ Creates warning pop up

        Args:
            title (string): Title of message box
            text (string): Text of message box
        """

        msg = QMessageBox()

        msg.setIcon(QMessageBox.Warning)

        msg.setWindowTitle(title)
        msg.setText(text)

        msg.exec_()
    
    def create_info_pop_up(self, title, text):
        """ Creates information pop up

        Args:
            title (string): Title of message box
            text (string): Text of message box
        """

        msg = QMessageBox()

        msg.setIcon(QMessageBox.Information)

        msg.setWindowTitle(title)
        msg.setText(text)

        msg.exec_()

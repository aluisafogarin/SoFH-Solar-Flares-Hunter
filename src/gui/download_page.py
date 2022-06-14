import os

from time import sleep

import logging

from model import enum

from gui import convert_page

from util import download_images, path_mapper

from PyQt5.QtWidgets import (
    QApplication, QWidget, QAction, QCheckBox,
    QGridLayout, QVBoxLayout, QLabel, QGroupBox,
    QFileDialog, QPushButton, QMainWindow, QToolButton, QPlainTextEdit, QTextEdit, QMessageBox)

from PyQt5 import QtGui
from PyQt5.Qt import Qt


from PyQt5.QtCore import QObject, QThread, pyqtSignal


class DownloadWorker(QObject):
    """
    Multi-thread download
    """

    finished = pyqtSignal()
    logging = pyqtSignal(int)
    error = pyqtSignal(str)
    warning = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        """ Class constructor """

        super(DownloadWorker, self).__init__()
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """
        Run thread
        """

        download = download_images.Download(self.args[0], self.args[1])
        download.download_images(self.args[0], self.args[1], self)


class DownloadWindow(QMainWindow):
    """
    Creates main window download
    """

    def __init__(self, obj_configuration, parent=None):
        """ Class constructor """

        super(DownloadWindow, self).__init__(parent)

        self.logger = logging.getLogger(enum.Files.LOG_DOWNLOAD.value)

        # Control
        self.obj_configuration = obj_configuration
        self.configuration_values = obj_configuration.ConfigurationDownload()
        self.control_values = obj_configuration.ControlDownload()
        self.paths = path_mapper.PathMapper()

        # Layout
        self.main_layout = QVBoxLayout()
        self.grid = QGridLayout()

        # General configurations
        self.setWindowTitle("Solar Flares Hunter (SoFH)")
        self.setWindowIcon(QtGui.QIcon(
            self.paths.generate_icon_path("sun_icon.png")))
        self.resize(1000, 650)

        # Tool bar and menu
        self.create_tool_bar()
        self.create_menu_bar()
        self.create_central_widget()

        # Configurations of download
        text = QLabel("Configurations")
        text.setStyleSheet("font-size: 16px; font-weight: bold")
        self.grid.addWidget(text, 0, 0)

        # Log area
        self.create_log_area(0, 2)

        # Wavelenght and output image
        self.create_wavelength_group_box(1, 0)
        self.create_output_image_group_box(2, 0)

        # Fieldnames
        self.grid.addWidget(QLabel("Insert fieldnames"),
                            3, 0, alignment=Qt.AlignTop)
        self.create_fieldnames_area(4, 0)

        # Email
        self.grid.addWidget(QLabel("Insert email"),
                            5, 0, alignment=Qt.AlignTop)
        self.email = self.create_email_field(6, 0)

        # Data file
        self.grid.addWidget(QLabel("Data file"), 7, 0, alignment=Qt.AlignTop)
        self.create_file_name_field(8, 0)

        button_file = self.create_icon_button_grid("csv_file.png")
        button_file.clicked.connect(self.get_file_name)
        self.grid.addWidget(button_file, 8, 1, alignment=Qt.AlignLeft)

        # Output folder
        self.grid.addWidget(QLabel("Output folder"), 9,
                            0, alignment=Qt.AlignTop)
        self.create_folder_name_field(10, 0)
        button_folder = self.create_icon_button_grid("folder.png")
        button_folder.clicked.connect(self.get_download_images_directory)
        self.grid.addWidget(button_folder, 10, 1, alignment=Qt.AlignLeft)

        # Download button
        self.button_download = QPushButton("Start download", self)
        self.button_download.clicked.connect(self.save_infos)
        self.button_download.clicked.connect(self.start_download)
        self.grid.addWidget(self.button_download, 11, 0)

        # Control buttons
        button_play_pause = self.create_icon_button_grid("play_pause.png")
        button_cancel = self.create_icon_button_grid("cancel.png")

        # self.grid.addWidget(button_play_pause, 12, 2)
        # self.grid.addWidget(button_cancel, 12, 3)

        self.main_layout.addLayout(self.grid)

    def save_infos(self):
        """ Save informations from gui to configuration """

        self.configuration_values.email = self.email.toPlainText()

    def start_download(self):
        """ Calls download_images.py using multi-thread """

        missing_parameters = []

        if not self.configuration_values.wavelenghts:
            missing_parameters.append("Wavelenghts")
        if not self.configuration_values.output_image_types:
            missing_parameters.append("Image type")
        if not self.configuration_values.email:
            missing_parameters.append("Email")
        if not self.configuration_values.info_file:
            missing_parameters.append("Data file")
        if not self.configuration_values.fieldnames:
            missing_parameters.append("Fieldnames")

        if missing_parameters:
            self.create_error_pop_up(
                "Missing parameters!", "Please, insert or select the following parameters: " + str(missing_parameters)[1:-1])

        else:
            self.thread = QThread()
            self.worker = DownloadWorker(
                self.configuration_values, self.control_values)

            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)

            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.logging.connect(self.update_log)

            self.worker.error.connect(
                lambda msg: self.create_error_pop_up("Error!",
                                                     msg))
            self.worker.warning.connect(
                lambda msg: self.create_warning_pop_up("Image without records!",
                                                       msg))
            self.worker.finished.connect(
                lambda: self.create_info_pop_up("Download complete!",
                                                "Your download was successful."))

            self.thread.start()

            self.button_download.setEnabled(False)
            self.thread.finished.connect(
                lambda: self.button_download.setEnabled(True))

    def create_central_widget(self):
        """ Creates central widget """

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)

        self.setCentralWidget(central_widget)

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

    def create_menu_bar(self):
        """ Creates menu bar widget """

        self.menu_bar = self.menuBar()

        file_menu = self.menu_bar.addMenu("File")
        settings_menu = self.menu_bar.addMenu("Settings")
        about_menu = self.menu_bar.addMenu("About")

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

        button_convert = QToolButton()
        button_convert.setIcon(QtGui.QIcon(
            self.paths.generate_icon_path("convert.png")))
        button_convert.clicked.connect(
            self.open_convert_window)

        tool_bar.addWidget(button_download)
        tool_bar.addWidget(button_convert)

    def open_convert_window(self):
        """ Open convert window action """

        self.new_window = convert_page.ConvertWindow(self.obj_configuration)
        self.new_window.show()

    def create_wavelength_group_box(self, x, y):
        """ Creates wavelenght group box

        Args:
            x (int): Position of widget in axis x
            y (int): Position of widget axis y
        """

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
        """ Saves wavelenght tipe selected """

        for checkbox in self.wavelenght_checkbox:
            if(checkbox.isChecked() and checkbox.text() not in self.configuration_values.wavelenghts):
                self.configuration_values.wavelenghts.append(checkbox.text())
            elif(not checkbox.isChecked() and checkbox.text() in self.configuration_values.wavelenghts):
                self.configuration_values.wavelenghts.remove(
                    checkbox.text())

    def create_output_image_group_box(self, x, y):
        """ Creates output image combo box

        Args:
            x (int): Position of widget in axis x
            y (int): Position of widget axis y
        """

        vbox = QVBoxLayout()

        groupbox = QGroupBox("Image format:")
        groupbox.setLayout(vbox)

        self.output_image_checkbox = []

        for extension in enum.ExtensionImages:
            self.output_image_checkbox.append(
                QCheckBox(extension.value))

        for checkbox in self.output_image_checkbox:
            checkbox.clicked.connect(self.output_image_selected)
            vbox.addWidget(checkbox)

        self.grid.addWidget(groupbox, x, y)

    def output_image_selected(self):
        """ Saves output tipe selected """

        for checkbox in self.output_image_checkbox:
            if(checkbox.isChecked() and checkbox.text() not in self.configuration_values.output_image_types):
                self.configuration_values.output_image_types.append(
                    checkbox.text())
            elif(not checkbox.isChecked() and checkbox.text() in self.configuration_values.output_image_types):
                self.configuration_values.output_image_types.remove(
                    checkbox.text())

    def create_fieldnames_area(self, x, y):
        """ Creates fieldnames field

            Args:
                x (int): Position of widget in axis x
                y (int): Position of widget axis y
        """

        text_area = QPlainTextEdit()
        text_area.setFixedSize(250, 25)

        # TODO Build check on csv header values from inner function
        def check_fieldnames():
            if(text_area.toPlainText() not in self.configuration_values.fieldnames):
                self.configuration_values.fieldnames.clear()
                fieldnames = text_area.toPlainText().split(",")

                for element in fieldnames:
                    self.configuration_values.fieldnames.append(element)

        tool_tip = self.create_icon_button_grid("check.png")
        tool_tip.clicked.connect(check_fieldnames)

        tool_tip.setToolTip(
            "Insert fieldnames found on input file separeted by comma (,)")

        self.grid.addWidget(text_area, x, y, alignment=Qt.AlignCenter)
        self.grid.addWidget(tool_tip, x, y + 1, alignment=Qt.AlignLeft)

    def create_email_field(self, x, y):
        """ Creates email field

            Args:
                x (int): Position of widget in axis x
                y (int): Position of widget axis y

            Returns:
                text_area (object): Widget created
        """

        text_area = QPlainTextEdit()
        text_area.setFixedSize(250, 25)
        text_area.setToolTip("Insert email ")

        self.grid.addWidget(text_area, x, y, alignment=Qt.AlignCenter)

        return text_area

    def get_file_name(self):
        """ Get file name

        Returns:
            file[0] (string): Flare file
        """

        file_filter = "Data File (*.csv)"
        file = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select a csv file",
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter=file_filter
        )

        self.file_field.setText(file[0])
        self.configuration_values.path_info_file = file[0]
        self.configuration_values.info_file = os.path.basename(file[0])

        self.configuration_values.path_valid_file = file[0][:-4] + 'valid.csv'
        self.configuration_values.valid_file = os.path.basename(file[0])[
            :-4] + 'valid.csv'

        return file[0]

    def create_file_name_field(self, x, y):
        """ Create file name field and get file

            Args:
                x (int): Position of widget in axis x
                y (int): Position of widget axis y

            Returns:
                self.file_field (string): Flare file name
        """

        self.file_field = QTextEdit()
        self.file_field.setReadOnly(True)
        self.file_field.setFixedSize(200, 25)

        self.grid.addWidget(self.file_field, x, y)

        return self.file_field

    def get_download_images_directory(self):
        """ Get donwload image folder directory 

            Returns:
                directory (string): Output folder path
        """

        directory = QFileDialog.getExistingDirectory(
            self,
            caption="Select a folder"
        )

        self.folder_field.setText(directory)

        # TODO Create folder with none was selected
        if(directory.__len__() == 0):
            directory = os.getcwd()
        self.configuration_values.path_output_folder = directory

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

    def load_log_file(self):
        """ Read log file """

        try:
            with open(enum.Files.LOG_DOWNLOAD.value, 'r', encoding="utf8") as log_file:
                log = log_file.read()
                return log
        except OSError as exception:
            self.logger.critical(exception)

    def update_log(self):
        """ Read log file and update log area """

        self.log_area.clear()
        log = self.load_log_file()
        self.log_area.insertPlainText(log)
        self.log_area.verticalScrollBar().setValue(
            self.log_area.verticalScrollBar().maximum())

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
        self.grid.addWidget(self.log_area, x, y, 6, 4, alignment=Qt.AlignLeft)

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

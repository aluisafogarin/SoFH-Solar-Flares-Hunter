"""
    Main class
    Responsible to start the gui and generate needed folders and files.
"""

import sys
import os
import logging

from PyQt5.QtWidgets import QApplication

from model import configuration, enum

from util import util, convert_images, download_images

from gui import download_page, convert_page

# Get currently directory
directory = (os.path.dirname(os.path.realpath(__file__)))

download_log = util.setup_logger(enum.Files.LOG_DOWNLOAD.value)
convert_log = util.setup_logger(enum.Files.LOG_CONVERT.value)

download_log.debug(
    "Directory where files are being created - MAIN: %s", directory)

# Creates not_found.csv when necessary
if not os.path.exists(directory + os.sep + enum.Files.NOT_FOUND_CSV.value):
    util.create_files(directory + os.sep +
                        enum.Files.NOT_FOUND_CSV.value, 'w',
                        configuration.ConfigurationDownload())
    download_log.info("Creating %s file",
                        enum.Files.NOT_FOUND_CSV.value)

if not os.path.exists(directory + os.sep + enum.Files.NOT_FOUND_BIN.value):
    util.create_files(directory + os.sep +
                        enum.Files.NOT_FOUND_BIN.value, 'wb+',
                        configuration.ConfigurationDownload())
    download_log.info("Creating %s file",
                        enum.Files.NOT_FOUND_BIN.value)
    
# Creates controlFile (control_downloads.bin) when necessary
if not os.path.exists(enum.Files.CONTROL.value):
    util.create_files(enum.Files.CONTROL.value, 'wb+',
                        configuration.ConfigurationDownload())
    download_log.info(
        "Creating %s file", enum.Files.CONTROL.value)

if not os.path.exists(directory + os.sep + enum.Folders.CONFIG.value):
    os.makedirs(directory + os.sep + enum.Folders.CONFIG.value)

app = QApplication(sys.argv)
window = download_page.DownloadWindow(configuration)
#window = convert_page.ConvertWindow(configuration)
window.show()
sys.exit(app.exec_())

info_file = sys.argv[1]
valid_file = info_file[:-4] + 'valid.csv'
operation = sys.argv[2]
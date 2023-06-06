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

# TODO Remove variables bellow after implementing GUI
# TEMPORARY VARIABLES
# path_file_control = directory + os.sep + enum.Files.CONTROL.value
# images_directory = directory + os.sep + 'images' + os.sep


def setup_logger(log_file, level=logging.INFO):
    """ Setup up different log files for download and conversion

    Args:
        log_file (string): Name of log file
    """
    formatter = logging.Formatter(
        '%(levelname)s - %(asctime)s: %(message)s')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(log_file)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


download_log = setup_logger(
    enum.Files.LOG_DOWNLOAD.value)
convert_log = setup_logger(
    enum.Files.LOG_CONVERT.value)

download_log.debug(
    "Directory where files are being created - MAIN: %s", directory)

try:
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
    window = download_page.DownloadWindow(
        configuration)
    window.show()
    sys.exit(app.exec_())
    #download_init = download_page.DownloadPage(configuration)

    # convert = convert_page.ConvertPage(
    #     configuration.ConfigurationConversion, configuration.ControlVariables())

    info_file = sys.argv[1]
    valid_file = info_file[:-4] + 'valid.csv'
    operation = sys.argv[2]

    # config = download_init.__getattribute__()

    # config = configuration.ConfigurationDownload('automatic.download.ic@gmail.com',
    #                                            ['Type', 'Year', 'Spot',
    #                                                'Start', 'Max', 'End'],
    #                                            info_file, path_file_control,
    #                                            images_directory, 'continuum')

    control = configuration.ControlDownload()

    # while operation != '1' and operation != '2':
    #     operation = input(
    #         "Please, insert 1 to download images or 2 to convert FITS to PNG and press ENTER: ")

    # if operation == '1':
    #     print("DOWNLOAD IMAGES")

    #     # Verify if the output file already exists. If it don't, than create it.
    #     if (control.new_lines == 0):
    #         util.verify_output_file(directory, valid_file, info_file, config)

    #     # Function to record only the flare infos older than 2011
    #     util.verify_date(directory, valid_file, info_file, control, config)

    #     # Creates not_found.csv when necessary
    #     if not os.path.exists(directory + os.sep + 'not_found.csv'):
    #         util.create_files(directory + os.sep +
    #                           'not_found.csv', 'w', config)

    #     if not os.path.exists(directory + os.sep + 'not_found.bin'):
    #         util.create_files(directory + os.sep +
    #                           'not_found.bin', 'wb+', config)

    #     # Creates controlFile (control_downloads.bin) when necessary
    #     if not os.path.exists(enum.Files.CONTROL.value):
    #         util.create_files(enum.Files.CONTROL.value, 'wb+', config)

    #     if config.path_save_images == '':
    #         os.mkdir(directory + os.sep + 'images')
    #         config.path_save_images = directory + os.sep + 'images'

    #     # Creates destiny folders for the files
    #     if not os.path.exists(config.path_save_images + enum.Wavelenghts.CONTINUUM.value):
    #         util.create_folders(config.path_save_images,
    #                             enum.Wavelenghts.CONTINUUM.value, config.path_save_images)

    #     if not os.path.exists(config.path_save_images + enum.Wavelenghts.AIA1600.value):
    #         util.create_folders(config.path_save_images,
    #                             enum.Wavelenghts.AIA1600.value, config.path_save_images)

    #     if not os.path.exists(config.path_save_images + enum.Wavelenghts.AIA1700.value):
    #         util.create_folders(config.path_save_images,
    #                             enum.Wavelenghts.AIA1700.value, config.path_save_images)

    #     if not os.path.exists(config.path_save_images + enum.Wavelenghts.MAGNETOGRAMS.value):
    #         util.create_folders(config.path_save_images,
    #                             enum.Wavelenghts.MAGNETOGRAMS.value, config.path_save_images)

    #     # After all the process done correctly, everything is read to start the download
    #     download_images.download_images(valid_file, config)

    # if operation == '2':
    #     convert_images.convert_images(directory, config)

except IndexError:
    logging.error(
        "Incorrect parameters when using command line." +
        "Try: >$ python download_images.py <flare_infos.csv> <number_operation>")

    print("Incorrect parameters")
    print(
        "Try: >$ python download_images.py <flare_infos.csv> <number_operation>")
    print("Number 1: Download images basead on the csv file")
    print("Number 2: Convert FITS images to PNG images")

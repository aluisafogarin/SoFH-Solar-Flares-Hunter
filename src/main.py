import sys
import os

from model import configuration
from model import enum

from util import util
from util import convert_images
from util import download_images

from gui import download_page

# Get currently directory
directory = (os.path.dirname(os.path.realpath(__file__)))

# TODO Remove variables bellow after implementing GUI
# TEMPORARY VARIABLES
path_file_control = directory + os.sep + enum.Files.CONTROL.value
images_directory = directory + os.sep + 'images' + os.sep

print('a')


# TODO Add more error handling
try:

    download_init = download_page.DownloadPage(
        configuration.ConfigurationValues())
    info_file = sys.argv[1]
    valid_file = info_file[:-4] + 'valid.csv'
    operation = sys.argv[2]

    config = download_init.__getattribute__()

    # config = configuration.ConfigurationValues('automatic.download.ic@gmail.com',
    #                                            ['Type', 'Year', 'Spot',
    #                                                'Start', 'Max', 'End'],
    #                                            info_file, path_file_control,
    #                                            images_directory, 'continuum')

    params = configuration.ControlVariables()

    while operation != '1' and operation != '2':
        operation = input(
            "Please, insert 1 to download images or 2 to convert FITS to PNG and press ENTER: ")

    if operation == '1':
        print("DOWNLOAD IMAGES")

        # Verify if the output file already exists. If it don't, than create it.
        if (params.new_lines == 0):
            util.verify_output_file(directory, valid_file, info_file, config)

        # Function to record only the flare infos older than 2011
        util.verify_date(directory, valid_file, info_file, params, config)

        # Creates not_found.csv when necessary
        if not os.path.exists(directory + os.sep + 'not_found.csv'):
            util.create_files(directory + os.sep +
                              'not_found.csv', 'w', config)

        if not os.path.exists(directory + os.sep + 'not_found.bin'):
            util.create_files(directory + os.sep +
                              'not_found.bin', 'wb+', config)

        # Creates controlFile (control_downloads.bin) when necessary
        if not os.path.exists(enum.Files.CONTROL.value):
            util.create_files(enum.Files.CONTROL.value, 'wb+', config)

        if config.path_save_images == '':
            os.mkdir(directory + os.sep + 'images')
            config.path_save_images = directory + os.sep + 'images'

        # Creates destiny folders for the files
        if not os.path.exists(config.path_save_images + enum.Wavelenghts.CONTINUUM.value):
            util.create_folders(config.path_save_images +
                                enum.Wavelenghts.CONTINUUM.value)

        if not os.path.exists(config.path_save_images + enum.Wavelenghts.AIA1600.value):
            util.create_folders(config.path_save_images +
                                enum.Wavelenghts.AIA1600.value)

        if not os.path.exists(config.path_save_images + enum.Wavelenghts.AIA1700.value):
            util.create_folders(config.path_save_images +
                                enum.Wavelenghts.AIA1700.value)

        if not os.path.exists(config.path_save_images + enum.Wavelenghts.MAGNETOGRAMS.value):
            util.create_folders(config.path_save_images +
                                enum.Wavelenghts.MAGNETOGRAMS.value)

        # After all the process done correctly, everything is read to start the download
        download_images.downloadImages(valid_file, config)

    if operation == '2':
        convert_images.convert_images(directory, config)

except IndexError:
    print("Incorrect parameters")
    print("Try: >$ python download_images.py <flare_infos.csv> <number_operation>")
    print("Number 1: Download images basead on the csv file")
    print("Number 2: Convert FITS images to PNG images")

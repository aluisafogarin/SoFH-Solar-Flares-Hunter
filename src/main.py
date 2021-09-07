import sys
import os

from model import config_infos as config
from model import flares_enum as enum

from util import util
from util import convert_images
from util import download_images

controlFile = 'controlDownloads.bin'  # Control file
# TODO Add more error handling
try:
    infoFile = sys.argv[1]
    validFile = infoFile[:-4] + 'valid.csv'
    operation = sys.argv[2]

    params = config.Params()

    # Get currently directory
    directory = (os.path.dirname(os.path.realpath(__file__)))

    while operation != '1' and operation != '2':
        operation = input(
            "Please, insert 1 to download images or 2 to convert FITS to PNG and press ENTER: ")

    if operation == '1':
        print("DOWNLOAD IMAGES")

        # Verify if the output file already exists. If it don't, than create it.
        if (params.newLines == 0):
            util.verifyOutputFile(directory, validFile, infoFile)

        # Function to record only the flare infos older than 2011
        util.verifyDate(directory, validFile, infoFile, params)

        # Creates notFound.csv when necessary
        notFoundFlares = directory + os.sep + 'notFound.csv'
        if not os.path.exists(notFoundFlares):
            util.createFiles(notFoundFlares, 'w')

        notFoundFlaresPath = directory + os.sep + 'notFound.bin'
        if not os.path.exists(notFoundFlaresPath):
            util.createFiles(notFoundFlaresPath, 'wb+')

        # Creates controlFile (controlDownloads.bin) when necessary
        fileControlPath = directory + os.sep + controlFile
        images_directory = directory + os.sep + 'images' + os.sep

        if not os.path.exists(fileControlPath):
            util.createFiles(fileControlPath, 'wb+')

        # Creates destiny folders for the files
        if not os.path.exists(images_directory + enum.Wavelenghts.CONTINUUM.value):
            util.createFolders(images_directory +
                               enum.Wavelenghts.CONTINUUM.value)

        if not os.path.exists(images_directory + enum.Wavelenghts.AIA1600.value):
            util.createFolders(images_directory +
                               enum.Wavelenghts.AIA1600.value)

        if not os.path.exists(images_directory + enum.Wavelenghts.AIA1700.value):
            util.createFolders(images_directory +
                               enum.Wavelenghts.AIA1700.value)

        # After all the process done correctly, everything is read to start the download
        download_images.downloadImages(validFile)

    if operation == '2':
        convert_images.ConvertImages(directory)

except IndexError:
    print("Incorrect parameters")
    print("Try: >$ python download_images.py <flare_infos.csv> <number_operation>")
    print("Number 1: Download images basead on the csv file")
    print("Number 2: Convert FITS images to PNG images")

import os
import sys
from os import listdir
import glob
import shutil

from astropy.io import fits
from PIL import Image
import numpy as np
from os import listdir

# TODO Add params of wavelength dinamic


def convert_images(directory):
    print("------- Converting FITS to PNG ------- ")
    path = directory + os.sep + 'continuum' + os.sep + 'x/'
    control_wave = 1  # 1 - 'continuum', 2 - 'aia1600', 3 - 'aia1700'
    control_type = 'x'
    global fits_files
    global png_files
    global fits_converted
    control = 0

    while control_wave != 4:
        if control_wave == 1:
            files = listdir(path)
            wave = 'continuum'
            vmin, vmax = float(40000), float(80000)
            control_type == 'x'
            fits_converted = 0
            fits_files = 0
            png_files = 0
            print("Converting ", wave, " images.")

        if control_wave == 2:
            wave = 'aia1600'
            files = listdir(path)
            vmin, vmax = float(0), float(1113)
            control_type == 'x'
            fits_converted = 0
            fits_files = 0
            png_files = 0
            print("Converting ", wave, " images.")

        if control_wave == 3:
            wave = 'aia1700'
            files = listdir(path)
            vmin, vmax = float(0), float(1113)
            control_type == 'x'
            fits_converted = 0
            fits_files = 0
            png_files = 0
            print("Converting ", wave, " images.")

        if control_type == 'x':
            path = directory + os.sep + wave + os.sep + control_type

        if control_type == 'm':
            path = directory + os.sep + wave + os.sep + control_type

        if control_type == 'c':
            path = directory + os.sep + wave + os.sep + control_type

        if control_type == 'b':
            path = directory + os.sep + wave + os.sep + control_type

        newPath = path + os.sep + "*.fits"
        for file in glob.glob(newPath):
            # if "fits" in file:
            fits_files += 1

        if fits_files != 0:
            print("Fits to convert:", fits_files)
            print("Converting images " + wave +
                  " type ", control_type, "to PNG.")
            print("This can take some time. Please, wait.")

            # convertToPNG(path, wave, control_type, vmax, vmin, True)
            newPath = path + os.sep + "*.fits"
            for file in glob.glob(newPath):
                hdulist = fits.open(file, ignore_missing_end=True)
                hdulist.verify('fix')
                imagem = hdulist[1]._data
                np.warnings.filterwarnings('ignore')

                # Clip data to brightness limits
                imagem[imagem > vmax] = vmax
                imagem[imagem < vmin] = vmin
                # Scale data to range [0, 1]
                imagem = (imagem - vmin)/(vmax - vmin)
                # Convert to 8-bit integer
                imagem = (255*imagem).astype(np.uint8)
                # Invert y axis
                imagem = imagem[::-1, :]

                # Create image from data array and save as png
                image = Image.fromarray(imagem)
                destino = file[:-5] + '.png'
                image.save(destino)
                fits_converted += 1
                control += 1
                print(fits_converted, "/", fits_files)

            # Move image to png folders
            newPath = path + os.sep + "*.png"
            for file in glob.glob(newPath):
                file = file.replace(path, "")
                file = file.replace(os.sep, "")
                imagePath = directory + os.sep + wave + os.sep + control_type + os.sep + file

                pngFolder = directory + os.sep + wave + os.sep + \
                    'png' + os.sep + control_type + os.sep + file
                shutil.move(imagePath, pngFolder)
                png_files += 1
                control += 1

        if fits_converted + png_files == control:

            if control_type == 'x':
                control_type = 'm'
                resetVariables(
                    [fits_converted, fits_files, png_files, control])
                #fits_converted = 0
                #fits_files = 0
                #png_files = 0
                #control = 0

            elif control_type == 'm':
                control_type = 'c'
                resetVariables(
                    [fits_converted, fits_files, png_files, control])
                #fits_converted = 0
                #fits_files = 0
                #png_files = 0
                #control = 0

            elif control_type == 'c':
                control_type = 'b'
                resetVariables(
                    [fits_converted, fits_files, png_files, control])
                #fits_converted = 0
                #fits_files = 0
                #png_files = 0
                #control = 0

            elif control_type == 'b':
                control_type = 'x'
                control_wave += 1
                resetVariables(
                    [fits_converted, fits_files, png_files, control])
                #fits_converted = 0
                #fits_files = 0
                #png_files = 0
                #control = 0

        elif fits_files == 0:
            if control_type == 'b':
                control_type = 'x'
                control_wave += 1
                resetVariables(
                    [fits_converted, fits_files, png_files, control])
                #fits_converted = 0
                #fits_files = 0
                #png_files = 0
                #control = 0

            elif control_type == 'x':
                control_type = 'm'
                resetVariables(
                    [fits_converted, fits_files, png_files, control])
                #fits_converted = 0
                #fits_files = 0
                #png_files = 0
                #control = 0

            elif control_type == 'm':
                control_type = 'c'
                resetVariables(
                    [fits_converted, fits_files, png_files, control])
                #fits_converted = 0
                #fits_files = 0
                #png_files = 0
                #control = 0

            elif control_type == 'c':
                control_type = 'b'
                resetVariables(
                    [fits_converted, fits_files, png_files, control])
                #fits_converted = 0
                #fits_files = 0
                #png_files = 0
                #control = 0


def resetVariables(variables):
    for v in variables:
        v = 0

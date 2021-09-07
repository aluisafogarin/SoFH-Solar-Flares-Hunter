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


def ConvertImages(directory):
    print("------- Converting FITS to PNG ------- ")
    path = directory + os.sep + 'continuum' + os.sep + 'x/'
    controlWave = 1  # 1 - 'continuum', 2 - 'aia1600', 3 - 'aia1700'
    controlType = 'x'
    global fitsFiles
    global pngFiles
    global fitsConverted
    control = 0

    while controlWave != 4:
        if controlWave == 1:
            files = listdir(path)
            wave = 'continuum'
            vmin, vmax = float(40000), float(80000)
            controlType == 'x'
            fitsConverted = 0
            fitsFiles = 0
            pngFiles = 0
            print("Converting ", wave, " images.")

        if controlWave == 2:
            wave = 'aia1600'
            files = listdir(path)
            vmin, vmax = float(0), float(1113)
            controlType == 'x'
            fitsConverted = 0
            fitsFiles = 0
            pngFiles = 0
            print("Converting ", wave, " images.")

        if controlWave == 3:
            wave = 'aia1700'
            files = listdir(path)
            vmin, vmax = float(0), float(1113)
            controlType == 'x'
            fitsConverted = 0
            fitsFiles = 0
            pngFiles = 0
            print("Converting ", wave, " images.")

        if controlType == 'x':
            path = directory + os.sep + wave + os.sep + controlType

        if controlType == 'm':
            path = directory + os.sep + wave + os.sep + controlType

        if controlType == 'c':
            path = directory + os.sep + wave + os.sep + controlType

        if controlType == 'b':
            path = directory + os.sep + wave + os.sep + controlType

        newPath = path + os.sep + "*.fits"
        for file in glob.glob(newPath):
            # if "fits" in file:
            fitsFiles += 1

        if fitsFiles != 0:
            print("Fits to convert:", fitsFiles)
            print("Converting images " + wave +
                  " type ", controlType, "to PNG.")
            print("This can take some time. Please, wait.")

            # convertToPNG(path, wave, controlType, vmax, vmin, True)
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
                fitsConverted += 1
                control += 1
                print(fitsConverted, "/", fitsFiles)

            # Move image to png folders
            newPath = path + os.sep + "*.png"
            for file in glob.glob(newPath):
                file = file.replace(path, "")
                file = file.replace(os.sep, "")
                imagePath = directory + os.sep + wave + os.sep + controlType + os.sep + file

                pngFolder = directory + os.sep + wave + os.sep + \
                    'png' + os.sep + controlType + os.sep + file
                shutil.move(imagePath, pngFolder)
                pngFiles += 1
                control += 1

        if fitsConverted + pngFiles == control:

            if controlType == 'x':
                controlType = 'm'
                resetVariables([fitsConverted, fitsFiles, pngFiles, control])
                #fitsConverted = 0
                #fitsFiles = 0
                #pngFiles = 0
                #control = 0

            elif controlType == 'm':
                controlType = 'c'
                resetVariables([fitsConverted, fitsFiles, pngFiles, control])
                #fitsConverted = 0
                #fitsFiles = 0
                #pngFiles = 0
                #control = 0

            elif controlType == 'c':
                controlType = 'b'
                resetVariables([fitsConverted, fitsFiles, pngFiles, control])
                #fitsConverted = 0
                #fitsFiles = 0
                #pngFiles = 0
                #control = 0

            elif controlType == 'b':
                controlType = 'x'
                controlWave += 1
                resetVariables([fitsConverted, fitsFiles, pngFiles, control])
                #fitsConverted = 0
                #fitsFiles = 0
                #pngFiles = 0
                #control = 0

        elif fitsFiles == 0:
            if controlType == 'b':
                controlType = 'x'
                controlWave += 1
                resetVariables([fitsConverted, fitsFiles, pngFiles, control])
                #fitsConverted = 0
                #fitsFiles = 0
                #pngFiles = 0
                #control = 0

            elif controlType == 'x':
                controlType = 'm'
                resetVariables([fitsConverted, fitsFiles, pngFiles, control])
                #fitsConverted = 0
                #fitsFiles = 0
                #pngFiles = 0
                #control = 0

            elif controlType == 'm':
                controlType = 'c'
                resetVariables([fitsConverted, fitsFiles, pngFiles, control])
                #fitsConverted = 0
                #fitsFiles = 0
                #pngFiles = 0
                #control = 0

            elif controlType == 'c':
                controlType = 'b'
                resetVariables([fitsConverted, fitsFiles, pngFiles, control])
                #fitsConverted = 0
                #fitsFiles = 0
                #pngFiles = 0
                #control = 0


def resetVariables(variables):
    for v in variables:
        v = 0

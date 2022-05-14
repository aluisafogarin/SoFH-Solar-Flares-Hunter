import os
import sys
from os import listdir
import glob
import shutil

import logging

from astropy.io import fits
from PIL import Image
import numpy as np

# TODO Add params of wavelength dinamic

from model import enum, configuration
from util import util


class Convert():

    def __init__(self):
        self.fits_files = 0
        self.png_files = 0
        self.fits_converted = 0

    def convert_images(self, config, signal):

        util.create_folders(config.wavelenghts,
                            config.extensions, config.path_save_images)

        # control_wave = 1  # 1 - 'continuum', 2 - 'aia1600', 3 - 'aia1700'
        # control_type = 'x'
        # global self.fits_files
        # global self.png_files
        # global self.fits_converted
        control = 0
        self.fits_files = len(config.images_to_convert)

        for image in config.images_to_convert.keys():
            # Image gets names of the images
            if enum.Wavelenghts.CONTINUUM.value in image:
                path = config.path_save_images + os.sep + \
                    enum.Wavelenghts.CONTINUUM.value + os.sep
                image_path = config.images_to_convert.get(image)
                wave = enum.Wavelenghts.CONTINUUM.value

                vmin, vmax = float(40000), float(80000)

            logging.info("Fits to convert: %d", self.fits_files)
            logging.info("Converting image %s to PNG.", image)
            logging.info("Starting conversion...")
            logging.info("This can tanke some time. Please, wait.")

            #newPath = path + os.sep + "*.fits"

            hdulist = fits.open(image_path, ignore_missing_end=True)
            hdulist.verify('fix')
            im = hdulist[1].data
            np.warnings.filterwarnings('ignore')

            # Clip data to brightness limits
            im[im > vmax] = vmax
            im[im < vmin] = vmin
            # Scale data to range [0, 1]
            im = (im - vmin)/(vmax - vmin)
            # Convert to 8-bit integer
            im = (255*im).astype(np.uint8)
            # Invert y axis
            im = im[::-1, :]

            im = Image.fromarray(im)
            converted = config.images_to_convert.get(image)[:-5] + ".png"
            im.save(converted)
            self.fits_converted += 1
            control += 1

            logging.info("%d/%d", self.fits_converted, self.fits_files)

            logging.info("Moving image to output folder")

            save_path = config.path_save_images + os.sep + converted
            logging.info("%s", save_path)

            shutil.move(config.images_to_convert.get(image)[
                        :-5] + ".png", config.path_save_images + os.sep + wave + os.sep + image[:-5] + ".png")
            self.png_files += 1

            # file = file.replace(path, "")
            # file = file.replace(os.sep, "")

            #image_path = config.path_save_images + os.sep + wave + os.sep + file

        # while control_wave != 4:
        #     if control_wave == 1:
        #         files = listdir(path)
        #         wave = enum.Wavelenghts.CONTINUUM.value
        #         vmin, vmax = float(40000), float(80000)
        #         control_type == 'x'
        #         self.fits_converted = 0
        #         self.fits_files = 0
        #         self.png_files = 0
        #         logging.info("Converting %s images.", wave)

        #     if control_wave == 2:
        #         wave = enum.Wavelenghts.AIA1600.value
        #         files = listdir(path)
        #         vmin, vmax = float(0), float(1113)
        #         control_type == 'x'
        #         self.fits_converted = 0
        #         self.fits_files = 0
        #         self.png_files = 0
        #         logging.info("Converting %s images.", wave)

        #     if control_wave == 3:
        #         wave = enum.Wavelenghts.AIA1700.value
        #         files = listdir(path)
        #         vmin, vmax = float(0), float(1113)
        #         control_type == 'x'
        #         self.fits_converted = 0
        #         self.fits_files = 0
        #         self.png_files = 0
        #         logging.info("Converting %s images.", wave)

        #         path = config.path_save_images + os.sep + wave + os.sep

            # if control_type == 'x':
            #     path = config.path_save_images + os.sep + wave + os.sep + control_type

            # if control_type == 'm':
            #     path = config.path_save_images + os.sep + wave + os.sep + control_type

            # if control_type == 'c':
            #     path = config.path_save_images + os.sep + wave + os.sep + control_type

            # if control_type == 'b':
            #     path = config.path_save_images + os.sep + wave + os.sep + control_type

            # newPath = path + os.sep + "*.fits"
            # for file in glob.glob(newPath):
            #     # if "fits" in file:
            #     self.fits_files += 1

            # if self.fits_files != 0:
            #     logging.info("Fits to convert: %d", self.fits_files)
            #     logging.info("Converting images %s type %s to PNG.",
            #                  wave, control_type)
            #     logging.info("This can take some time. Please, wait.")
            #     print("Converting images " + wave +
            #           " type ", control_type, "to PNG.")
            #     print("This can take some time. Please, wait.")

            #     # convertToPNG(path, wave, control_type, vmax, vmin, True)
            #     newPath = path + os.sep + "*.fits"
            #     for file in glob.glob(newPath):
            #         hdulist = fits.open(file, ignore_missing_end=True)
            #         hdulist.verify('fix')
            #         im = hdulist[1].data
            #         np.warnings.filterwarnings('ignore')

            #         # Clip data to brightness limits
            #         im[im > vmax] = vmax
            #         im[im < vmin] = vmin
            #         # Scale data to range [0, 1]
            #         im = (im - vmin)/(vmax - vmin)
            #         # Convert to 8-bit integer
            #         im = (255*im).astype(np.uint8)
            #         # Invert y axis
            #         im = im[::-1, :]

            #         # Create image from data array and save as png
            #         image = Image.fromarray(im)
            #         converted = file[:-5] + '.png'
            #         image.save(converted)
            #         self.fits_converted += 1
            #         control += 1
            #         print(self.fits_converted, "/", self.fits_files)

            #     # Move image to png folders
            #     newPath = path + os.sep + "*.png"
            #     print(newPath)
            #     for file in glob.glob(newPath):
            #         file = file.replace(path, "")
            #         file = file.replace(os.sep, "")
            #         imagePath = config.path_save_images + os.sep + \
            #             wave + os.sep + control_type + os.sep + file
            #         pngFolder = config.path_save_images + os.sep + wave + os.sep + \
            #             'png' + os.sep + control_type + os.sep + file
            #         shutil.move(imagePath, pngFolder)
            #         self.png_files += 1
            #         control += 1

            # if self.fits_converted + self.png_files == control:

            #     if control_type == 'x':
            #         control_type = 'm'
            #         self.resetVariables(
            #             [self.fits_converted, self.fits_files, self.png_files, control])
            #         print(self.fits_converted, self.fits_files, self.png_files, control)
            #         #self.fits_converted = 0
            #         #self.fits_files = 0
            #         #self.png_files = 0
            #         #control = 0

            #     elif control_type == 'm':
            #         control_type = 'c'
            #         self.resetVariables(
            #             [self.fits_converted, self.fits_files, self.png_files, control])
            #         #self.fits_converted = 0
            #         #self.fits_files = 0
            #         #self.png_files = 0
            #         #control = 0

            #     elif control_type == 'c':
            #         control_type = 'b'
            #         self.resetVariables(
            #             [self.fits_converted, self.fits_files, self.png_files, control])
            #         #self.fits_converted = 0
            #         #self.fits_files = 0
            #         #self.png_files = 0
            #         #control = 0

            #     elif control_type == 'b':
            #         control_type = 'x'
            #         control_wave += 1
            #         self.resetVariables(
            #             [self.fits_converted, self.fits_files, self.png_files, control])
            #         #self.fits_converted = 0
            #         #self.fits_files = 0
            #         #self.png_files = 0
            #         #control = 0

            # elif self.fits_files == 0:
            #     if control_type == 'b':
            #         control_type = 'x'
            #         control_wave += 1
            #         self.resetVariables(
            #             [self.fits_converted, self.fits_files, self.png_files, control])
            #         #self.fits_converted = 0
            #         #self.fits_files = 0
            #         #self.png_files = 0
            #         #control = 0

            #     elif control_type == 'x':
            #         control_type = 'm'
            #         self.resetVariables(
            #             [self.fits_converted, self.fits_files, self.png_files, control])
            #         #self.fits_converted = 0
            #         #self.fits_files = 0
            #         #self.png_files = 0
            #         #control = 0

            #     elif control_type == 'm':
            #         control_type = 'c'
            #         self.resetVariables(
            #             [self.fits_converted, self.fits_files, self.png_files, control])
            #         #self.fits_converted = 0
            #         #self.fits_files = 0
            #         #self.png_files = 0
            #         #control = 0

            #     elif control_type == 'c':
            #         control_type = 'b'
            #         self.resetVariables(
            #             [self.fits_converted, self.fits_files, self.png_files, control])
            #         #self.fits_converted = 0
            #         #self.fits_files = 0
            #         #self.png_files = 0
            #         #control = 0

    def convert_continuum(self, config):
        pass

    def convert_aia1600(self, config):
        pass

    def convert_aia1700(self):
        pass

    def convert_magnetograms(self):
        pass

    def resetVariables(self, variables):
        for v in variables:
            v = 0

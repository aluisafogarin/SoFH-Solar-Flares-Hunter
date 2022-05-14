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

        wavelenghts = []
        self.fits_files = len(config.images_to_convert)
        logging.info("Fits to convert: %d", self.fits_files)
        signal.logging.emit(1)

        for image in config.images_to_convert.keys():
            # Image gets names of the images
            if enum.Wavelenghts.CONTINUUM.value in image:
                wavelenghts.append(enum.Wavelenghts.CONTINUUM.value)
                image_path = config.images_to_convert.get(image)
                wave = enum.Wavelenghts.CONTINUUM.value

                vmin, vmax = float(40000), float(80000)

            elif '1600' in image:
                wavelenghts.append(enum.Wavelenghts.AIA1600.value)
                image_path = config.images_to_convert.get(image)
                wave = enum.Wavelenghts.AIA1600.value

                vmin, vmax = float(0), float(1113)

            elif '1700' in image:
                wavelenghts.append(enum.Wavelenghts.AIA1700.value)
                image_path = config.images_to_convert.get(image)
                wave = enum.Wavelenghts.AIA1700.value

                vmin, vmax = float(0), float(1113)

            util.create_folders(wavelenghts,
                                config.extensions, config.path_save_images, False)

            logging.info("Converting image %s to PNG.", image)
            logging.info(
                "Starting conversion... This can take some time. Please, wait.")
            signal.logging.emit(1)

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
            logging.info("Image converted with success! %d images converted out of %d",
                         self.fits_converted, self.fits_files)
            signal.logging.emit(1)

            self.fits_converted += 1
            save_path = config.path_save_images + os.sep + converted

            shutil.move(config.images_to_convert.get(image)[
                        :-5] + ".png", config.path_save_images + os.sep + wave + os.sep + image[:-5] + ".png")
            self.png_files += 1

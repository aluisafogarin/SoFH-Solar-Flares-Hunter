import os
import shutil
import logging

from astropy.io import fits
from PIL import Image
import numpy as np

from model import enum, configuration
from util import util


class Convert():
    """
    Does all conversion image processment
    """

    def __init__(self):
        """ Class constructor """
        self.fits_files = 0
        self.png_files = 0
        self.fits_converted = 0
        self.logger = logging.getLogger(enum.Files.LOG_CONVERT.value)

    def convert_images(self, config, signal):
        """ Convert images

        Args:
            config (object): Object of configuration class
            signal (object): Signal used to communicate using threads
        """

        wavelenghts = []
        self.fits_files = len(config.images_to_convert)
        self.logger.info("Fits to convert: %d", self.fits_files)
        signal.logging.emit(1)
        
        vmin, vmax = float(0), float(0)
        wave = ''

        for image in config.images_to_convert.keys():
            image_path = config.images_to_convert.get(image)
            print(image_path)
            # Image gets names of the images
            if enum.Wavelenghts.CONTINUUM.value in image:
                wavelenghts.append(enum.Wavelenghts.CONTINUUM.value)
                wave = enum.Wavelenghts.CONTINUUM.value

                vmin, vmax = float(40000), float(80000)
            
            if 'magnetogram' in image:
                wavelenghts.append(enum.Wavelenghts.MAGNETOGRAMS.value)
                wave = enum.Wavelenghts.MAGNETOGRAMS.value
                vmin, vmax = float(-100), float(50)

            elif '1600' in image:
                wavelenghts.append(enum.Wavelenghts.AIA1600.value)
                wave = enum.Wavelenghts.AIA1600.value

                vmin, vmax = float(0), float(1113)

            elif '1700' in image:
                wavelenghts.append(enum.Wavelenghts.AIA1700.value)
                wave = enum.Wavelenghts.AIA1700.value

                vmin, vmax = float(0), float(1113)
                
            util.create_folders(wavelenghts,
                                config.extensions,
                                config.path_save_images,
                                False)

            self.logger.info("Converting image %s to PNG.", image)
            self.logger.info(
                "Starting conversion... This can take some time. Please, wait.")
            signal.logging.emit(1)

            hdulist = fits.open(image_path, ignore_missing_end=True)
            hdulist.verify('fix')
            image_converted = hdulist[1].data
            np.warnings.filterwarnings('ignore')

            # Clip data to brightness limits
            image_converted[image_converted > vmax] = vmax
            image_converted[image_converted < vmin] = vmin
            # Scale data to range [0, 1]
            image_converted = (image_converted - vmin)/(vmax - vmin)
            # Convert to 8-bit integer
            image_converted = (255*image_converted).astype(np.uint8)
            # Invert y axis
            image_converted = image_converted[::-1, :]

            image_converted = Image.fromarray(image_converted)
            converted = config.images_to_convert.get(image)[:-5] + ".png"
            image_converted.save(converted)

            self.fits_converted += 1
            save_path = config.path_save_images + os.sep + converted

            print(wave)

            shutil.move(config.images_to_convert.get(image)[
                        :-5] + ".png", config.path_save_images +
                        os.sep + wave + os.sep + image[:-5] + ".png")
            self.png_files += 1

            self.logger.info("Image converted with success! %d images converted out of %d",
                             self.fits_converted, self.fits_files)
            signal.logging.emit(1)
            
        signal.finished.emit()
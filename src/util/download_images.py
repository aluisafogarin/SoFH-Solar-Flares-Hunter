# TODO Review imports and remove unused ones
import sys
import drms
import os
import csv
import urllib
import time
import logging

from time import sleep

from model import configuration
from model import enum

from util import util


class Download():

    def download_images(self, config, control, signal):
        util.create_folders(config.wavelenghts, config.output_image_types,
                            config.path_output_folder, True)

        if control.new_lines == 0:
            util.verify_output_file(
                config.path_valid_file, config.valid_file, config)

        util.verify_date(config.path_info_file, config.path_valid_file,
                         config.info_file, control, config)

        self.logger = logging.getLogger(enum.Files.LOG_DOWNLOAD.value)

        self.logger.info('Started download')
        signal.logging.emit(1)

        self.date_field = config.date_field
        self.time_field = config.time_field
        self.type_field = config.type_field

        # Creates an instance of drms.Client class
        try:
            self.c = drms.Client(email=config.email, verbose=True)
        except ValueError as exception:
            logging.error(exception)
            signal.error.emit(str(exception))

        self.control = control
        self.control_web_site = 0

        with open(config.valid_file, 'r') as input_file:
            rows = csv.DictReader(input_file)
            for self.row in rows:
                self.date_flare = self.row[self.date_field]
                self.time_flare = self.row[self.time_field]
                self.list_time = self.time_flare[:-3]

                # Relevant informations about current flare, to compare and avoid replication
                self.current_flare = self.date_flare + "_" + self.time_flare
                self.current_flare = self.current_flare.replace(" ", "")

                for wave in config.wavelenghts:
                    if wave == enum.Wavelenghts.CONTINUUM.value:
                        self.download_continuum(
                            config.valid_file, config, signal)
                    elif wave == enum.Wavelenghts.AIA1600.value:
                        self.download_aia1600(
                            config.valid_file, config, signal)
                    elif wave == enum.Wavelenghts.AIA1700.value:
                        self.download_aia1700(
                            config.valid_file, config, signal)

        self.logger.info("Finished download \n")
        total = self.control.aia_seven_images + \
            self.control.aia_six_images + self.control.continuum_images
        self.logger.info("Total of images downloaded: %d", total)
        self.logger.info("HMI Continuum images: %d",
                         self.control.continuum_images)
        self.logger.info("AIA 1600 images: %d", self.control.aia_six_images)
        self.logger.info("AIA 1700 images: %d", self.control.aia_seven_images)
        self.logger.info("%d weren't downloaded to avoid duplication.",
                         self.control.existing_images)

        signal.finished.emit()
        signal.logging.emit(2)

    def download_continuum(self, valid_file, config, signal):
        for output_type in config.output_image_types:

            # Read control file and decode it into "data"
            with open(enum.Files.CONTROL.value, 'rb') as read_control_file:
                data = read_control_file.read()
                data = data.decode('utf-8')
                data = str(data)
                data = data.split('|')

            continuum_flare = self.current_flare + "C" + \
                output_type  # Control flare continuum
            if continuum_flare in data:  # Verify if the image has already been downloaded
                self.control.existing_images += 1
            elif continuum_flare not in data:
                try:
                    # TODO Calcular média do início e fim das explosões
                    self.logger.info("CONTINUUM IMAGE DOWNLOAD")
                    dc = enum.Download.CONTINUUM.value + \
                        '[' + self.date_flare + '_' + self.list_time + '_TAI/' + \
                        enum.Download.TIME_BREAK.value + ']'
                    self.logger.info(dc)
                    signal.logging.emit(1)
                    dc = dc.replace(" ", "")  # Removes blank spaces
                    # Using url/fits
                    r = self.c.export(dc, method='url', protocol=output_type)
                    r.wait()
                    r.status
                    r.request_url
                    # TODO fix output format folder
                    if 'X' in self.row[self.type_field]:
                        r.download(config.path_output_folder + os.sep +
                                   enum.Wavelenghts.CONTINUUM.value + os.sep + output_type + os.sep + 'x')

                    elif 'M' in self.row[self.type_field]:
                        r.download(config.path_output_folder + os.sep +
                                   enum.Wavelenghts.CONTINUUM.value + os.sep + output_type + os.sep + 'm')

                    elif 'C' in self.row[self.type_field]:
                        r.download(config.path_output_folder + os.sep +
                                   enum.Wavelenghts.CONTINUUM.value + os.sep + output_type + os.sep + 'c')

                    elif 'B' in self.row[self.type_field]:
                        r.download(config.path_output_folder + os.sep +
                                   enum.Wavelenghts.CONTINUUM.value + os.sep + output_type + os.sep + 'b')

                    self.control.continuum_images += 1

                # TODO Change notFound file to csv
                except drms.DrmsExportError:
                    self.logger.warning(
                        "Current image doesn't have records online. It can't be downloaded.")
                    signal.logging.emit(1)
                    signal.warning.emit()

                    newRow = self.row[self.type_field] + "," + self.row['Year'] + "," + self.row['Spot'] + \
                        "," + self.row['Start'] + "," + \
                        self.row[self.time_field] + "," + self.row['End']
                    if newRow not in self.not_found_data:
                        with open('notFound.bin', 'ab+') as not_found_file:
                            not_found_file.write(newRow.encode('utf-8'))
                            not_found_file.write('|'.encode('utf-8'))

                except urllib.error.HTTPError:
                    self.logger.warning("The website appers to be offline.")
                    signal.logging.emit(1)
                    if self.control_web_site < 5:
                        self.logger.warning(
                            "Trying to reconnect. Attempt %d of 5", self.control_web_site)
                        signal.logging.emit(1)
                        time.sleep(60)
                        self.download_continuum(valid_file, config, signal)

                    else:
                        self.logger.critical(
                            "The website is offline. Try to run the download again in a few minutes.")
                        signal.logging.emit(1)
                        signal.error.emit(
                            "The website is offline. Try to run the download again in a few minutes.")

                with open(enum.Files.CONTROL.value, 'ab+') as write_control_file:
                    write_control_file.write(
                        continuum_flare.encode('utf-8'))
                    write_control_file.write('|'.encode('utf-8'))

    def download_aia1600(self, valid_file, config, signal):

        for output_type in config.output_image_types:

            # Read control file and decode it into "data"
            with open(enum.Files.CONTROL.value, 'rb') as read_control_file:
                data = read_control_file.read()
                data = data.decode('utf-8')
                data = str(data)
                data = data.split('|')

            aia_1600_flare = self.current_flare + "A16" + output_type
            if aia_1600_flare in data:
                self.control.existing_images += 1

            elif aia_1600_flare not in data:
                try:
                    self.logger.info("AIA1600 IMAGE DOWNLOAD")
                    da = 'aia.lev1_uv_24s[' + self.date_flare + \
                        '_' + self.list_time + '/30m@30m][1600]'
                    da = da.replace(" ", "")  # Removes blank spaces
                    self.logger.info(da)
                    signal.logging.emit(1)
                    r = self.c.export(da, method='url', protocol=output_type)
                    r.wait()
                    r.status
                    r.request_url

                    if 'X' in self.row[self.type_field]:
                        r.download(config.path_output_folder + os.sep +
                                   enum.Wavelenghts.AIA1600.value + os.sep + output_type + os.sep + 'x')

                    elif 'M' in self.row[self.type_field]:
                        r.download(config.path_output_folder + os.sep +
                                   enum.Wavelenghts.AIA1600.value + os.sep + output_type + os.sep + 'm')

                    elif 'C' in self.row[self.type_field]:
                        r.download(config.path_output_folder + os.sep +
                                   enum.Wavelenghts.AIA1600.value + os.sep + output_type + os.sep + 'c')

                    elif 'B' in self.row[self.type_field]:
                        r.download(config.path_output_folder + os.sep +
                                   enum.Wavelenghts.AIA1600.value + os.sep + output_type + os.sep + 'b')

                    self.control.aia_six_images += 1

                    with open(enum.Files.CONTROL.value, 'ab+') as write_control_file:
                        write_control_file.write(
                            aia_1600_flare.encode('utf-8'))
                        write_control_file.write('|'.encode('utf-8'))

                except drms.DrmsExportError:
                    self.logger.warning(
                        "Current image doesn't have records online. It can't be downloaded.")
                    signal.logging.emit(1)
                    signal.warning.emit()

                    with open('notFound.bin', 'rb+') as not_found_file:
                        not_found_data = not_found_file.read()
                        not_found_data = not_found_data.decode('utf-8')
                        not_found_data = str(not_found_data)

                    newRow = self.row[self.type_field] + "," + self.row['Year'] + "," + self.row['Spot'] + \
                        "," + self.row['Start'] + "," + \
                        self.row[self.time_field] + "," + self.row['End']
                    if newRow not in not_found_data:
                        with open('notFound.bin', 'ab+') as not_found_file:
                            not_found_file.write(newRow.encode('utf-8'))
                            not_found_file.write('|'.encode('utf-8'))

                except urllib.error.HTTPError:
                    self.logger.warning("The website appers to be offline.")
                    signal.logging.emit(1)
                    if self.control_web_site < 5:
                        self.logger.warning(
                            "Trying to reconnect. Attempt %d of 5", self.control_web_site)
                        signal.logging.emit(1)
                        time.sleep(60)
                        self.download_aia1600(valid_file, config, signal)

                    else:
                        self.logger.critical(
                            "The website is offline. Try to run the download again in a few minutes.")
                        signal.logging.emit(1)
                        signal.error.emit(
                            "The website is offline. Try to run the download again in a few minutes.")

                with open(enum.Files.CONTROL.value, 'ab+') as write_control_file:
                    write_control_file.write(
                        aia_1600_flare.encode('utf-8'))
                    write_control_file.write('|'.encode('utf-8'))

    def download_aia1700(self, valid_file, config, signal):
        for output_type in config.output_image_types:

            # Read control file and decode it into "data"
            with open(enum.Files.CONTROL.value, 'rb') as read_control_file:
                data = read_control_file.read()
                data = data.decode('utf-8')
                data = str(data)
                data = data.split('|')

            aia_1700_flare = self.current_flare + "A17"
            if aia_1700_flare in data:
                self.control.existing_images += 1

            elif aia_1700_flare not in data:
                try:
                    self.logger.info("AIA1700 IMAGE DOWNLOAD ")
                    daia = 'aia.lev1_uv_24s[' + self.date_flare + \
                        '_' + self.list_time + '/30m@30m][1700]'
                    daia = daia.replace(" ", "")  # Removes blank spaces
                    self.logger.info(daia)
                    signal.logging.emit(1)
                    r = self.c.export(daia, method='url', protocol=output_type)

                    r.wait()
                    r.status
                    r.request_url

                    if 'X' in self.row[self.type_field]:
                        r.download(config.path_output_folder + os.sep +
                                   enum.Wavelenghts.AIA1700.value + os.sep + output_type + os.sep + 'x')

                    elif 'M' in self.row[self.type_field]:
                        r.download(config.path_output_folder + os.sep +
                                   enum.Wavelenghts.AIA1700.value + os.sep + output_type + os.sep + 'm')

                    elif 'C' in self.row[self.type_field]:
                        r.download(config.path_output_folder + os.sep +
                                   enum.Wavelenghts.AIA1700.value + os.sep + output_type + os.sep + 'c')

                    elif 'B' in self.row[self.type_field]:
                        r.download(config.path_output_folder + os.sep +
                                   enum.Wavelenghts.AIA1700.value + os.sep + output_type + os.sep + 'b')

                    self.control.aia_seven_images += 1

                    with open(enum.Files.CONTROL.value, 'ab+') as write_control_file:
                        write_control_file.write(
                            aia_1700_flare.encode('utf-8'))
                        write_control_file.write('|'.encode('utf-8'))

                except drms.DrmsExportError:
                    self.logger.warning(
                        "Current image doesn't have records online. It can't be downloaded.")
                    signal.logging.emit(1)
                    signal.warning.emit()

                    with open('notFound.bin', 'rb+') as self.not_found_file:
                        self.not_found_data = self.not_found_file.read()
                        self.not_found_data = self.not_found_data.decode(
                            'utf-8')
                        self.not_found_data = str(self.not_found_data)

                    newRow = self.row[self.type_field] + "," + self.row['Year'] + "," + self.row['Spot'] + \
                        "," + self.row['Start'] + "," + \
                        self.row[self.time_field] + "," + self.row['End']
                    if newRow not in self.not_found_data:
                        with open('notFound.bin', 'ab+') as not_found_file:
                            not_found_file.write(newRow.encode('utf-8'))
                            not_found_file.write('|'.encode('utf-8'))

                except urllib.error.HTTPError:
                    self.logger.warning("The website appers to be offline.")
                    signal.logging.emit(1)
                    if self.control_web_site < 5:
                        self.logger.warning(
                            "Trying to reconnect. Attempt %d of 5", self.control_web_site)
                        signal.logging.emit(1)
                        time.sleep(60)
                        self.download_aia1700(valid_file, config, signal)

                    else:
                        self.logger.critical(
                            "The website is offline. Try to run the download again in a few minutes.")
                        signal.logging.emit(1)
                        signal.error.emit(
                            "The website is offline. Try to run the download again in a few minutes.")

                with open(enum.Files.CONTROL.value, 'ab+') as write_control_file:
                    write_control_file.write(
                        aia_1700_flare.encode('utf-8'))
                    write_control_file.write('|'.encode('utf-8'))

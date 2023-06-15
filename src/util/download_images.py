import os
import csv
import urllib
import logging
import drms
import time
import pandas as pd


from model import configuration
from model import enum
from util import util


class Download():
    """
    Does all download file processment
    """

    def __init__(self, config, control):
        """ Class constructor

        Args:
            config (object): Object of configuration class
            control (object): Object of control class
        """

        self.logger = logging.getLogger(enum.Files.LOG_DOWNLOAD.value)
        self.date_field = config.date_field
        self.time_field = config.time_field
        self.type_field = config.type_field

        self.control = control

        self.control_web_site = 0

    def download_images(self, config, control, signal):
        """ Download images according to file informed

        Args:
            config (object): Object of configuration class
            control (object): Object of control class
            signal (object): Signal used to communicate using threads
        """

        util.create_folders(config.wavelenghts, config.output_image_types,
                            config.path_output_folder, True)

        if control.new_lines == 0:
            util.verify_output_file(config.path_valid_file, config.valid_file, config)

        util.verify_date(config.path_info_file, config.path_valid_file, control, config)

        self.logger.info('---- DOWNLOAD STARTED')
        signal.logging.emit(1)

        # Creates an instance of drms.Client class
        try:
            self.client = drms.Client(email=config.email, verbose=True)
        except ValueError as exception:
            logging.error(exception)
            signal.error.emit(str(exception))

        with open(config.path_valid_file, 'r') as input_file:
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
                        self.download_continuum(config.valid_file, config, signal)
                    elif wave == enum.Wavelenghts.MAGNETOGRAMS.value:
                        self.download_magnetograms(config.valid_file, config, signal)
                    elif wave == enum.Wavelenghts.AIA1600.value:
                        self.download_aia1600(config.valid_file, config, signal)
                    elif wave == enum.Wavelenghts.AIA1700.value:
                        self.download_aia1700(config.valid_file, config, signal)

        self.logger.info(" ---- END OF DOWNLOAD PROCESS \n")
        total = self.control.aia_seven_images + \
            self.control.aia_six_images + self.control.continuum_images + \
            self.control.magnetogram_images
        self.logger.info("Total of images downloaded: %d", total)
        self.logger.info("HMI Continuum images: %d",self.control.continuum_images)
        self.logger.info("HMI Magnetograms images: %d",self.control.magnetogram_images)
        self.logger.info("AIA 1600 images: %d", self.control.aia_six_images)
        self.logger.info("AIA 1700 images: %d", self.control.aia_seven_images)
        self.logger.info("%d weren't downloaded to avoid duplication. \n", self.control.existing_images)

        not_total = self.control.not_downloaded_continuum + self.control.not_downloaded_magnetogram + \
            self.control.not_downloaded_aia1600 + self.control.not_downloaded_aia1700

        if not_total > 0:
            self.logger.info("Total of files that could not be downloaded: %d", not_total)
            self.logger.info("HMI Continuum images: %d",self.control.not_downloaded_continuum)
            self.logger.info("HMI Magnetograms images: %d",self.control.not_downloaded_magnetogram)
            self.logger.info("AIA 1600 images: %d",self.control.not_downloaded_aia1600)
            self.logger.info("AIA 1700 images: %d",self.control.not_downloaded_aia1700)

            if self.control.not_downloaded_continuum > 0:
                signal.logging.emit(1)
                signal.error.emit("At least one continuum file wasn't download. Check log and 'not_found.csv' file")
            if self.control.not_downloaded_magnetogram > 0:
                signal.logging.emit(1)
                signal.error.emit("At least one magnetogram file wasn't download. Check log and 'not_found.csv' file")
            if self.control.not_downloaded_aia1600 > 0:
                signal.logging.emit(1)
                signal.error.emit("At least one aia1600 file wasn't download. Check log and 'not_found.csv' file")
            if self.control.not_downloaded_aia1700 > 0:
                signal.logging.emit(1)
                signal.error.emit("At least one aia1700 file wasn't download. Check log and 'not_found.csv' file")

        signal.finished.emit()
        signal.logging.emit(2)

    def download_continuum(self, valid_file, config, signal):
        """ Download images in continuum wavelenght

        Args:
            valid_file (string): Name of file with flare information
            config (object): Object of configuration class
            signal (object): Signal used to communicate using threads
        """
        for output_type in config.output_image_types:

            # Read control file and decode it into "data"
            with open(enum.Files.CONTROL.value, 'rb') as read_control_file:
                data = read_control_file.read()
                data = data.decode('utf-8')
                data = str(data)
                data = data.split('|')

            continuum_flare = self.current_flare + "C" + \
                output_type  # Control flare continuum
            if continuum_flare in data:  # Verify if the file has already been downloaded
                self.control.existing_images += 1
            elif continuum_flare not in data:
                try:
                    self.logger.info("CONTINUUM IMAGE DOWNLOAD")
                    continuum_download_control = enum.Download.CONTINUUM.value + \
                        '[' + self.date_flare + '_' + self.list_time + '_TAI/' + \
                        enum.Download.TIME_BREAK.value + ']'
                    self.logger.info(continuum_download_control)
                    signal.logging.emit(1)
                    continuum_download_control = continuum_download_control.replace(
                        " ", "")  # Removes blank spaces
                    # Using url/fits
                    request = self.client.export(
                        continuum_download_control, method='url', protocol=output_type)
                    request.wait()
                    request.status
                    request.request_url
                    if 'X' in self.row[self.type_field]:
                        df = pd.DataFrame(request.download(config.path_output_folder + os.sep +
                                                           enum.Wavelenghts.CONTINUUM.value +
                                                           os.sep + output_type + os.sep + 'x'))

                    elif 'M' in self.row[self.type_field]:
                        df = pd.DataFrame(request.download(config.path_output_folder + os.sep +
                                                           enum.Wavelenghts.CONTINUUM.value +
                                                           os.sep + output_type + os.sep + 'm'))

                    elif 'C' in self.row[self.type_field]:
                        df = pd.DataFrame(request.download(config.path_output_folder + os.sep +
                                                           enum.Wavelenghts.CONTINUUM.value +
                                                           os.sep + output_type + os.sep + 'c'))

                    elif 'B' in self.row[self.type_field]:
                        df = pd.DataFrame(request.download(config.path_output_folder + os.sep +
                                                           enum.Wavelenghts.CONTINUUM.value +
                                                           os.sep + output_type + os.sep + 'b'))

                    if df.loc[0].at["download"] != None:
                        self.control.continuum_images += 1

                        with open(enum.Files.CONTROL.value, 'ab+') as write_control_file:
                            write_control_file.write(
                                continuum_flare.encode('utf-8'))
                            write_control_file.write('|'.encode('utf-8'))

                    else:
                        self.record_flare_on_not_found(
                            self.row, continuum_download_control, signal)
                        self.control.not_downloaded_continuum += 1

                except drms.DrmsExportError:
                    self.record_flare_on_not_found(
                        self.row, continuum_download_control, signal)
                    self.control.not_downloaded_continuum += 1

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

                except:
                    self.record_flare_on_not_found(
                        self.row, continuum_download_control, signal)
                    self.control.not_downloaded_continuum += 1

    def download_magnetograms(self, valid_file, config, signal):
        """ Download images in magnetograms wavelenght

        Args:
            valid_file (string): Name of file with flare information
            config (object): Object of configuration class
            signal (object): Signal used to communicate using threads
        """
        for output_type in config.output_image_types:

            # Read control file and decode it into "data"
            with open(enum.Files.CONTROL.value, 'rb') as read_control_file:
                data = read_control_file.read()
                data = data.decode('utf-8')
                data = str(data)
                data = data.split('|')

            magnetogram_flare = self.current_flare + "M" + \
                output_type  # Control flare continuum
            if magnetogram_flare in data:  # Verify if the file has already been downloaded
                self.control.existing_images += 1
            elif magnetogram_flare not in data:
                try:
                    self.logger.info("MAGNETOGRAM IMAGE DOWNLOAD")
                    magnetogram_download_control = enum.Download.MAGNETOGRAMS.value + \
                        '[' + self.date_flare + '_' + self.list_time + '_TAI/' + \
                        enum.Download.TIME_BREAK.value + ']'
                    self.logger.info(magnetogram_download_control)
                    signal.logging.emit(1)
                    magnetogram_download_control = magnetogram_download_control.replace(
                        " ", "")  # Removes blank spaces
                    # Using url/fits
                    request = self.client.export(
                        magnetogram_download_control, method='url', protocol=output_type)
                    request.wait()
                    request.status
                    request.request_url
                    if 'X' in self.row[self.type_field]:
                        df = pd.DataFrame(request.download(config.path_output_folder + os.sep +
                                                           enum.Wavelenghts.MAGNETOGRAMS.value +
                                                           os.sep + output_type + os.sep + 'x'))

                    elif 'M' in self.row[self.type_field]:
                        df = pd.DataFrame(request.download(config.path_output_folder + os.sep +
                                                           enum.Wavelenghts.MAGNETOGRAMS.value +
                                                           os.sep + output_type + os.sep + 'm'))

                    elif 'C' in self.row[self.type_field]:
                        df = pd.DataFrame(request.download(config.path_output_folder + os.sep +
                                                           enum.Wavelenghts.MAGNETOGRAMS.value +
                                                           os.sep + output_type + os.sep + 'c'))

                    elif 'B' in self.row[self.type_field]:
                        df = pd.DataFrame(request.download(config.path_output_folder + os.sep +
                                                           enum.Wavelenghts.MAGNETOGRAMS.value +
                                                           os.sep + output_type + os.sep + 'b'))

                    if df.loc[0].at["download"] != None:
                        self.control.magnetogram_images += 1

                        with open(enum.Files.CONTROL.value, 'ab+') as write_control_file:
                            write_control_file.write(
                                magnetogram_flare.encode('utf-8'))
                            write_control_file.write('|'.encode('utf-8'))

                    else:
                        self.record_flare_on_not_found(
                            self.row, magnetogram_download_control, signal)
                        self.control.not_downloaded_magnetogram += 1

                except drms.DrmsExportError:
                    self.record_flare_on_not_found(
                        self.row, magnetogram_download_control, signal)
                    self.control.not_downloaded_magnetogram += 1

                except urllib.error.HTTPError:
                    self.logger.warning("The website appers to be offline.")
                    signal.logging.emit(1)
                    if self.control_web_site < 5:
                        self.logger.warning(
                            "Trying to reconnect. Attempt %d of 5", self.control_web_site)
                        signal.logging.emit(1)
                        time.sleep(60)
                        self.download_magnetograms(valid_file, config, signal)

                    else:
                        self.logger.critical(
                            "The website is offline. Try to run the download again in a few minutes.")
                        signal.logging.emit(1)
                        signal.error.emit(
                            "The website is offline. Try to run the download again in a few minutes.")

                except:
                    self.record_flare_on_not_found(
                        self.row, magnetogram_download_control, signal)
                    self.control.not_downloaded_magnetogram += 1

    def download_aia1600(self, valid_file, config, signal):
        """ Download images in aia1600 wavelenght

        Args:
            valid_file (string): Name of file with flare information
            config (object): Object of configuration class
            signal (object): Signal used to communicate using threads
        """

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
                    download_1600_control = 'aia.lev1_uv_24s[' + self.date_flare + \
                        '_' + self.list_time + '/30m@30m][1600]'
                    download_1600_control = download_1600_control.replace(
                        " ", "")  # Removes blank spaces
                    self.logger.info(download_1600_control)
                    signal.logging.emit(1)
                    request = self.client.export(
                        download_1600_control, method='url', protocol=output_type)
                    request.wait()
                    request.status
                    request.request_url

                    if 'X' in self.row[self.type_field]:
                        df = pd.DataFrame(request.download(config.path_output_folder + os.sep +
                                                           enum.Wavelenghts.AIA1600.value +
                                                           os.sep + output_type + os.sep + 'x'))

                    elif 'M' in self.row[self.type_field]:
                        df = pd.DataFrame(request.download(config.path_output_folder + os.sep +
                                                           enum.Wavelenghts.AIA1600.value +
                                                           os.sep + output_type + os.sep + 'm'))

                    elif 'C' in self.row[self.type_field]:
                        df = pd.DataFrame(request.download(config.path_output_folder + os.sep +
                                                           enum.Wavelenghts.AIA1600.value +
                                                           os.sep + output_type + os.sep + 'c'))

                    elif 'B' in self.row[self.type_field]:
                        df = pd.DataFrame(request.download(config.path_output_folder + os.sep +
                                                           enum.Wavelenghts.AIA1600.value +
                                                           os.sep + output_type + os.sep + 'b'))

                    if df.loc[0].at["download"] != None:
                        self.control.aia_six_images += 1

                        with open(enum.Files.CONTROL.value, 'ab+') as write_control_file:
                            write_control_file.write(
                                aia_1600_flare.encode('utf-8'))
                            write_control_file.write('|'.encode('utf-8'))
                    else:
                        self.record_flare_on_not_found(
                            self.row, download_1600_control, signal)
                        self.control.not_downloaded_aia1600 += 1

                except drms.DrmsExportError:
                    self.record_flare_on_not_found(
                        self.row, download_1600_control, signal)
                    self.control.not_downloaded_aia1600 += 1

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

                except:
                    self.record_flare_on_not_found(
                        self.row, download_1600_control, signal)
                    self.control.not_downloaded_aia1600 += 1

    def download_aia1700(self, valid_file, config, signal):
        """ Download images in aia1700 wavelenght

        Args:
            valid_file (string): Name of file with flare information
            config (object): Object of configuration class
            signal (object): Signal used to communicate using threads
        """

        for output_type in config.output_image_types:
            # Read control file and decode it into "data"
            with open(enum.Files.CONTROL.value, 'rb') as read_control_file:
                data = read_control_file.read()
                data = data.decode('utf-8')
                data = str(data)
                data = data.split('|')

            aia_1700_flare = self.current_flare + "A17" + output_type
            if aia_1700_flare in data:
                self.control.existing_images += 1

            elif aia_1700_flare not in data:
                try:
                    self.logger.info("AIA1700 IMAGE DOWNLOAD ")
                    download_1700_control = 'aia.lev1_uv_24s[' + self.date_flare + \
                        '_' + self.list_time + '/30m@30m][1700]'
                    download_1700_control = download_1700_control.replace(
                        " ", "")  # Removes blank spaces
                    self.logger.info(download_1700_control)
                    signal.logging.emit(1)
                    request = self.client.export(
                        download_1700_control, method='url', protocol=output_type)

                    request.wait()
                    request.status
                    request.request_url

                    if 'X' in self.row[self.type_field]:
                        df = pd.DataFrame(request.download(config.path_output_folder + os.sep +
                                                           enum.Wavelenghts.AIA1700.value +
                                                           os.sep + output_type + os.sep + 'x'))

                    elif 'M' in self.row[self.type_field]:
                        df = pd.DataFrame(request.download(config.path_output_folder + os.sep +
                                                           enum.Wavelenghts.AIA1700.value +
                                                           os.sep + output_type + os.sep + 'm'))

                    elif 'C' in self.row[self.type_field]:
                        df = pd.DataFrame(request.download(config.path_output_folder + os.sep +
                                                           enum.Wavelenghts.AIA1700.value +
                                                           os.sep + output_type + os.sep + 'c'))

                    elif 'B' in self.row[self.type_field]:
                        df = pd.DataFrame(request.download(config.path_output_folder + os.sep +
                                                           enum.Wavelenghts.AIA1700.value +
                                                           os.sep + output_type + os.sep + 'b'))

                    if df.loc[0].at["download"] != None:
                        self.control.aia_seven_images += 1

                        with open(enum.Files.CONTROL.value, 'ab+') as write_control_file:
                            write_control_file.write(
                                aia_1700_flare.encode('utf-8'))
                            write_control_file.write('|'.encode('utf-8'))
                    else:
                        self.record_flare_on_not_found(
                            self.row, download_1700_control, signal)
                        self.control.not_downloaded_aia1700 += 1
                except drms.DrmsExportError:
                    self.record_flare_on_not_found(
                        self.row, download_1700_control, signal)
                    self.control.not_downloaded_aia1700 += 1

                    self.logger.critical(
                        "Error during exporting file - %s", download_1700_control)

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

                except:
                    self.record_flare_on_not_found(
                        self.row, download_1700_control, signal)
                    self.control.not_downloaded_aia1700 += 1

    def record_flare_on_not_found(self, row, file, signal):
        """
        Record flare information on csv file when download isn't successful

        Args:
            row (string): Flare information as it is from input csv
            file (string): Request format to drms
            signal (object): Signal used to comunicate using threads
        """
        new_row = self.row[self.type_field] + "," + self.row['Year'] + "," + self.row['Spot'] + \
            "," + self.row['Start'] + "," + \
            self.row[self.time_field] + "," + self.row['End']

        directory = (os.path.dirname(os.path.realpath(__file__)))

        if not os.path.exists(directory + os.sep + enum.Files.NOT_FOUND_CSV.value):
            util.create_files(directory + os.sep +
                              enum.Files.NOT_FOUND_CSV.value, 'w',
                              configuration.ConfigurationDownload())
            self.logger.info("Creating %s file",
                             enum.Files.NOT_FOUND_CSV.value)

        with open(enum.Files.NOT_FOUND_CSV.value, 'ab+') as not_found_file:
            not_found_file.write(new_row.encode('utf-8'))
            not_found_file.write('|'.encode('utf-8'))
            self.logger.critical("Could not download file - %s", file)
            self.logger.critical(
                "Recording corresponding flare informations on 'not_found.csv'")

# TODO Review imports and remove unused ones
import sys
import drms
import os
import csv
import urllib
import time

from time import sleep

from model import configuration
from model import enum

from util import util


class Download():

    def download_images(self, valid_file, config):
        util.create_folders(config.wavelenghts, config.output_image_types,
                            config.path_output_folder)

        self.date_field = config.date_field
        self.time_field = config.time_field
        self.type_field = config.type_field

        # Creates an instance of drms.Client class
        self.c = drms.Client(email=config.email, verbose=True)
        self.control = configuration.ControlVariables()

        # TODO Refactor download images
        # TODO controlFile has the same name on different files, padronize this somewhere
        self.control_web_site = 0

        print("Starting downloading process")
        with open(valid_file, 'r') as input_file:
            rows = csv.DictReader(input_file)
            for self.row in rows:
                self.date_flare = self.row[self.date_field]
                self.time_flare = self.row[self.time_field]
                self.list_time = self.time_flare[:-3]

                # Relevant informations about current flare, to compare and avoid replication
                self.current_flare = self.date_flare + "_" + self.time_flare
                self.current_flare = self.current_flare.replace(" ", "")

                # Read control file and decode it into "data"
                with open(enum.Files.CONTROL.value, 'rb') as read_control_file:
                    self.data = read_control_file.read()
                    self.data = self.data.decode('utf-8')
                    self.data = str(self.data)
                    self.data = self.data.split('|')

                    for wave in config.wavelenghts:
                        if wave == enum.Wavelenghts.CONTINUUM.value:
                            self.download_continuum(
                                valid_file, config)
                        elif wave == enum.Wavelenghts.AIA1600.value:
                            self.download_aia1600(
                                valid_file, config)
                        elif wave == enum.Wavelenghts.AIA1700.value:
                            self.download_aia1700(
                                valid_file, config)

        print("Download complete!")
        print("\n\n ----------------------------------------------------- ")
        print("Total of images downloaded: ", self.control.aia_seven_images +
              self.control.aia_six_images + self.control.continuum_images)
        print("HMI Continuum images: ", self.control.continuum_images)
        print("AIA 1600 images: ", self.control.aia_six_images)
        print("AIA 1700 images: ", self.control.aia_seven_images)
        print(self.control.existing_images,
              "weren't downloaded to avoid duplication.")

    def download_continuum(self, valid_file, config):
        # Downloading images on HMI Continuum --------------------------------------------
        continuum_flare = self.current_flare + "C"  # Control flare continuum
        if continuum_flare in self.data:  # Verify if the image has already been downloaded
            self.control.existing_images += 1
        elif continuum_flare not in self.data:
            try:
                # TODO Calcular média do início e fim das explosões
                print("------ CONTINUUM IMAGE DOWNLOAD --------")
                dc = enum.Download.CONTINUUM.value + \
                    '[' + self.date_flare + '_' + self.list_time + '_TAI/' + \
                    enum.Download.TIME_BREAK.value + ']'
                # dc = 'hmi.Ic_45s['+date_flare + \
                #     '_'+list_time+'_TAI/30m@30m]'
                print(dc)
                dc = dc.replace(" ", "")  # Removes blank spaces
                # Using url/fits
                r = self.c.export(dc, method='url', protocol='fits')
                r.wait()
                r.status
                r.request_url
                if 'X' in self.row[self.type_field]:
                    r.download(config.path_output_folder + os.sep +
                               enum.Wavelenghts.CONTINUUM.value + os.sep + 'x')

                elif 'M' in self.row[self.type_field]:
                    r.download(config.path_output_folder + os.sep +
                               enum.Wavelenghts.CONTINUUM.value + os.sep + 'm')

                elif 'C' in self.row[self.type_field]:
                    r.download(config.path_output_folder + os.sep +
                               enum.Wavelenghts.CONTINUUM.value + os.sep + 'c')

                elif 'B' in self.row[self.type_field]:
                    r.download(config.path_output_folder + os.sep +
                               enum.Wavelenghts.CONTINUUM.value + os.sep + 'b')

                self.control.continuum_images += 1

            # TODO Change notFound file to csv
            except drms.DrmsExportError:
                print(
                    "Current image doesn't have records online. It can't be downloaded.")
                with open(enum.Files.CONTROL.value, 'ab+') as write_control_file:
                    write_control_file.write(
                        continuum_flare.encode('utf-8'))
                    write_control_file.write('|'.encode('utf-8'))

                newRow = self.row[self.type_field] + "," + self.row['Year'] + "," + self.row['Spot'] + \
                    "," + self.row['Start'] + "," + \
                    self.row[self.time_field] + "," + self.row['End']
                if newRow not in self.not_found_data:
                    with open('notFound.bin', 'ab+') as not_found_file:
                        not_found_file.write(newRow.encode('utf-8'))
                        not_found_file.write('|'.encode('utf-8'))

            except urllib.error.HTTPError:
                print("The website appers to be offline.")
                if self.control_web_site < 5:
                    print("Trying to reconnet. Attempt ",
                          self.control_web_site, " of 5.")
                    time.sleep(60)
                    self.download_continuum(valid_file, config)

                else:
                    print(
                        "The website is offline. Try to run the script again in a few minutes.")

    def download_aia1600(self, valid_file, config):
        aia_1600_flare = self.current_flare + "A16"
        if aia_1600_flare in self.data:
            self.control.existing_images += 1

        elif aia_1600_flare not in self.data:
            try:
                print("------ AIA1600 IMAGE DOWNLOAD --------")
                da = 'aia.lev1_uv_24s[' + self.date_flare + \
                    '_' + self.list_time + '/30m@30m][1600]'
                da = da.replace(" ", "")  # Removes blank spaces
                r = self.c.export(da, method='url', protocol='fits')
                r.wait()
                r.status
                r.request_url

                if 'X' in self.row[self.type_field]:
                    r.download(config.path_output_folder +
                               enum.Wavelenghts.AIA1600.value + '/x')

                elif 'M' in self.row[self.type_field]:
                    r.download(config.path_output_folder +
                               enum.Wavelenghts.AIA1600.value + '/m')

                elif 'C' in self.row[self.type_field]:
                    r.download(config.path_output_folder +
                               enum.Wavelenghts.AIA1600.value + '/c')

                elif 'B' in self.row[self.type_field]:
                    r.download(config.path_output_folder +
                               enum.Wavelenghts.AIA1600.value + '/b')

                self.control.aia_six_images += 1

                with open(enum.Files.CONTROL.value, 'ab+') as write_control_file:
                    write_control_file.write(
                        aia_1600_flare.encode('utf-8'))
                    write_control_file.write('|'.encode('utf-8'))

            except drms.DrmsExportError:
                print(
                    "Current image doesn't have records online. It can't be downloaded.")
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
                print("The website appers to be offline.")
                if self.control_web_site < 5:
                    print("Trying to reconnet. Attempt ",
                          self.control_web_site, " of 5.")
                    time.sleep(60)
                    self.download_aia1600(valid_file, config)

                else:
                    print(
                        "The website is offline. Try to run the script again in a few minutes.")

    def download_aia1700(self, valid_file, config):
        # Downloading images on AIA 1700 --------------------------------------------
        aia_1700_flare = self.current_flare + "A17"
        if aia_1700_flare in self.data:
            self.control.existing_images += 1

        elif aia_1700_flare not in self.data:
            try:
                print("------ AIA1700 IMAGE DOWNLOAD --------")
                daia = 'aia.lev1_uv_24s[' + self.date_flare + \
                    '_' + self.list_time + '/30m@30m][1700]'
                daia = daia.replace(" ", "")  # Removes blank spaces
                r = self.c.export(daia, method='url', protocol='fits')

                r.wait()
                r.status
                r.request_url

                if 'X' in self.row[self.type_field]:
                    r.download(config.path_output_folder +
                               enum.Wavelenghts.AIA1700.value + '/x')

                elif 'M' in self.row[self.type_field]:
                    r.download(config.path_output_folder +
                               enum.Wavelenghts.AIA1700.value + '/m')

                elif 'C' in self.row[self.type_field]:
                    r.download(config.path_output_folder +
                               enum.Wavelenghts.AIA1700.value + '/c')

                elif 'B' in self.row[self.type_field]:
                    r.download(config.path_output_folder +
                               enum.Wavelenghts.AIA1700.value + '/b')

                self.control.aia_seven_images += 1

                with open(enum.Files.CONTROL.value, 'ab+') as write_control_file:
                    write_control_file.write(
                        aia_1700_flare.encode('utf-8'))
                    write_control_file.write('|'.encode('utf-8'))

            except drms.DrmsExportError:
                print(
                    "Current image doesn't have records online. It can't be downloaded.")
                with open('notFound.bin', 'rb+') as self.not_found_file:
                    self.not_found_data = self.not_found_file.read()
                    self.not_found_data = self.not_found_data.decode('utf-8')
                    self.not_found_data = str(self.not_found_data)

                newRow = self.row[self.type_field] + "," + self.row['Year'] + "," + self.row['Spot'] + \
                    "," + self.row['Start'] + "," + \
                    self.row[self.time_field] + "," + self.row['End']
                if newRow not in self.not_found_data:
                    with open('notFound.bin', 'ab+') as not_found_file:
                        not_found_file.write(newRow.encode('utf-8'))
                        not_found_file.write('|'.encode('utf-8'))

            except urllib.error.HTTPError:
                print("The website appers to be offline.")
                if self.control_web_site < 5:
                    print("Trying to reconnet. Attempt ",
                          self.control_web_site, " of 5.")
                    time.sleep(60)
                    self.download_aia1700(valid_file, config)

                else:
                    print(
                        "The website is offline. Try to run the script again in a few minutes.")

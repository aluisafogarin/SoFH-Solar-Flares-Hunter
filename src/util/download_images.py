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
# Rename method


def downloadImages(valid_file, config):

    print("DOWNLAOD IMAG OUTPUT FOLDER " + config.path_output_folder)
    print(config.email)
    print("-------------")

    util.create_folders(config.wavelenghts, config.output_image_types,
                        config.path_output_folder)

    date_field = config.date_field
    time_field = config.time_field
    type_field = config.type_field

    # Creates an instance of drms.Client class
    c = drms.Client(email=config.email, verbose=True)
    control = configuration.ControlVariables()

    # TODO Refactor download images
    # TODO controlFile has the same name on different files, padronize this somewhere
    control_web_site = 0

    print("Starting downloading process")
    with open(valid_file, 'r') as input_file:
        rows = csv.DictReader(input_file)
        for row in rows:
            date_flare = row[date_field]
            time_flare = row[time_field]
            list_time = time_flare[:-3]

            # Relevant informations about current flare, to compare and avoid replication
            current_flare = date_flare + "_" + time_flare
            current_flare = current_flare.replace(" ", "")

            # Read control file and decode it into "data"
            with open(enum.Files.CONTROL.value, 'rb') as read_control_file:
                data = read_control_file.read()
                data = data.decode('utf-8')
                data = str(data)
                data = data.split('|')

                # Downloading images on HMI Continuum --------------------------------------------
                continuum_flare = current_flare + "C"  # Control flare continuum
                if continuum_flare in data:  # Verify if the image has already been downloaded
                    control.existing_images += 1

                elif continuum_flare not in data:
                    try:
                        # TODO Calcular média do início e fim das explosões
                        print("------ CONTINUUM IMAGE DOWNLOAD --------")
                        dc = enum.Download.CONTINUUM.value + \
                            '[' + date_flare + '_' + list_time + '_TAI/' + \
                            enum.Download.TIME_BREAK.value + ']'
                        # dc = 'hmi.Ic_45s['+date_flare + \
                        #     '_'+list_time+'_TAI/30m@30m]'
                        print(dc)
                        dc = dc.replace(" ", "")  # Removes blank spaces
                        # Using url/fits
                        r = c.export(dc, method='url', protocol='fits')
                        r.wait()
                        r.status
                        r.request_url
                        if 'X' in row[type_field]:
                            r.download(config.path_output_folder + os.sep +
                                       enum.Wavelenghts.CONTINUUM.value + os.sep + 'x')

                        elif 'M' in row[type_field]:
                            r.download(config.path_output_folder + os.sep +
                                       enum.Wavelenghts.CONTINUUM.value + os.sep + 'm')

                        elif 'C' in row[type_field]:
                            r.download(config.path_output_folder + os.sep +
                                       enum.Wavelenghts.CONTINUUM.value + os.sep + 'c')

                        elif 'B' in row[type_field]:
                            r.download(config.path_output_folder + os.sep + 
                                       enum.Wavelenghts.CONTINUUM.value + os.sep + 'b')

                        control.continuum_images += 1

                    # TODO Change notFound file to csv
                    except drms.DrmsExportError:
                        print(
                            "Current image doesn't have records online. It can't be downloaded.")
                        with open('notFound.bin', 'rb+') as not_found_file:
                            not_found_data = not_found_file.read()
                            not_found_data = not_found_data.decode('utf-8')
                            not_found_data = str(not_found_data)

                        newRow = row[type_field] + "," + row['Year'] + "," + row['Spot'] + \
                            "," + row['Start'] + "," + \
                            row[time_field] + "," + row['End']
                        if newRow not in not_found_data:
                            with open('notFound.bin', 'ab+') as not_found_file:
                                not_found_file.write(newRow.encode('utf-8'))
                                not_found_file.write('|'.encode('utf-8'))

                    except urllib.error.HTTPError:
                        print("The website appers to be offline.")
                        if control_web_site < 5:
                            print("Trying to reconnet. Attempt ",
                                  control_web_site, " of 5.")
                            time.sleep(60)
                            downloadImages(valid_file, config)

                        else:
                            print(
                                "The website is offline. Try to run the script again in a few minutes.")

                    with open(enum.Files.CONTROL.value, 'ab+') as write_control_file:
                        write_control_file.write(
                            continuum_flare.encode('utf-8'))
                        write_control_file.write('|'.encode('utf-8'))

    print("Download complete!")
    print("\n\n ----------------------------------------------------- ")
    print("Total of images downloaded: ", control.aia_seven_images +
          control.aia_six_images + control.continuum_images)
    print("HMI Continuum images: ", control.continuum_images)
    print("AIA 1600 images: ", control.aia_six_images)
    print("AIA 1700 images: ", control.aia_seven_images)
    print(control.existing_images, "weren't downloaded to avoid duplication.")


def download_aia1600():
    # Downloading images on AIA 1600 --------------------------------------------
    # aia_1600_flare = current_flare + "A16"
    # if aia_1600_flare in data:
    #     control.existing_images += 1

    # elif aia_1600_flare not in data:
    #     try:
    #         print("------ AIA1600 IMAGE DOWNLOAD --------")
    #         da = 'aia.lev1_uv_24s['+date_flare + \
    #             '_' + list_time + '/30m@30m][1600]'
    #         da = da.replace(" ", "")  # Removes blank spaces
    #         r = c.export(da, method='url', protocol='fits')
    #         r.wait()
    #         r.status
    #         r.request_url

    #         if 'X' in row[type_field]:
    #             r.download(config.path_output_folder +
    #                        enum.Wavelenghts.AIA1600.value + '/x')

    #         elif 'M' in row[type_field]:
    #             r.download(config.path_output_folder +
    #                        enum.Wavelenghts.AIA1600.value + '/m')

    #         elif 'C' in row[type_field]:
    #             r.download(config.path_output_folder +
    #                        enum.Wavelenghts.AIA1600.value + '/c')

    #         elif 'B' in row[type_field]:
    #             r.download(config.path_output_folder +
    #                        enum.Wavelenghts.AIA1600.value + '/b')

    #         control.aia_six_images += 1

    #         with open(enum.Files.CONTROL.value, 'ab+') as write_control_file:
    #             write_control_file.write(
    #                 aia_1600_flare.encode('utf-8'))
    #             write_control_file.write('|'.encode('utf-8'))

    #     except drms.DrmsExportError:
    #         print(
    #             "Current image doesn't have records online. It can't be downloaded.")
    #         with open('notFound.bin', 'rb+') as not_found_file:
    #             not_found_data = not_found_file.read()
    #             not_found_data = not_found_data.decode('utf-8')
    #             not_found_data = str(not_found_data)

    #         newRow = row[type_field] + "," + row['Year'] + "," + row['Spot'] + \
    #             "," + row['Start'] + "," + \
    #             row[time_field] + "," + row['End']
    #         if newRow not in not_found_data:
    #             with open('notFound.bin', 'ab+') as not_found_file:
    #                 not_found_file.write(newRow.encode('utf-8'))
    #                 not_found_file.write('|'.encode('utf-8'))

    #     except urllib.error.HTTPError:
    #         print("The website appers to be offline.")
    #         if control_web_site < 5:
    #             print("Trying to reconnet. Attempt ",
    #                   control_web_site, " of 5.")
    #             time.sleep(60)
    #             downloadImages(valid_file, config)

    #         else:
    #             print(
    #                 "The website is offline. Try to run the script again in a few minutes.")
    pass


def download_aia1700():
    # # Downloading images on AIA 1700 --------------------------------------------
    # aia_1700_flare = current_flare + "A17"
    # if aia_1700_flare in data:
    #     control.existing_images += 1

    # elif aia_1700_flare not in data:
    #     try:
    #         print("------ AIA1700 IMAGE DOWNLOAD --------")
    #         daia = 'aia.lev1_uv_24s[' + date_flare + \
    #             '_' + list_time + '/30m@30m][1700]'
    #         daia = daia.replace(" ", "")  # Removes blank spaces
    #         r = c.export(daia, method='url', protocol='fits')

    #         r.wait()
    #         r.status
    #         r.request_url

    #         if 'X' in row[type_field]:
    #             r.download(config.path_output_folder +
    #                        enum.Wavelenghts.AIA1700.value + '/x')

    #         elif 'M' in row[type_field]:
    #             r.download(config.path_output_folder +
    #                        enum.Wavelenghts.AIA1700.value + '/m')

    #         elif 'C' in row[type_field]:
    #             r.download(config.path_output_folder +
    #                        enum.Wavelenghts.AIA1700.value + '/c')

    #         elif 'B' in row[type_field]:
    #             r.download(config.path_output_folder +
    #                        enum.Wavelenghts.AIA1700.value + '/b')

    #         control.aia_seven_images += 1

    #         with open(enum.Files.CONTROL.value, 'ab+') as write_control_file:
    #             write_control_file.write(
    #                 aia_1700_flare.encode('utf-8'))
    #             write_control_file.write('|'.encode('utf-8'))

    #     except drms.DrmsExportError:
    #         print(
    #             "Current image doesn't have records online. It can't be downloaded.")
    #         with open('notFound.bin', 'rb+') as not_found_file:
    #             not_found_data = not_found_file.read()
    #             not_found_data = not_found_data.decode('utf-8')
    #             not_found_data = str(not_found_data)

    #         newRow = row[type_field] + "," + row['Year'] + "," + row['Spot'] + \
    #             "," + row['Start'] + "," + \
    #             row[time_field] + "," + row['End']
    #         if newRow not in not_found_data:
    #             with open('notFound.bin', 'ab+') as not_found_file:
    #                 not_found_file.write(newRow.encode('utf-8'))
    #                 not_found_file.write('|'.encode('utf-8'))

    # except urllib.error.HTTPError:
    #     print("The website appers to be offline.")
    #     if control_web_site < 5:
    #         print("Trying to reconnet. Attempt ",
    #               control_web_site, " of 5.")
    #         time.sleep(60)
    #         downloadImages(valid_file, config)

    #     else:
    #         print(
    #             "The website is offline. Try to run the script again in a few minutes.")
    pass

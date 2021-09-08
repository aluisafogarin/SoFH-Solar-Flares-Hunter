# TODO Review imports and remove unused ones
import sys
import drms
import os
import csv
import urllib
import time

from time import sleep

from model import wavelenghts as enum


def downloadImages(valid_file, config):

    date_field = config.date_field
    time_field = config.time_field
    type_field = config.type_field

    # Creates an instance of drms.Client class
    c = drms.Client(email=config.email, verbose=True)

    # TODO Refactor download images
    # TODO controlFile has the same name on different files, padronize this somewhere
    control_web_site = 0

    global continuum_images
    global aia_six_images
    global aia_seven_images
    global existing_images

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
                    existing_images += 1

                elif continuum_flare not in data:
                    try:
                        print("------ CONTINUUM IMAGE DOWNLOAD --------")
                        dc = 'hmi.Ic_45s['+date_flare + \
                            '_'+list_time+'_TAI/30m@30m]'
                        dc = dc.replace(" ", "")  # Removes blank spaces
                        # Using url/fits
                        r = c.export(dc, method='url', protocol='fits')
                        r.wait()
                        r.status
                        r.request_url
                        if 'X' in row[type_field]:
                            r.download(config.path_save_images +
                                       enum.Wavelenghts.CONTINUUM.value + '/x')

                        elif 'M' in row[type_field]:
                            r.download(enum.Wavelenghts.CONTINUUM.value + '/m')

                        elif 'C' in row[type_field]:
                            r.download(enum.Wavelenghts.CONTINUUM.value + '/c')

                        elif 'B' in row[type_field]:
                            r.download(enum.Wavelenghts.CONTINUUM.value + '/b')

                        continuum_images += 1

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

                # Downloading images on AIA 1600 --------------------------------------------
                sixteenHundredFlare = current_flare + "A16"
                if sixteenHundredFlare in data:
                    existing_images += 1

                elif sixteenHundredFlare not in data:
                    try:
                        print("------ AIA1600 IMAGE DOWNLOAD --------")
                        da = 'aia.lev1_uv_24s['+date_flare + \
                            '_'+list_time+'/30m@30m][1600]'
                        da = da.replace(" ", "")  # Removes blank spaces
                        r = c.export(da, method='url', protocol='fits')
                        r.wait()
                        r.status
                        r.request_url

                        if 'X' in row[type_field]:
                            r.download(enum.Wavelenghts.AIA1600.value + '/x')

                        elif 'M' in row[type_field]:
                            r.download(enum.Wavelenghts.AIA1600.value + '/m')

                        elif 'C' in row[type_field]:
                            r.download(enum.Wavelenghts.AIA1600.value + '/c')

                        elif 'B' in row[type_field]:
                            r.download(enum.Wavelenghts.AIA1600.value + '/b')

                        aia_six_images += 1

                        with open(enum.Files.CONTROL.value, 'ab+') as write_control_file:
                            write_control_file.write(
                                sixteenHundredFlare.encode('utf-8'))
                            write_control_file.write('|'.encode('utf-8'))

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

                # Downloading images on AIA 1700 --------------------------------------------
                seventeenHundredFlare = current_flare + "A17"
                if seventeenHundredFlare in data:
                    existing_images += 1

                elif seventeenHundredFlare not in data:
                    try:
                        print("------ AIA1700 IMAGE DOWNLOAD --------")
                        daia = 'aia.lev1_uv_24s['+date_flare + \
                            '_'+list_time+'/30m@30m][1700]'
                        daia = daia.replace(" ", "")  # Removes blank spaces
                        r = c.export(daia, method='url', protocol='fits')

                        r.wait()
                        r.status
                        r.request_url

                        if 'X' in row[type_field]:
                            r.download(enum.Wavelenghts.AIA1700.value + '/x')

                        elif 'M' in row[type_field]:
                            r.download(enum.Wavelenghts.AIA1700.value + '/m')

                        elif 'C' in row[type_field]:
                            r.download(enum.Wavelenghts.AIA1700.value + '/c')

                        elif 'B' in row[type_field]:
                            r.download(enum.Wavelenghts.AIA1700.value + '/b')

                        aia_seven_images += 1

                        with open(enum.Files.CONTROL.value, 'ab+') as write_control_file:
                            write_control_file.write(
                                seventeenHundredFlare.encode('utf-8'))
                            write_control_file.write('|'.encode('utf-8'))

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

    print("Download complete!")
    print("\n\n ----------------------------------------------------- ")
    print("Total of images downloaded: ", aia_seven_images +
          aia_six_images + continuum_images)
    print("HMI Continuum images: ", continuum_images)
    print("AIA 1600 images: ", aia_six_images)
    print("AIA 1700 images: ", aia_seven_images)
    print(existing_images, "weren't downloaded to avoid duplication.")

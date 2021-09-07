import sys
import drms
import os
import csv
import urllib
import time

# from tqdm import tqdm
from time import sleep

from model import configuration
from model import wavelenghts as enum


def downloadImages(validFile, configuration):

    # TODO Review imports and remove unused ones

    # DO NOT CHANGE
    # TODO Create enum
    # TODO check on wavelengths array on drms package

    date_field = configuration.date_field
    time_field = configuration.time_field
    type_field = configuration.type_field

    # Creates an instance of drms.Client class
    c = drms.Client(email=configuration.email, verbose=True)

    fitsFiles = 0
    pngFiles = 0
    fitsConverted = 0
    # This function is responsible to make sure that the file with valid data exists and has the right header

    # Function responsible to download the images based on the validFile

    # TODO Refactor download images
    # TODO controlFile has the same name on different files, padronize this somewhere

    controlFile = 'controlDownloads.bin'  # Control file
    controlWebSite = 0

    global continuum_images
    global aia_six_images
    global aia_seven_images
    global existing_images

    print("Starting downloading process")
    with open(validFile, 'r') as inputFile:
        rows = csv.DictReader(inputFile)
        for row in rows:
            dateFlare = row[date_field]
            timeFlare = row[time_field]
            listTime = timeFlare[:-3]

            # Relevant informations about current flare, to compare and avoid replication
            currentFlare = dateFlare + "_" + timeFlare
            currentFlare = currentFlare.replace(" ", "")

            # Read control file and decode it into "data"
            with open(controlFile, 'rb') as controlFileR:
                data = controlFileR.read()
                data = data.decode('utf-8')
                data = str(data)
                data = data.split('|')

                # Downloading images on HMI Continuum --------------------------------------------
                continuumFlare = currentFlare + "C"  # Control flare continuum
                if continuumFlare in data:  # Verify if the image has already been downloaded
                    existing_images += 1

                elif continuumFlare not in data:
                    try:
                        print("------ CONTINUUM IMAGE DOWNLOAD --------")
                        dc = 'hmi.Ic_45s['+dateFlare + \
                            '_'+listTime+'_TAI/30m@30m]'
                        dc = dc.replace(" ", "")  # Removes blank spaces
                        # Using url/fits
                        r = c.export(dc, method='url', protocol='fits')
                        r.wait()
                        r.status
                        r.request_url
                        if 'X' in row[type_field]:
                            r.download(enum.Wavelenghts.CONTINUUM + '/x')

                        elif 'M' in row[type_field]:
                            r.download(enum.Wavelenghts.CONTINUUM + '/m')

                        elif 'C' in row[type_field]:
                            r.download(enum.Wavelenghts.CONTINUUM + '/c')

                        elif 'B' in row[type_field]:
                            r.download(enum.Wavelenghts.CONTINUUM + '/b')

                        continuum_images += 1

                    except drms.DrmsExportError:
                        print(
                            "Current image doesn't have records online. It can't be downloaded.")
                        with open('notFound.bin', 'rb+') as notFoundFile:
                            notFoundData = notFoundFile.read()
                            notFoundData = notFoundData.decode('utf-8')
                            notFoundData = str(notFoundData)

                        newRow = row[type_field] + "," + row['Year'] + "," + row['Spot'] + \
                            "," + row['Start'] + "," + \
                            row[time_field] + "," + row['End']
                        if newRow not in notFoundData:
                            with open('notFound.bin', 'ab+') as notFoundFile:
                                notFoundFile.write(newRow.encode('utf-8'))
                                notFoundFile.write('|'.encode('utf-8'))

                    except urllib.error.HTTPError:
                        print("The website appers to be offline.")
                        if controlWebSite < 5:
                            print("Trying to reconnet. Attempt ",
                                  controlWebSite, " of 5.")
                            time.sleep(60)
                            downloadImages(validFile, configuration)

                        else:
                            print(
                                "The website is offline. Try to run the script again in a few minutes.")

                    with open(controlFile, 'ab+') as controlFileW:
                        controlFileW.write(continuumFlare.encode('utf-8'))
                        controlFileW.write('|'.encode('utf-8'))

                # Downloading images on AIA 1600 --------------------------------------------
                sixteenHundredFlare = currentFlare + "A16"
                if sixteenHundredFlare in data:
                    existing_images += 1

                elif sixteenHundredFlare not in data:
                    try:
                        print("------ AIA1600 IMAGE DOWNLOAD --------")
                        da = 'aia.lev1_uv_24s['+dateFlare + \
                            '_'+listTime+'/30m@30m][1600]'
                        da = da.replace(" ", "")  # Removes blank spaces
                        r = c.export(da, method='url', protocol='fits')
                        r.wait()
                        r.status
                        r.request_url

                        if 'X' in row[type_field]:
                            r.download(enum.Wavelenghts.AIA1600 + '/x')

                        elif 'M' in row[type_field]:
                            r.download(enum.Wavelenghts.AIA1600 + '/m')

                        elif 'C' in row[type_field]:
                            r.download(enum.Wavelenghts.AIA1600 + '/c')

                        elif 'B' in row[type_field]:
                            r.download(enum.Wavelenghts.AIA1600 + '/b')

                        aia_six_images += 1

                        with open(controlFile, 'ab+') as controlFileW:
                            controlFileW.write(
                                sixteenHundredFlare.encode('utf-8'))
                            controlFileW.write('|'.encode('utf-8'))

                    except drms.DrmsExportError:
                        print(
                            "Current image doesn't have records online. It can't be downloaded.")
                        with open('notFound.bin', 'rb+') as notFoundFile:
                            notFoundData = notFoundFile.read()
                            notFoundData = notFoundData.decode('utf-8')
                            notFoundData = str(notFoundData)

                        newRow = row[type_field] + "," + row['Year'] + "," + row['Spot'] + \
                            "," + row['Start'] + "," + \
                            row[time_field] + "," + row['End']
                        if newRow not in notFoundData:
                            with open('notFound.bin', 'ab+') as notFoundFile:
                                notFoundFile.write(newRow.encode('utf-8'))
                                notFoundFile.write('|'.encode('utf-8'))

                    except urllib.error.HTTPError:
                        print("The website appers to be offline.")
                        if controlWebSite < 5:
                            print("Trying to reconnet. Attempt ",
                                  controlWebSite, " of 5.")
                            time.sleep(60)
                            downloadImages(validFile, configuration)

                        else:
                            print(
                                "The website is offline. Try to run the script again in a few minutes.")

                # Downloading images on AIA 1700 --------------------------------------------
                seventeenHundredFlare = currentFlare + "A17"
                if seventeenHundredFlare in data:
                    existing_images += 1

                elif seventeenHundredFlare not in data:
                    try:
                        print("------ AIA1700 IMAGE DOWNLOAD --------")
                        daia = 'aia.lev1_uv_24s['+dateFlare + \
                            '_'+listTime+'/30m@30m][1700]'
                        daia = daia.replace(" ", "")  # Removes blank spaces
                        r = c.export(daia, method='url', protocol='fits')

                        r.wait()
                        r.status
                        r.request_url

                        if 'X' in row[type_field]:
                            r.download(enum.Wavelenghts.AIA1700 + '/x')

                        elif 'M' in row[type_field]:
                            r.download(enum.Wavelenghts.AIA1700 + '/m')

                        elif 'C' in row[type_field]:
                            r.download(enum.Wavelenghts.AIA1700 + '/c')

                        elif 'B' in row[type_field]:
                            r.download(enum.Wavelenghts.AIA1700 + '/b')

                        aia_seven_images += 1

                        with open(controlFile, 'ab+') as controlFileW:
                            controlFileW.write(
                                seventeenHundredFlare.encode('utf-8'))
                            controlFileW.write('|'.encode('utf-8'))

                    except drms.DrmsExportError:
                        print(
                            "Current image doesn't have records online. It can't be downloaded.")
                        with open('notFound.bin', 'rb+') as notFoundFile:
                            notFoundData = notFoundFile.read()
                            notFoundData = notFoundData.decode('utf-8')
                            notFoundData = str(notFoundData)

                        newRow = row[type_field] + "," + row['Year'] + "," + row['Spot'] + \
                            "," + row['Start'] + "," + \
                            row[time_field] + "," + row['End']
                        if newRow not in notFoundData:
                            with open('notFound.bin', 'ab+') as notFoundFile:
                                notFoundFile.write(newRow.encode('utf-8'))
                                notFoundFile.write('|'.encode('utf-8'))

                    except urllib.error.HTTPError:
                        print("The website appers to be offline.")
                        if controlWebSite < 5:
                            print("Trying to reconnet. Attempt ",
                                  controlWebSite, " of 5.")
                            time.sleep(60)
                            downloadImages(validFile, configuration)

                        else:
                            print(
                                "The website is offline. Try to run the script again in a few minutes.")

    totalImages = aia_seven_images + aia_six_images + continuum_images
    print("Download complete!")
    print("\n\n ----------------------------------------------------- ")
    print("Total of images downloaded: ", totalImages)
    print("HMI Continuum images: ", continuum_images)
    print("AIA 1600 images: ", aia_six_images)
    print("AIA 1700 images: ", aia_seven_images)
    print(existing_images, "weren't downloaded to avoid duplication.")

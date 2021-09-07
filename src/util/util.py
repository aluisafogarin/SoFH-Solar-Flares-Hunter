import os
import csv

from model import config_infos as config


def createFolders(wavelength):
    os.mkdir(wavelength)
    for folder_name in ['/x', '/m', '/c', '/b']:
        os.mkdir(wavelength + folder_name)

    os.mkdir(wavelength + os.sep + 'png')
    for folder_name in ['/png/x', '/png/m', '/png/c', '/png/b']:
        os.mkdir(wavelength + folder_name)


def createFiles(filePath, mode):
    if '.csv' in filePath:
        with open(filePath, mode) as file:
            w = csv.DictWriter(file, config.Config.fieldnames)
            w.writeheader()

    else:
        file = open(filePath, mode)
        file.close


def verifyOutputFile(filePath, validFile, infoFile):

    createFile = filePath + os.sep + validFile   # Adress of the file

    if not os.path.exists(createFile):  # Creates the file if necessary
        outputFile = filePath + os.sep + validFile

        # Write the header of the file, this way prevent replication
        with open(outputFile, 'w') as csvfile:
            # Path to write on the file
            w = csv.DictWriter(csvfile, config.Config.fieldnames)
            w.writeheader()

# This function is responsible to record only the data older than 2011 on the validFile that will be used to download images


def verifyDate(filePath, validFile, infoFile, params):
    controlE = 0
    controlN = 0

    with open(infoFile) as inputFile:
        # DictReader allow do get only some specify part of the file, based on the header
        rowReader = csv.DictReader(inputFile)

        for row in rowReader:
            completeRow = row  # Receives the row
            # Separate the column "Year" using "-" as the separation point
            dateList = row[config.Config.dateField].split("-")
            # All the years (position 0) goes to "year"
            year = dateList[0]

            if (int(year) > 2011):
                # Before recording, it should verify if the row is already on the validFile
                readFile = open(filePath + os.sep + validFile, 'r')
                reader = csv.DictReader(readFile)
                for existingRow in reader:
                    if completeRow == existingRow:
                        controlE = 1
                        params.oldLines += 1

                    elif completeRow != existingRow:
                        controlN = 1
                readFile.close

                # Recording on validFile
                # ControlE = 0 and ControlN = 1: current line wasn't recorded
                # ControlE = 0 and ControlN = 0: current line is the first
                if (controlE == 0 and controlN == 1) or (controlE == 0 and controlN == 0):

                    outputFile = open(validFile, 'a', newline='')
                    # Path to write on the file
                    write = csv.DictWriter(
                        outputFile, config.Config.fieldnames)
                    write.writerow({'Type': row['Type'], 'Year': row['Year'], 'Spot': row['Spot'],
                                   'Start': row['Start'], 'Max': row['Max'], 'End': row['End']})
                    params.newLines += 1
                    outputFile.close

            else:
                params.invalidLines += 1

    print("Success on the verification!")
    print(params.newLines, " lines were add to the file", validFile)
    print(params.oldLines, " lines already exists on the file, and weren't duplicated")
    print(params.invalidLines, " lines were invalid and weren't add to the file")

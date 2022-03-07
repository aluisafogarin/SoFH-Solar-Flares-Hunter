import os
import csv


def create_folders(wavelengths, image_types, output_directory):

    def create_wavelenght_folder(wave):
        os.mkdir(output_directory + os.sep + wave)

    def create_image_type_folder(wave, output_type):
        os.mkdir(output_directory + os.sep + wave + os.sep + output_type)

    def create_flare_type_folder(wave, output_type, flare_type):
        os.mkdir(output_directory + os.sep + wave + os.sep + output_type +
                 os.sep + flare_type)

    for index, wave in enumerate(wavelengths):
        if index <= len(wavelengths):
            if not os.path.exists(output_directory + os.sep + wave):
                create_wavelenght_folder(wave)

                for output_type in image_types:
                    if not os.path.exists(output_directory + os.sep + wave + os.sep + output_type):
                        create_image_type_folder(wave, output_type)

                        for flare_type in ['x', 'm', 'c', 'b']:
                            if not os.path.exists(output_directory + os.sep + wave + os.sep + output_type +
                                                  os.sep + flare_type):
                                create_flare_type_folder(
                                    wave, output_type, flare_type)

                    elif not(os.path.exists(output_directory + os.sep + wave + os.sep + output_type)):
                        for output_type in image_types:
                            if not os.path.exists(output_directory + os.sep + wave + os.sep + output_type):
                                create_image_type_folder(wave, output_type)

        # for (flare_type, output_type) in zip(['x', 'm', 'c', 'b'], image_types):
        #     print("---- " + flare_type + "---- " + output_type)
        #     print("Creating folder: " + output_directory +
        #           os.sep + wave + os.sep + flare_type)
        #     os.mkdir(output_directory + os.sep +
        #              wave + os.sep + flare_type)
        #     print("saindo do for interno")

        # for output_type in image_types:
        #     print("Creating folder: " + output_directory + os.sep + wave +
        #           os.sep + output_type + os.sep + flare_type)
        #     os.mkdir(output_directory + wave +
        #              output_type + flare_type)


def create_files(filePath, mode, config):
    if '.csv' in filePath:
        with open(filePath, mode) as file:
            w = csv.DictWriter(file, config.fieldnames)
            w.writeheader()

    else:
        file = open(filePath, mode)
        file.close


def verify_output_file(filePath, validFile, infoFile, config):

    createFile = filePath + os.sep + validFile   # Adress of the file

    if not os.path.exists(createFile):  # Creates the file if necessary
        outputFile = filePath + os.sep + validFile

        # Write the header of the file, this way prevent replication
        with open(outputFile, 'w') as csvfile:
            # Path to write on the file
            w = csv.DictWriter(csvfile, config.fieldnames)
            w.writeheader()

# This function is responsible to record only the data older than 2011 on the validFile that will be used to download images


def verify_date(filePath, validFile, infoFile, params, config):
    controlE = 0
    controlN = 0

    with open(infoFile) as inputFile:
        # DictReader allow do get only some specify part of the file, based on the header
        rowReader = csv.DictReader(inputFile)

        for row in rowReader:
            completeRow = row  # Receives the row
            # Separate the column "Year" using "-" as the separation point
            dateList = row[config.date_field].split("-")
            # All the years (position 0) goes to "year"
            year = dateList[0]

            if (int(year) > 2011):
                # Before recording, it should verify if the row is already on the validFile
                readFile = open(filePath + os.sep + validFile, 'r')
                reader = csv.DictReader(readFile)
                for existingRow in reader:
                    if completeRow == existingRow:
                        controlE = 1
                        params.old_lines += 1

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
                        outputFile, config.fieldnames)
                    write.writerow({'Type': row['Type'], 'Year': row['Year'], 'Spot': row['Spot'],
                                   'Start': row['Start'], 'Max': row['Max'], 'End': row['End']})
                    params.new_lines += 1
                    outputFile.close

            else:
                params.invalid_lines += 1

    print("Success on the verification!")
    print(params.new_lines, " lines were add to the file", validFile)
    print(params.old_lines, " lines already exists on the file, and weren't duplicated")
    print(params.invalid_lines, " lines were invalid and weren't add to the file")

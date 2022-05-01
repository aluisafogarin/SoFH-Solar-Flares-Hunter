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


def create_files(file_path, mode, config):
    if '.csv' in file_path:
        with open(file_path, mode, encoding="utf8") as file:
            w = csv.DictWriter(file, config.fieldnames)
            w.writeheader()

    else:
        file = open(file_path, mode, encoding="utf8")
        file.close


def verify_output_file(file_path, valid_file, info_file, config):

    createFile = file_path + os.sep + valid_file   # Adress of the file

    if not os.path.exists(createFile):  # Creates the file if necessary
        output_file = file_path + os.sep + valid_file

        # Write the header of the file, this way prevent replication
        with open(output_file, 'w') as csvfile:
            # Path to write on the file
            w = csv.DictWriter(csvfile, config.fieldnames)
            w.writeheader()

# This function is responsible to record only the data older than 2011 on the valid_file that will be used to download images


def verify_date(file_path, valid_file, info_file, params, config):
    control_existing = 0
    control_not_existing = 0

    with open(info_file, encoding="utf8") as input_file:
        # DictReader allow do get only some specify part of the file, based on the header
        row_reader = csv.DictReader(input_file)

        for row in row_reader:
            complete_row = row  # Receives the row
            # Separate the column "Year" using "-" as the separation point
            date_list = row[config.date_field].split("-")
            # All the years (position 0) goes to "year"
            year = date_list[0]

            if (int(year) > 2011):
                # Before recording, it should verify if the row is already on the valid_file
                read_file = open(file_path + os.sep +
                                 valid_file, 'r', encoding="utf8")
                reader = csv.DictReader(read_file)
                for existing_row in reader:
                    if complete_row == existing_row:
                        control_existing = 1
                        params.old_lines += 1

                    elif complete_row != existing_row:
                        control_not_existing = 1
                read_file.close

                # Recording on valid_file
                # ControlE = 0 and ControlN = 1: current line wasn't recorded
                # ControlE = 0 and ControlN = 0: current line is the first
                if (control_existing == 0 and control_not_existing == 1) or (control_existing == 0 and control_not_existing == 0):

                    output_file = open(
                        valid_file, 'a', newline='', encoding="utf8")
                    # Path to write on the file
                    write = csv.DictWriter(
                        output_file, config.fieldnames)
                    write.writerow({'Type': row['Type'], 'Year': row['Year'], 'Spot': row['Spot'],
                                   'Start': row['Start'], 'Max': row['Max'], 'End': row['End']})
                    params.new_lines += 1
                    output_file.close

            else:
                params.invalid_lines += 1

    print("Success on the verification!")
    print(params.new_lines, " lines were add to the file", valid_file)
    print(params.old_lines, " lines already exists on the file, and weren't duplicated")
    print(params.invalid_lines, " lines were invalid and weren't add to the file")

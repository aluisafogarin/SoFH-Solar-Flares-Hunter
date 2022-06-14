
"""
Utility class
"""

import os
import csv


def create_folders(wavelengths, image_types, output_directory, create_type):
    """ Configure and create folders according to recording parameters

    Args:
        wavelenghts (array): Wavelenghts for download images
        image_types (array): Wantend image extension to download
        output_directory (string): Output to save downloaded images
        create_type (boolean): If folders using flare types (x, m, c and b) should be created
    """

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

                if create_type:
                    for output_type in image_types:
                        if not os.path.exists(output_directory + os.sep +
                                              wave + os.sep + output_type):
                            create_image_type_folder(wave, output_type)

                            for flare_type in ['x', 'm', 'c', 'b']:
                                if not os.path.exists(output_directory + os.sep +
                                                      wave + os.sep + output_type +
                                                      os.sep + flare_type):
                                    create_flare_type_folder(
                                        wave, output_type, flare_type)

                        elif not(os.path.exists(output_directory + os.sep +
                                                wave + os.sep + output_type)):
                            for output_type_else in image_types:
                                if not os.path.exists(output_directory + os.sep +
                                                      wave + os.sep + output_type_else):
                                    create_image_type_folder(
                                        wave, output_type_else)


def create_files(path_info_file, mode, config):
    """ Create files

    Args:
        path_info_file (string): Path where the file must be created
        mode (string): Mode to open the file
        config (object): Object of configuration class
    """

    if '.csv' in path_info_file:
        with open(path_info_file, mode) as file:
            write = csv.DictWriter(file, config.fieldnames)
            write.writeheader()

    else:
        file = open(path_info_file, mode)


def verify_output_file(path_info_file, path_valid_file, config):
    """ Checks if output file exists and has fieldnames written

    Args:
        path_info_file (string): Path where the file with flare information is located
        path_valid_file (string): Path where the file with verified flare information is located
        config (object): Object of configuration class
    """

    create_file = path_info_file + os.sep + path_valid_file   # Adress of the file

    if not os.path.exists(create_file):  # Creates the file if necessary
        output_file = path_info_file + os.sep + path_valid_file

        # Write the header of the file, this way prevent replication
        with open(path_info_file, 'w', encoding="utf=8") as csvfile:
            # Path to write on the file
            write = csv.DictWriter(csvfile, config.fieldnames)
            write.writeheader()


def verify_date(path_info_file, path_valid_file, control, config):
    """ Record only data older than 2011 on the path_valid_file that will be used to download images

    Args:
        path_info_file (string): Path where the file with flare information is located
        path_valid_file (string): Path where the file with verified flare information is located
        config (object): Object of configuration class
    """

    control_existing = 0
    control_not_existing = 0

    with open(path_info_file) as input_file:
        # DictReader allow do get only some specify part of the file, based on the header
        row_reader = csv.DictReader(input_file)

        for row in row_reader:
            complete_row = row  # Receives the row
            # Separate the column "Year" using "-" as the separation point
            date_list = row[config.date_field].split("-")
            # All the years (position 0) goes to "year"
            year = date_list[0]

            if int(year) >= 2011:
                # Before recording, it should verify if the row is already on the path_valid_file
                read_file = open(path_valid_file, 'r')
                reader = csv.DictReader(read_file)
                for existing_row in reader:
                    if complete_row == existing_row:
                        control_existing = 1
                        control.old_lines += 1

                    elif complete_row != existing_row:
                        control_not_existing = 1

                # Recording on path_valid_file
                # control_existing = 0 and control_not_existing = 1: current line wasn't recorded
                # control_existing = 0 and control_not_existing = 0: current line is the first
                if (control_existing == 0
                    and control_not_existing == 1) or (control_existing == 0
                                                       and control_not_existing == 0):
                    output_file = open(
                        path_valid_file, 'a', newline='')
                    # Path to write on the file
                    print(config.fieldnames)
                    write = csv.DictWriter(
                        output_file, config.fieldnames)
                    write.writerow({"Type": row["Type"], "Year": row["Year"], "Spot": row["Spot"],
                                   "Start": row["Start"], "Max": row["Max"], "End": row["End"]})
                    control.new_lines += 1

            else:
                control.invalid_lines += 1

    print("Success on the verification!")
    print(control.new_lines, " lines were add to the file", path_valid_file)
    print(control.old_lines,
          " lines already exists on the file, and weren't duplicated")
    print(control.invalid_lines, " lines were invalid and weren't add to the file")

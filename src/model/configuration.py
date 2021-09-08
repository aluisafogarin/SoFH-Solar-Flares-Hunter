import os


class ConfigurationValues:
    fieldnames = []
    date_field = 'Year'
    time_field = 'Max'
    type_field = 'Type'

    info_file = ''
    path_info_file = ''

    path_save_images = ''

    def __init__(self, email, fieldnames, info_file, path_info_file, path_save_images):
        self.email = email
        for field in fieldnames:
            self.fieldnames.append(field)
        self.info_file = info_file
        self.path_info_file = path_info_file
        self.path_save_images = path_save_images


class ControlVariables:
    continuum_images = 0
    aia_six_images = 0
    aia_seven_images = 0
    existing_images = 0
    invalid_lines = 0
    new_lines = 0
    old_lines = 0

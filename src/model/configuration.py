import os


class ConfigurationValues:
    fieldnames = []
    date_field = 'Year'
    time_field = 'Max'
    type_field = 'Type'

    file_name = ''

    def __init__(self, email, fieldnames):
        self.email = email
        for field in fieldnames:
            self.fieldnames.append(field)


class ControlVariables:
    continuum_images = 0
    aia_six_images = 0
    aia_seven_images = 0
    existing_images = 0
    invalid_lines = 0
    new_lines = 0
    old_lines = 0

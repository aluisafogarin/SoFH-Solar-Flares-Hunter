class ConfigurationDownload:
    fieldnames = []
    date_field = 'Year'
    time_field = 'Max'
    type_field = 'Type'
    email = ''

    # File with flare informations
    info_file = ''
    path_info_file = ''

    # File only with valid flares (older than 2011)
    valid_file = ''
    path_valid_file = ''

    # Output folder with downloaded images
    path_output_folder = ''

    wavelenghts = []
    output_image_types = []


class ConfigurationConversion:
    # Key: image name, value: image path
    load_images = {}
    images_to_convert = {}

    extensions = []
    wavelenghts = []
    path_save_images = ''


class ControlConversion:
    fits_files = 0
    png_files = 0
    fits_converted = 0


class ControlDownload:
    continuum_images = 0
    aia_six_images = 0
    aia_seven_images = 0
    existing_images = 0
    invalid_lines = 0
    new_lines = 0
    old_lines = 0

from enum import Enum

# TODO check on wavelengths array on drms package


class Wavelenghts(Enum):
    CONTINUUM = 'continuum'
    MAGNETOGRAMS = 'magnetograms'
    AIA1600 = 'aia1600'
    AIA1700 = 'aia1700'


class ExtensionImages(Enum):
    PNG = 'png'
    FITS = 'fits'
    JPEG = 'jpg'


class Files(Enum):
    CONTROL = 'control_downloads.bin'
    NOT_FOUND_BIN = 'not_found.bin'
    NOT_FOUND_CSV = 'not_found.csv'
    LOG = 'log.log'
    LOG_DOWNLOAD = 'download_log.log'
    LOG_CONVERT = 'convert_log.log'


class Download(Enum):
    TIME_BREAK = '30m@30m'

    CONTINUUM = 'hmi.Ic_45s'
    MAGNETOGRAMS = 'hmi.M_45s '
    AIA = 'aia.lev1_uv_24s'


class Conversion(Enum):
    JPEG = 'jpeg'
    PNG = 'png'

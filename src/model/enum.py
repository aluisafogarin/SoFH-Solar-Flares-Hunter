from enum import Enum

# TODO check on wavelengths array on drms package


class Wavelenghts(Enum):
    CONTINUUM = 'continuum'
    MAGNETOGRAMS = 'magnetograms'
    AIA1600 = 'aia1600'
    AIA1700 = 'aia1700'


class Files(Enum):
    CONTROL = 'control_downloads.bin'


class Download(Enum):
    TIME_BREAK = '30m@30m'

    CONTINUUM = 'hmi.Ic_45s'
    MAGNETOGRAMS = 'hmi.M_45s '
    AIA = 'aia.lev1_uv_24s'

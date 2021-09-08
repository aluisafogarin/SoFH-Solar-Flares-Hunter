from enum import Enum

# TODO check on wavelengths array on drms package


class Wavelenghts(Enum):
    CONTINUUM = 'continuum'
    AIA1600 = 'aia1600'
    AIA1700 = 'aia1700'


class Files(Enum):
    CONTROL = 'control_downloads.bin'

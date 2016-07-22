import json

from file_io import FileIO

debug = True
verbose = True

class Cycler:
    """A representation of the PTC-200 DNA Engine Thermal Cycler 
    integrated with the OT.One platform
    """
#Special Methods ---------------------
    def __init__(self):
    if debug == True: FileIO.log('

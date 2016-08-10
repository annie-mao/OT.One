import sys
sys.path.insert(0.'../otone_backend/backend')
from file_io import FileIO
import json

""" cycler_lib class facilitating update/generation of
cycler_lib.json file
"""

class Cycler_Lib:
    """ Python way to generate/update cycler_lib.json
    """
    def __init__(self,fname):
        self.cyclerDict = {"cycler_lib":{}}
        if fname is not None:
            self.load_JSON(fname)

    def load_JSON(self,fname):
        """ Read in current cycler_lib.json and convert
        from JSON to python dict
        """
        self.cyclerDict = FileIO.get_dict_from_json(fname)

    def print_program_info(self,progName):
        try:
            print(progName)
            for fieldStr,fieldVal in self.cyclerDict["cycler_lib"][progName].items():
                print('{0}: {1}'.format(fieldStr,fieldVal))
            print('\n')
        except KeyError:
            print('{0} does not exist in library'.format(progName))

    def print_programs(self):
        try:
            print('All cycler programs')
            for progName,v in self.cyclerDict["cycler_lib"].items()
                print(progName)
        except KeyError:
            print('No programs in cycler library')

    def add_program(self,progName,runtime,holdTemp=None)

import datetime

from collections import OrderedDict
from containers import Containers

class baseProtocol:
    """ Python representation of a liquid-handling protocol
    Enables smart selection of containers and deck layout
    """

    def __init__(self,name,description,notes):
        self.info = {
            "name": name,
            "description": description,
            "create-date": str(datetime.date.today()), 
            "run-notes": notes
        }
        self.locations={}
        self.ingredients={}
        self.instructions={}
        self.transfer_defaults={
            "from":{
                "tip-offset":0,
                "touch-tip":False,
                "delay":0,
                "liquid-tracking":True
            }
            "to":{
                "tip-offset":0,
                "touch-tip":True,
                "delay":0,
                "liquid-tracking":True
            }
            "blowout":True,
            "extra-pull"False

        }
        self.mix_defaults={
            "repetitions":5,
            "blowout":True,
            "liquid-tracking":True
        }

    def print_info(self,key):
        print(self.key)
    
    def configure_transfer_tofrom(to_from,key,value):
        self.transfer_defaults[to_from][key]=value

    def configure_transfer(key,value):
        self.transfer_defaults[key]=value

    def configure_mix(key,value):
        self.mix_defaults[key]=value

    def add_ingredient(self,ingName,locName,volume):
        if(ingName is not in self.ingredients):
            #add ingredient to dict
            self.ingredients[ingName]={locName:volume}
            if(locName is not in self.locations and locName is not None):
                #if ingredient and location are new
                #add location to dict
                self.locations[locName]={
                    "volume":volume,
                    "maxVol":volume
                }
            if(locName is in self.locations and locName is not None):
                #if new ingredient but existing location
                #update location
                self.locations[locName]["volume"]+=volume
                if(self.locations[locName]["volume"]>self.locations[locName]["maxVol"]):
                    self.locations[locName]["maxVol"]=self.locations[locName]["volume"]
                #add new initial location
                self.locations[locName+"_initial"]={
                    "volume":0,
                    "maxVol":volume
                }
                #add instruction to transfer ing from initial location to current location
                self.instructions

    def make_transfer_group

    def add_transfer(self,transferGroup,settings=self.transfer_defaults):
        self.instructions["transfer"


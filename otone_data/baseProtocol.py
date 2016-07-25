import datetime

from collections import OrderedDict
from containers import Containers

class BaseProtocol:
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
        self.instructions=[]
        self.transfer_defaults={
            "from":{
                "tip-offset":0,
                "touch-tip":False,
                "delay":0,
                "liquid-tracking":True
            },
            "to":{
                "tip-offset":0,
                "touch-tip":True,
                "delay":0,
                "liquid-tracking":True
            },
            "blowout":True,
            "extra-pull":False

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

    def add_ingredient(self,ingrName,locName,volume):
        if(ingrName not in self.ingredients):
            #if adding to an unspecified location (None), pool all volumes of the same
            #ingredient in one initial pool called ingrName_initial
            if not locName:
                locName = ingrName+"_initial"
            #new ingredient -- add ingredient to dict
            self.ingredients[ingrName]={locName:volume}
            if locName not in self.locations:
                #if ingredient and location are new
                #add location to dict
                self.locations[locName]={
                    "volume":volume,
                    "maxVol":volume
                }
            elif locName in self.locations:
                #if new ingredient but existing location
                #update location
                self.update_loc_vol(locName,volume,True)
                #add new initial location for the ingredient
                self.locations[ingrName+"_initial"]={
                    "volume":0,
                    "maxVol":volume
                }
                #add instruction to transfer ingr from initial location to current location
                self.make_transfer_group([ingrName+"_initial"],[locName],[volume])

        else:
            #existing ingredient
            #if adding to unspecified location, set location to ingredient's initial pool
            if not locName:
                locName = ingrName+"_initial"
            #update volume in ingredients dictionary
            self.ingredients[ingrName][locName]=self.ingredients[ingrName].setdefault(locName,0)+volume
            if locName not in self.locations:
                #if existing ingredient to new location
                #add location to dict
                self.locations[locName]={
                    "volume":volume,
                    "maxVol":volume
                }
            elif locName in self.locations and locName != ingrName+"_initial":
                #if existing ingredient to existing location
                #update location
                self.update_loc_vol(locName,volume,True)
                #assume ingredient is coming from ingredient's initial pool
                #create initial pool location if not already in locations dict
                if(ingrName+"_initial" not in self.locations):
                    self.locations[ingrName+"_initial"]={
                        "volume":0,
                        "maxVol":volume
                    }
                #update initial pool if already in dict
                else:
                    self.update_loc_vol(ingrName+"_initial",volume,False)
                #add instruction to transfer ingr from initial location to current location
                self.make_transfer_group([ingrName+"_initial"],[locName],[volume])
            elif locName == ingrName+"_initial":
                #if adding existing ingredient to its initial pool
                #update location
                self.update_loc_vol((ingrName+"_initial"),volume,True)
        return "Added "+ingrName+" to "+locName

    def update_loc_vol(self,locName,addVol,keepVol):
        #sanity check to make sure volume does not go negative
        if self.locations[locName]["volume"]+addVol<0:
            print("Error: attempt to create negative volume at {0}".format(locName))
            return
        elif (self.locations[locName]["volume"]+addVol)>self.locations[locName]["maxVol"]:
            self.locations[locName]["maxVol"]=self.locations[locName]["volume"]+addVol
        if keepVol:
            self.locations[locName]["volume"]+=addVol

    def update_ingr_vol(self,ingrName,locsToChange,volChanges):
        for i in range(0,len(locsToChange)):
            self.ingredients[ingrName][locsToChange[i]]+=volChanges

    def make_transfer_group(self,fromLocs,toLocs,volumes,changeSettings=None):
        # add instruction to list
        transferGroup = []
        for i in range(0,len(fromLocs)):
            transferDict={
                "from":{"locName":fromLocs[i]},
                "to":{"locName":toLocs[i]},
                "volume":volumes[i]
            }
            if changeSettings:
                for key,value in changeSettings[i].items():
                    if key=="from" or key=="to":
                        for nextkey,nextvalue in value.items():
                            transferDict[key][nextkey]=nextvalue
                    else:
                        transferDict[key]=value
            # fill in missing fields with defaults
            transferDict=self.fill_transfer_defaults(transferDict)
            # add to list of transfers in this group (same tip)
            transferGroup.append(transferDict)
            # update locations dict
            self.update_loc_vol(fromLocs[i],-volumes[i])
            self.update_loc_vol(toLocs[i],volumes[i])
            # update ingredients dict
            self.update_ingr_vol([fromLocs[i],toLocs[i]],[-volumes[i],volumes[i]])
        self.instructions.append(transferGroup)

        # update volumes of ingredient and location dicts

    
    def fill_transfer_defaults(self,transferDict):
        # go through transfer defaults and transferDict and fill in any
        # missing fields
        for key,value in self.transfer_defaults.items():
            if key=="from" or key=="to":
                for nextkey,nextvalue in value.items():
                    transferDict[key].setdefault(nextkey,nextvalue)
            else:
                transferDict.setdefault(key,value)
        return transferDict

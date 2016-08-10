import datetime

from collections import OrderedDict
from containers import Containers

class BaseProtocol:
    """ Python representation of a liquid-handling protocol
    Enables smart selection of containers and deck layout
    """

    def __init__(self,name,description,notes):
        # load containers
        self.containers = Containers("avail_containers.json")
        
        self.info = {
            "name": name,
            "description": description,
            "create-date": str(datetime.date.today()), 
            "run-notes": notes
        }
        #TO DO: add edit capabilities for head
        self.head = {
            "p200":{
                "tool": "pipette",
                "tip-racks": [{"container": "p200-rack"}],
                "axis": "a",
                "volume": 200,
                "tip-plunge": 4,
                "points": [
                    {"f1": 20, "f2": 17.7},
                    {"f1": 100, "f2": 98.5},
                    {"f1": 200, "f2": 200}
                ]
            },
            "p10":{
                "tool": "pipette",
                "tip-racks": [{"container": "p10-rack"}],
                "axis": "b",
                "volume": 10,
                "tip-plunge": 7.5,
                "points": [
                    {"f1": 0.5, "f2": 0.41},
                    {"f1": 5, "f2": 4.7},
                    {"f1": 10, "f2": 10}
                ]
            }    
        }
        self.deck={}
        self.locations={}
        self.groupedLocs={}
        self.ingredients={} #initial deck layout/setup
        self.ingredients_export={}
        self.cycler={} #cycler programs
        self.instructions=[]
        self.head_defaults={
            "trash-container": {"container": "trash"},
            "multi-channel":  False,
            "down-plunger-speed": 300,
            "up-plunger-speed": 500,
            "extra-pull-volume": 0,
            "extra-pull-delay": 200,
            "distribute-percentage": 0.1
        }
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
        self.cycler_defaults={
            "control": "CALC",
            "lid": False,
            "vessel": "Tubes",
            "volume": 100
        }

    def print_info(self,key):
        print(self.key)
    
    def configure_transfer_tofrom(to_from,key,value):
        self.transfer_defaults[to_from][key]=value

    def configure_transfer(key,value):
        self.transfer_defaults[key]=value

    def configure_mix(key,value):
        self.mix_defaults[key]=value

    def configure_cycler(key,value):
        self.cycler_defaults[key]=value

    def configure_head(key,value):
        self.head_defaults[key]=value
    
    def set_head():
        for pipette in self.head:
            self.fill_instruction_defaults(self.head[pipette],self.head_defaults)

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
                #add loc to dict
                self.update_loc_vol(locName,volume)
            elif locName in self.locations:
                #if new ingredient but existing location
                #add new initial location for the ingredient
                self.update_loc_vol(ingrName+"_initial",volume)
                #add instruction to transfer ingr from initial location to current location
                self.add_transfer_group([ingrName+"_initial"],[locName],[volume])

        else:
            #existing ingredient
            #if adding to unspecified location, set location to ingredient's initial pool
            if not locName:
                locName = ingrName+"_initial"
            if locName in self.locations and locName != ingrName+"_initial":
                #if existing ingredient to existing location
                #assume ingredient is coming from ingredient's initial pool
                self.update_loc_vol(ingrName+"_initial",volume)
                self.update_ingr_vol(ingrName,ingrName+"_initial",volume)
                #add instruction to transfer ingr from initial location to current location
                self.add_transfer_group([ingrName+"_initial"],[locName],[volume])
            else:
                #if existing ingredient to new location or to initial pool
                #update location volume
                self.update_loc_vol(locName,volume)
                self.update_ingr_vol(ingrName,locName,volume)
        return "Added "+str(volume)+"uL of "+ingrName+" to "+locName

#    def fill_container(ingrName,source,containerName,volume,n,locations,groupName):
#        """fill n locations in a container, going by default in alpha-num order
#        e.g. A1,B1,C1....A2,B2,C2....A12,B12,C12
#
#        optionally specify list of locations in container
#
#        specify source as locName in self.locations, or None to pull from ingr pool 
#        """
#        # if unspecified source and new ingredient no
#        for i in range(0,n):
#            locName =        


    def add_transfer_group(self,fromLocs,toLocs,volumes,changeSettings=None):
        # add transfer group to instructions list
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
            transferDict=self.fill_instruction_defaults(transferDict,self.transfer_defaults)
            # if container and location are already specified, add
            transferDict["from"]["container"]=fromLocs[i].get("container")
            transferDict["from"]["location"]=fromLocs[i].get("location")
            transferDict["to"]["container"]=toLocs[i].get("container")
            transferDict["to"]["location"]=toLocs[i].get("location")
            # add to list of transfers in this group (same tip)
            transferGroup.append(transferDict)
            # update locations dict
            self.update_loc_vol(fromLocs[i],-volumes[i])
            self.update_loc_vol(toLocs[i],volumes[i])
        # assign pipette and format group
        formattedTransfer = self.assign_pipette("transfer",transferGroup)
        # add to instructions
        self.instructions.append(formattedTransfer)

    def add_mix_group(self,mixLocs,volumes,changeSettings=None):
        # add mix group to instructions list
        mixGroup = []
        for i in range(0,len(mixLocs)):
            mixDict={
                "locName":mixLocs[i],
                "volume":volumes[i]
            }
            if changeSettings:
                for key,value in changeSettings[i].items():
                    mixDict[key]=value
            #fill in missing fields with defaults
            mixDict=self.fill_instruction_defaults(mixDict,self.mix_defaults)
            #if container and location are already specified, add
            mixDict["container"]=mixLocs[i].get("container")
            mixDict["location"]=mixLocs[i].get("location")
            #add to list of mixes in this group (same tip)
            mixGroup.append(mixDict)
        # assign pipette and format group
        formattedMix = self.assign_pipette("mix",mixGroup)
        # add to instructions
        self.instructions.append(formattedMix)

    def update_loc_vol(self,locName,addVol):
        #if adding to a new location
        if locName not in self.locations:
            self.locations[locName]={"volume":addVol,"maxVol":addVol}
        #if updating existing location
        else:
            #sanity check to make sure volume does not go negative
            if self.locations[locName]["volume"]+addVol<0:
                raise InvalidEntry("Error: attempt to create negative volume at {0}".format(locName))
                return
            self.locations[locName]["volume"]+=addVol
            if self.locations[locName]["volume"]>self.locations[locName]["maxVol"]:
                self.locations[locName]["maxVol"]=self.locations[locName]["volume"]


    def update_ingr_vol(self,ingrName,locName,addVol):
        self.ingredients[ingrName][locName]=self.ingredients[ingrName].setdefault(locName,0)+addVol

    def assign_pipette(self,command,group):
        """assign correct pipette for instruction based on volume
        and return updated instruction group
        """
        # TO DO: add edit capabilities for head
        prevVolume = None
        prevPipette = None
        volume = None
        pipette = None
        for i in range(0,len(group)):
            instDict = group[i]
            volume = instDict["volume"]
            if volume >= 20 and volume <= 200:
                pipette = 'p200'
            elif volume <= 10:
                pipette = 'p10'
            elif volume > 10 and volume < 20:
                # split volume group up into two p10 movements
                volume = volume/2
                instDict["volume"]=volume
                copyDict = instDict
                # insert copy behind current index
                group.insert(i,copyDict)
                pipette = 'p10'
            elif volume > 200:
                # split volume group up into multiple p200 movements
                div = (volume//200)+1
                volume = volume/div
                instDict["volume"]=volume
                copyDict = instDict
                for i in range(0,div):
                    #insert copies behind current index
                    group.insert(i,copyDict)
                pipette = 'p200'
            if prevPipette and (pipette != prevPipette):
                raise InvalidEntry('Volume {0} does not match rest of group'.format(volume))
            prevPipette = pipette
        formattedGroup = {
            "tool": pipette,
            "groups": [
                {command: group}
            ]
        }
        return formattedGroup
            
    def assign_container(self,locName,containerName,containerLoc):
        """assign a container and container location to a named location
        e.g. OrangeG_initial --> tubes-2mL, A1
        """
        # add container and location to locations dict for future edit
        if locName not in self.locations:
            raise InvalidEntry("Attempted to assign container to nonexistent location")
        self.locations[locName].setdefault("container",containerName)
        self.locations[locName].setdefault("location",containerLoc)
        # find all occurences of locName in instructions
        for i in range(0,len(self.instructions)):
            if self.instructions[i].get("tool") in self.head:
                for j in range(0,len(self.instructions[i]["groups"])):
                    for k,v, in self.instructions[i]["groups"][j].items():
                        for k in range(0,len(v)):
                            if "from" in v:
                                if v[k]["from"].get("locName")==locName:
                                    v[k]["from"]["container"]=containerName
                                    v[k]["from"]["location"]=containerLoc
                                if v[k]["to"].get("locName")==locName:
                                    v[k]["to"]["container"]=containerName
                                    v[k]["to"]["location"]=locationName
                            else:
                                if v[k].get("locName")==locName:
                                    v[k]["container"]=containerName
                                    v[k]["location"]=containerLoc
        # find locName in ingredients
        for ing,locs in self.ingredients.items():
            for loc,vol in locs.items():
                if loc == locName:
                    # add to ingredients_export dict
                    self.ingredients_export.setdefault(ing,[]).append({
                            "container" : containerName,
                            "location" : containerLoc,
                            "volume" : vol
                        })



    def fill_instruction_defaults(self,instDict,instDefaults):
        """go through transfer,mix,cycler etc. defaults and fill in any
        missing fields
        """
        for key,value in instDefaults.items():
            if key=="from" or key=="to":
                for nextkey,nextvalue in value.items():
                    instDict[key].setdefault(nextkey,nextvalue)
            else:
                instDict.setdefault(key,value)
        return instDict

    def add_cycler_prog(self,progName,holdTemp=None,runtime=None):
        """add new cycler program to the cycler section in the protocol
        optionally specify hold temp at end of program and runtime
        """
        newProg={'hold':holdTemp, 'runtime':runtime}
        #fill defaults
        self.fill_instruction_defaults(newProg,self.cycler_defaults)
        #add to cycler dict
        self.cycler[progName]=newProg

    def add_cycler_group(self,progName,changeSettings=None):
        """add cycler group to instructions list
        progName = [] list of programs to run in group (usually single)
        
        optionally specify changes to default cycler settings with 
        changeSettings={change_key1:val1,change_key2:val2...}
        
        to add just a hold/incubate step, set progName as None and
        specify a holding temp in changeSettings
        """
        newGroup = {
            "tool": "cycler",
            "groups": []
        }
        for i in range(0,len(progName)):
            if (progName[i]) and (progName[i] not in self.cycler):
                raise InvalidEntry("Error: program not found")
                return
            newGroup["groups"].append({"run":{"name":progName[i]}})
            if changeSettings:
                for key,value in changeSettings[i].items():
                    newGroup["groups"][i]["run"].setdefault(key,value)
        self.instructions.append(newGroup)

#    def suggest_containers(self):
#        """ suggest optimum container for unspecified locations 
#        based on volume
#        """
#        for locName in self.locations:
#            if not locName["container"]:



    def export_to_JSON(self,fname):
        """ aggregate all sections into one dict and export to JSON
        """
        final_dict = {
            "info": self.info,
            "deck": self.deck,
            "head": self.head,
            "cycler": self.cycler,
            "ingredients": self.ingredients_export,
            "instructions": self.instructions
        }
        try:
            out_file=open(fname,"w")
            json.dump(final_dict,out_file,indent=4);
            print("Exported protocol to JSON")
        except EnvironmentError as err:
            print("Error exporting protocol to JSON")
            raise
        finally:
            if out_file is not None:
                out_file.close()
            
        

class InvalidEntry(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)

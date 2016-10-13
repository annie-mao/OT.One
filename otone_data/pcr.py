from openpyxl import load_workbook
from openpyxl.styles import colors
from baseProtocol import BaseProtocol, InvalidEntry
from collections import OrderedDict
from pprint import PrettyPrinter

class PCR:
    def __init__(self, name, description, notes):
        self.name = name
        self.description = description
        self.notes = notes
        self.copies = 1
        self.groups = []
        self.cyclerPtr = 0
        self.cyclerPrograms = ["PFUNKEL1","PFUNKEL2","PFUNKEL3"]
        self.excel = {
            'sheet_name': 'Combinatorial (no delay)',
            'start_row': 20,
            'reagent': {'key': 'D4', 'scan': 'D', 'name': 'A'},
            'cycler': {'key': 'D5', 'scan': 'B'},
            'aliquot': {'key': 'D6', 'scan': 'D'},
            'unshared' : ['Primary oligos (uM)',' secondary oligo  (uM)',\
                        'ssDNA (ng/uL)']
        } 
        self.mix_settings = {
            "repetitions": 5,
            "blowout": True,
            "liquid-tracking": False
        }
        self.cycler_settings = {
            "control": "CALC",
            "heated-lid": False,
            "vessel": "Tubes",
            "volume": 100
        }
        self.oil_transfer_settings = {
            "extra-pull": True,
            "to": {
                "tip-offset": 5,
                "touch-tip": False
            }
        }
        self.after_oil_transfer_settings = {
            "to": {
                "tip-offset": -10,
                "touch-tip": False
            }
        }
        self.after_oil_mix_settings = {
            "tip-offset": -10
        }
        self.mixVol = 10
        self.oilVol = 60
        self.aliquotRow = "A"
        self.aliquotVol = 5
        self.aliquotTotalVol = 20
        self.aliquotNum = 1
        self.useOil = True
        self.addedOil = False
        self.loadDye = True
        self.holdTemp = 4
        self.cyclerContainer = "2-8-tube-strip"
        self.iceContainer = "96-PCR-tubes"
        self.row = "A"
        self.printer = PrettyPrinter(indent = 2)

    def duplicate(self,copies):
        self.copies = copies
#        i = 0
#        while i < len(self.groups):
#            if self.groups[i]["type"] == 'reagent' or \
#                    self.groups[i]["type"] == 'aliquot':
#                for j in range(0,copies):
#                    # copy reagent and aliquot groups and insert 
#                    # right after, but do not copy cycler groups
#                    self.groups.insert(i+1,self.groups[i])
#                    # increment past newly copied group
#                    i = i + 2
#            else:
#                # if cycler, don't copy and increment to next group
#                i = i + 1
        

    def set_shared_reagents(self,reagents):
        """input list of reagents to set as shared
        """
        reagents = BaseProtocol.listify(reagents)
        for reagent in reagents:
            self.excel['shared'].append(reagent)

    def import_from_excel(self,filename):
        wb = load_workbook(filename, data_only = True)
        ws = wb[self.excel['sheet_name']]
        self.excel['reagent']['color'] = \
            ws[self.excel['reagent']['key']].fill.start_color.index
        self.excel['cycler']['color'] = \
            ws[self.excel['cycler']['key']].fill.start_color.index
        self.excel['aliquot']['color'] = \
            ws[self.excel['aliquot']['key']].fill.start_color.index
        row = self.excel['start_row']
        
        # scan down sheet and look for color-coded reagent, cycler,
        # and aliquot groups
        while (row < ws.max_row):
            rCell = self.excel['reagent']['scan'] + str(row)
            cCell = self.excel['cycler']['scan'] + str(row)
            aCell = self.excel['aliquot']['scan'] + str(row)
            rColor = ws[rCell].fill.start_color.index
            cColor = ws[cCell].fill.start_color.index
            aColor = ws[aCell].fill.start_color.index
            if (rColor == self.excel['reagent']['color']):
                row = self.load_reagent_group(ws,row)
            elif (cColor == self.excel['cycler']['color']):
                row = self.load_cycler_group(ws,row)
            elif (aColor == self.excel['aliquot']['color']):
                row = self.load_aliquot_group(ws,row)
            else:
                row = row + 1

    
    def load_reagent_group(self,ws,row):
        """ loads a group of reagents from excel sheet
        returns the next row after the group
        """
        scanCell = self.excel['reagent']['scan'] + str(row)
        nameCell = self.excel['reagent']['name'] + str(row)
        while ws[scanCell].fill.start_color.index ==\
                            self.excel['reagent']['color']:
            # get reagent name from nameCell
            name = ws[nameCell].value
            reagentGroup = {
                "type": "reagent",
                "name": name,
                # get reagent volume from scanCell
                "volume": ws[scanCell].value,
                # look for reagent in the set of shared reagents
                "shared": (name not in self.excel["unshared"])
            }
            # add reagent group to self.groups
            self.groups.append(reagentGroup)
            # increment to next row
            row = row + 1
            scanCell = self.excel['reagent']['scan'] + str(row)
            nameCell = self.excel['reagent']['name'] + str(row) 
        return row 

    def load_cycler_group(self,ws,row):
        """ loads a cycler instruction group from excel sheet
        right now just picks from a list of predefined cycler
        program names. Can be extended to create custom cycler
        programs based on the temperature steps and durations.
        """
        scanCell = self.excel['cycler']['scan'] + str(row)
        loadGroup = True
        while ws[scanCell].fill.start_color.index ==\
                            self.excel['cycler']['color']:
            if loadGroup:
                name = self.cyclerPrograms[self.cyclerPtr] 
                cyclerGroup = {
                    "type": "cycler",
                    "name": name
                }
                # add cycler group to self.groups
                self.groups.append(cyclerGroup)
                # don't load a new group in the next iteration of while
                loadGroup = False
                # increment cycler pointer
                self.cyclerPtr=(self.cyclerPtr+1)%len(self.cyclerPrograms)
            # increment to next row
            row = row + 1
            scanCell = self.excel['cycler']['scan'] + str(row)
        return row 


    def load_aliquot_group(self,ws,row):
        """ loads an aliquot instruction group from excel sheets
        """
        scanCell = self.excel['aliquot']['scan'] + str(row)
        while ws[scanCell].fill.start_color.index ==\
                                self.excel['aliquot']['color']:
            aliquotGroup = {
                "type": "aliquot",
                # get aliquot volume from scanCell
                "volume": ws[scanCell].value,
            }
            # add aliquot group to self.groups
            self.groups.append(aliquotGroup)
            # increment to next row
            row = row + 1
            scanCell = self.excel['aliquot']['scan'] + str(row)
        return row

    def convert_to_protocol(self):
        """ convert to a baseProtocol class
        """
        # instantiate protocol
        self.p = BaseProtocol(self.name,self.description,self.notes)
        # assign cycler and ice containers
        self.p.assign_labware("ice",self.iceContainer)
        self.p.assign_labware("cycler",self.cyclerContainer)
        # add cycler programs to protocol library
        for prog in self.cyclerPrograms:
            self.p.add_cycler_prog(prog,self.holdTemp)
        # create a reaction tube for each copy of the protocol
        rxnTubes = []
        for i in range(0,self.copies):
            rxnTubes.append("rxn_"+str(i+1))
        # preload reagents
        self.add_reagents_to_protocol(rxnTubes)
        # add instructions to protocol
        self.add_instructions_to_protocol(rxnTubes)

    def add_instructions_to_protocol(self,rxnTubes):
        # loop through instruction groups and add to protocol
        for group in self.groups:
            if group["type"] == "reagent" and group["shared"]:
                self.convert_shared_reagent_group(group,rxnTubes)
            elif group["type"] == "reagent" and not group["shared"]:
                self.convert_reagent_group(group,rxnTubes)
            elif group["type"] == "aliquot":
                self.convert_aliquot_group(group,rxnTubes)
            elif group["type"] == "cycler":
                self.convert_cycler_group(group,rxnTubes)
        self.cleanup(rxnTubes)

    def cleanup(self,rxnTubes):
        for i in range(0,len(rxnTubes)):
            location = self.next_empty_location("cycler")
            self.p.assign_container(rxnTubes[i],"cycler",location)

    def add_reagents_to_protocol(self,rxnTubes):
        """ Pre-load all reagents into protocol for accurate volume
        calculations
        """
        for group in self.groups:
            if group["type"] == "reagent" and group["shared"]:
                self.add_shared_reagent(group,rxnTubes)
            elif group["type"] == "reagent" and not group["shared"]:
                self.add_reagent(group,rxnTubes)
    

    def add_shared_reagent(self,group,rxnTubes):
        """ add a shared reagent to baseProtocol ingredients dictionary
        """
        name = group["name"]
        volume = group["volume"]
        for i in range(0,len(rxnTubes)):  
            # add ingredient to protocol
            self.p.add_ingredient(name,name,volume)


    def add_reagent(self,group,rxnTubes):
        """ add a reagent to baseProtocol ingredients dictionary
        """
        volume = group["volume"]
        container = "ice"
        for i in range(0,len(rxnTubes)): 
            name = group["name"] + str(i+1)
            row = chr(ord(self.row))
            col = str(i+1)
            # add ingredient to protocol 
            self.p.add_ingredient(name,name,group["volume"])
            # assign container
            self.p.assign_container(name,container,row+col)
        # increment column for next round of rxn-specific reagents
        self.row = chr(ord(self.row) + 1)


    def convert_shared_reagent_group(self,group,rxnTubes):
        """ convert a reagent group to baseProtocol transfer instructions
        when the reagent is being shared among all rxns
        """
        name = group["name"]
        volume = group["volume"]
        for i in range(0,len(rxnTubes)):  
            # transfer ingredient to rxn tube
            self.p.add_transfer_group(name,rxnTubes[i],volume)


    def convert_reagent_group(self,group,rxnTubes):
        """ convert a reagent group to baseProtocol transfer instructions
        """
        volume = group["volume"]
        for i in range(0,len(rxnTubes)): 
            name = group["name"] + str(i+1)
            # transfer ingredient to rxn tube
            self.p.add_transfer_group(name,rxnTubes[i],group["volume"])

    def add_aliquot_to_protocol(self,rxnTubes):
        """ pre-load aliquot reagents to protocol
        """


    def convert_aliquot_group(self,group,rxnTubes):
        """ convert an aliquot group to baseProtocol instructions
        """
        for i in range(0,len(rxnTubes)):
            name = "aliquot_{0}_{1}".format(str(i+1),self.aliquotNum)
            volume = group["volume"]
            self.p.add_transfer_group(rxnTubes[i],name,volume)
            # load dye for gel electrophoresis
            if self.loadDye:
                self.load_dye(name,volume)
            # assign aliquot to ice container
            row = chr(ord(self.aliquotRow) + len(self.excel["unshared"]))
            col = str(i+1)
            self.p.assign_container(name,"ice",row+col)
        # increment column and # of aliquots for next round
        self.aliquotRow = chr(ord(self.aliquotRow) + 1)
        self.aliquotNum = self.aliquotNum + 1

    def load_dye(self, aliquotName, aliquotVol):
        """ load dye for running aliquot gels
        """
        # calculate dye dilution
        dyeVol = self.aliquotTotalVol/6
        waterVol = self.aliquotTotalVol - dyeVol - aliquotVol
        # add dye and water to ingredients
        self.p.add_ingredient("dye","dye",dyeVol)
        self.p.add_ingredient("DI-NF water","DI-NF water",waterVol)
        # transfer dye and water to aliquot, mix at end
        self.p.add_transfer_group("dye",aliquotName,dyeVol)
        self.p.add_transfer_with_mix("DI-NF water",aliquotName,waterVol)


    def convert_cycler_group(self,group,rxnTubes):
        """ convert a cycler group to baseProtocol instructions
        """
        # mix rxn tubes
        for rxn in rxnTubes: 
            self.p.add_mix_group(rxn,self.mixVol)
        # add PCR oil if necessary
        if self.useOil and not self.addedOil:
            self.add_oil(rxnTubes)
        # add cycler instruction to protocol
        self.p.add_cycler_group(group["name"])

    def add_oil(self,rxnTubes):
        """ add oil to PCR tubes before running a cycler program
        to prevent evaporation
        """
        # change default transfer settings for oil settings
        for key, value in self.oil_transfer_settings.items():
            self.p.configure_transfer(key,value)
        # add oil to the top of each rxn tube
        for rxn in rxnTubes:
            self.p.add_ingredient("oil","oil",self.oilVol)
            self.p.add_transfer_group("oil",rxn,self.oilVol)
        # change default settings for subsequent instructions
        for key,value in self.after_oil_transfer_settings.items():
            self.p.configure_transfer(key,value)
        for key,value in self.after_oil_mix_settings.items():
            self.p.configure_mix(key,value)
        # only add oil once to rxn tubes
        self.addedOil = True

    def next_empty_location(self,containerName):
        """ return the next empty location in a container
        e.g. A5
        """
        return self.p.deck[containerName]["empty"][0]


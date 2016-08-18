from baseProtocol import BaseProtocol, InvalidEntry
import sys
import pprint

pp = pprint.PrettyPrinter(indent=2)

""" Uses the baseProtocol class in a basic command line UI
"""

class ProtocolUI:
    
    def __init__(self):
        self.protocol = None
    
    def welcome(self):
        userIn = input("--------------------------------------------\n\
        Welcome to the OT.One Protocol Editor.\n\
        Create a new protocol: 'N' \n\
        Edit existing protoco: 'E' \n\
        Quit: 'Q' \n\n\
        Please enter your choice: ")
        if userIn == 'N': 
            self.new_protocol()
        elif userIn == 'E':
            pass
        elif userIn == 'Q':
            sys.exit()
        else:
            raise InvalidEntry('Invalid input. Please try again')

    def new_protocol(self):
        print("--------------------------------------------")
        name = input("Protocol name: ")
        desc = input("Protocol description: ")
        notes = input("Protocol notes: ")
        self.protocol = BaseProtocol(name,desc,notes)
        self.protocol_menu()

    def protocol_menu(self):
        inProgress = True
        while inProgress:
            print("--------------------------------------------")
            userIn =  input("\tAdd ingredient: 'I'\
            \n\tAdd pipette group: 'G'\
            \n\tAdd cycler program: 'P'\
            \n\tAdd cycler instruction: 'C'\
            \n\tAssign locations: 'A'\
            \n\tExport to JSON: 'J'\
            \n\tView: 'V'\
            \n\tQuit: 'Q'\n\
            \n\tPlease enter your choice: ")
            if userIn == 'I':
                self.ingredient()
            elif userIn == 'P':
                self.cycler_program()
            elif userIn == 'C':
                self.cycler_instruction()
            elif userIn == 'G':
                self.instruction_stream_cmdline()
            elif userIn == 'A':
                self.assign_locations()
            elif userIn == 'J':
                self.export()
            elif userIn == 'V':
                self.view()
            elif userIn == 'Q':
                if self.y_n_prompt("Save protocol?"):
                    self.export()
                inProgress = False
            else:
                raise InvalidEntry('Invalid input. Please try again')


    def ingredient(self):
        print("--------------------------------------------")
        print("Add ingredients to the protocol. If the location is not\
        \nspecified, an initial location will be created for it, and all\
        \nunspecified volumes of the same ingredient will be added there.\
        \nIf adding an existing ingredient to an existing location, it\
        \nwill first be added to its initial pool, and a transfer instruction\
        \nwill be added from the pool to the target location.")
        print("--------------------------------------------")
        ingrName = input("Ingredient name: ")
        locName = None
        volume = float(input("Ingredient volume (uL): "))
        containerName = None
        containerLoc = None
        if self.y_n_prompt("Specify location?"):
            locName = input("Location name: ")
        if self.y_n_prompt("Specify container now?"):
            containerName = input("Container name: ")
            containerLoc = input("Location in container (e.g. A1): ")
        print('\n'+self.protocol.add_ingredient(ingrName,locName,volume,containerName,containerLoc))
        if containerName and (containerName in self.protocol.list_unassigned_containers()):
            print("--------------------------------------------")
            if self.y_n_prompt("Assign labware to {0} now?".format(containerName)):
                while True:
                    try:
                        labware = input("Labware: ")
                        self.protocol.assign_labware(containerName,labware)
                        break
                    except InvalidEntry as e:
                        print(e)


    def cycler_program(self):
        print("--------------------------------------------")
        print("Add to the available cycler programs for this protocol")
        print("--------------------------------------------")
        progName = input("Program name: ")
        holdTemp = None
        if self.y_n_prompt("Add temperature hold at end of program?"):
            holdTemp = float(input("Temperature: "))
        self.protocol.add_cycler_prog(progName,holdTemp)


    def cycler_instruction(self):
        print("--------------------------------------------")
        print("Add a cycler program to the protocol instructons")
        print("--------------------------------------------")
        progName = input("Program name: ")
        changeSettings = self.change_settings('C')
        self.protocol.add_cycler_group(progName,changeSettings)


    def assign_locations(self):
        print("--------------------------------------------")
        print("Unassigned locations:")
        for loc in self.protocol.list_unassigned_locations():
            while True:
                try:
                    print(loc)
                    if self.y_n_prompt("Assign?"):
                        containerName = input("Container: ")
                        containerLoc = input("Container Location (e.g. A1): ")
                        self.protocol.assign_container(loc,containerName,containerLoc)
                        break
                    else:
                        break
                except InvalidEntry as e:
                    print(e)

    def assign_containers(self):
        print("--------------------------------------------")
        print("Unassigned containers:")
        for cont in self.protocol.list_unassigned_containers():
            while True:
                try:
                    print(cont)
                    if self.y_n_prompt("Assign?"):
                        labware = input("Labware: ")
                        self.protocol.assign_labware(cont,labware)
                        break
                    else:
                        break
                except InvalidEntry as e:
                    print(e)


    def export(self):
        if self.protocol.list_unassigned_locations():
            self.assign_locations()
        if self.protocol.list_unassigned_containers():
            self.assign_containers()
        print("--------------------------------------------")
        fname = input("Save as: ")
        self.protocol.export_to_JSON(fname)
        
    
    def view(self):
        inProgress = True
        while inProgress: 
            print("--------------------------------------------")
            userIn = input("\tView:\
            \n\tInfo (F)\
            \n\tHead (H)\
            \n\tDeck (D)\
            \n\tIngredients (I)\
            \n\tLocations (L)\
            \n\tInstructions (N)\
            \n\tCycler Programs (C)\
            \n\tQuit (Q)\n\
            \n\tPlease enter your choice: ")
            print("--------------------------------------------")
            if userIn == 'F':
                print('*** INFO ***\n')
                pp.pprint(self.protocol.info)
            if userIn == 'H':
                print('*** HEAD ***\n')
                pp.pprint(self.protocol.head)
            elif userIn == 'D':
                print('*** DECK ***\n')
                pp.pprint(self.protocol.deck)
            elif userIn == 'I':
                print('*** INGREDIENTS ***\n')
                pp.pprint(self.protocol.ingredients)
            elif userIn == 'L':
                print('*** LOCATIONS ***\n')
                pp.pprint(self.protocol.locations)
            elif userIn == 'N':
                print('*** INSTRUCTIONS ***\n')
                pp.pprint(self.protocol.instructions)
            elif userIn == 'C':
                print('*** CYCLER PROGRAMS ***\n')
                pp.pprint(self.protocol.cycler)
            elif userIn == 'Q':
                inProgress = False


    def instruction_stream_cmdline(self):
        """ begin a new instruction
        can append any combination of transfers, mixes, as long as all
        volumes belong to the same pipette range
        """
        # get pipette type 
        print("--------------------------------------------")
        print("All movements in this instruction group will share a pipette tip.\
        \nAny combination of pipette commands can be added, as long as they are\
        \nin the same volume range.") 
        print("--------------------------------------------")
        pipette = input("Select a pipette:\n\tp200 (20-200uL)\n\tp10(0.5-10uL)\n\t")
        inProgress = True
        while inProgress:
            try: 
                print("--------------------------------------------")
                cmd = input("Select a command:\n\tTransfer (T)\n\tMix(M)\n\tTransfer+Mix (X)\n\tEnd (E)\n\t")
                # get parameters
                if cmd == 'T':
                    changeSettings = self.change_settings(cmd)
                    fromLocs = input('From (location1,location2,location3...):  ').split(',')
                    toLocs = input('To (location2,location2,location3...):  ').split(',')
                    volumes = input('Transfer volumes (vol1,vol2,vol3...):  ').split(',')
                    for i in range(0,len(volumes)): volumes[i] = float(volumes[i])
                    self.protocol.add_transfer_to_stream(fromLocs,toLocs,volumes,changeSettings)
                elif cmd == 'M':
                    changeSettings = self.change_settings(cmd)
                    mixLocs = input('Mix (location1,location2,location3...):  ').split(',')
                    volumes = input('Mix volumes (vol1,vol2,vol3...):  ').split(',')
                    for i in range(0,len(volumes)): volumes[i] = float(volumes[i])
                    self.protocol.add_mix_to_stream(mixLocs,volumes,changeSettings)
                elif cmd == 'X':
                    tr_changeSettings = self.change_settings('T')
                    mix_changeSettings = self.change_settings('M')
                    fromLocs = input('From (location1,location2,location3...):  ').split(',')
                    toLocs = input('To (location2,location2,location3...):  ').split(',')
                    volumes = input('Transfer volumes (vol1,vol2,vol3...):  ').split(',')
                    for i in range(0,len(volumes)): volumes[i] = float(volumes[i])
                    
                    print(fromLocs)
                    print(toLocs)
                    print(volumes)
                    self.protocol.transfer_with_mix(fromLocs,toLocs,volumes,tr_changeSettings,mix_changeSettings)
                # check for exit
                elif cmd == 'E':
                    print('The current instruction group:')
                    pp.pprint(self.protocol.instruction_stream)
                    if self.y_n_prompt("Finish and add this group to protocol?"):
                        self.protocol.end_stream()
                        inProgress = False
                    elif self.y_n_prompt("Discard group?"):
                        self.protocol.clear_stream()
                        inProgress = False
                    else:
                        print('Continue editing group')
            #except(SyntaxError,NameError,IndexError):
            #        print("Invalid input. Please try again")
            except InvalidEntry as e:
                    print("***Error:" + e.value)


    def y_n_prompt(self,question):
        while True:
            yn = input(question + ' (Y/N): ')
            if yn == 'Y':
                return True
            if yn == 'N':
                return False
            else:
                print('Please enter Y or N')


    def change_settings(self,cmd):
        str = ''
        if cmd == 'T':
            str = 'transfer'
        elif cmd == 'M':
            str = 'mix'
        elif cmd == 'C':
            str = 'cycler'
        if self.y_n_prompt("Configure {0} settings?".format(str)):
            print("--------------------------------------------")
            if cmd == 'T':
                print("Transfer defaults:")
                pp.pprint(self.protocol.transfer_defaults)
            elif cmd == 'M':
                print("Mix defaults:")
                pp.pprint(self.protocol.mix_defaults)
            elif cmd == 'C':
                print("Cycler defaults:")
                pp.pprint(self.protocol.cycler_defaults)
            inProgress = True
            settingDict = {}
            while inProgress:
                try:
                    print("--------------------------------------------")
                    print("Input changes or Q to quit")
                    userIn = input("Setting to change (setting,val,(to/from)): ").split(',')
                    if userIn[0] == 'Q':
                        print("--------------------------------------------")
                        print("Changed settings:\n")
                        pp.pprint(settingDict)
                        print("--------------------------------------------") 
                        return settingDict
                    if len(userIn)>2:
                        if userIn[2] == 'to' or userIn[2] == 'from':
                            settingDict.setdefault(userIn[2],{}).\
                            setdefault(self.str2type(userIn[0]),self.str2type(userIn[1]))
                        else:
                            print('***Error: Use format setting,val,(to/from)')
                    else:
                        settingDict[self.str2type(userIn[0])] = self.str2type(userIn[1])
                except (SyntaxError,NameError,IndexError,KeyError) as e:
                    print(e)
        else:
            return {}


    def str2type(self,val):
        """parse string inputs and return numbers as numbers, bools as bools,
        strings as strings
        """
        # check for num
        if self.is_num(val):
            return float(val)
        elif val == 'False':
            return False
        elif val == 'True':
            return True
        else:
            return val

    def is_num(self,val):
        try:
            float(val)
            return True
        except ValueError:
            return False

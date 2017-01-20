from pcr import PCR
print("----------------------------------------------")
name = input("\tProtocol name: ")
desc = input("\tDescription: ")
notes = input("\tNotes: ")
fname = input("\tName of excel file to convert (*.xlsx): ")
protocol = PCR(name, desc, notes)

while True:
    try:
        useMM1and2 = input("----------------------------------------------\n\
        Use Mastermixes 1 and 2 (M)\n\
        Proceed to first cycler step (C)\n\n\
        Please enter your choice: ")
        if useMM1and2 == "C":
            protocol.rxnVol = int(input("\tReaction volume (uL): "))
            protocol.useMM1and2 = False
            break
        elif useMM1and2 == "M":
            protocol.useMM1and2 = True
            break
        else:
            print("\tInvalid input. Please try again")
    except NameError:
        print("\tInvalid input. Please try again")

protocol.import_from_excel(fname)
duplicates = int(input("\tHow many reactions? (max. 11): "))
protocol.duplicate(duplicates)
protocol.convert_to_protocol()
jsonname = input("\tJSON file name (*.json): ")
print("----------------------------------------------")
protocol.export_to_JSON(jsonname)

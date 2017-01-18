from pcr import PCR

name = input("Protocol name: ")
desc = input("Description: ")
notes = input("Notes: ")
fname = input("Name of excel file to convert (*.xlsx): ")
protocol = PCR(name, desc, notes)
protocol.import_from_excel(fname)
duplicates = int(input("How many reactions?: "))
protocol.duplicate(duplicates)
protocol.convert_to_protocol()
jsonname = input("JSON file name: ")
protocol.export_to_JSON(jsonname)

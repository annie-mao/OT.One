# Generates a JSON protocol for Accuracy/Precision volume transfer
# calibration on the OT.One

from baseProtocol import BaseProtocol, InvalidEntry, Prompt
import pprint

pp = pprint.PrettyPrinter(indent=2)
p = BaseProtocol("AnP","Test AnP of OT.One using p10 and p200 pipettes","1/23/17")
p.set_container_library("containers.json")

# ingredients
OrangeG10 = "OrangeG_1:10"
OrangeG100 = "OrangeG_1:100"
OrangeG200 = "OrangeG_1:200"
OrangeG40 = "OrangeG_1:40"
OrangeG400 = "OrangeG_1:400"
OrangeG400_1 = "OrangeG_1:400_1"
OrangeG400_2 = "OrangeG_1:400_2"
PBS = "PBS"

# containers
plate = "plate"
WS = "working_solutions"

# dictionary to link each test well with its starting volume and WS
test_wells = []
for i in range(0,2):
    for j in range(0,6):
        well = chr(ord("A")+i)+str(j+1)
        test_wells.append({
            "well":well,
            "PBS":50,
            "WS":OrangeG400+"_"+str(i+1),
            "testVol":200})

for i in range(0,2):
    for j in range(0,6):
        well = chr(ord("C")+i)+str(j+1)
        test_wells.append({"well":well,"PBS":150,"WS":OrangeG200,"testVol":100})

for i in range(0,2):
    for j in range(0,6):
        well = chr(ord("E")+i)+str(j+1)
        test_wells.append({"well":well,"PBS":230,"WS":OrangeG40,"testVol":20})

for i in range(0,2):
    for j in range(6,12):
        well = chr(ord("A")+i)+str(j+1)
        test_wells.append({"well":well,"PBS":240,"WS":OrangeG200,"testVol":10})

for i in range(0,2):
    for j in range(6,12):
        well = chr(ord("C")+i)+str(j+1)
        test_wells.append({"well":well,"PBS":245,"WS":OrangeG100,"testVol":5})

for i in range(0,2):
    for j in range(6,12):
        well = chr(ord("E")+i)+str(j+1)
        test_wells.append({"well":well,"PBS":249.5,"WS":OrangeG10,"testVol":0.5})

# starting volumes of PBS
for well in test_wells:
    p.add_ingredient(well["well"],well["well"],well["PBS"])
    p.assign_container(well["well"],plate,well["well"])

p.assign_labware(plate,"96-PCR-flat")

# starting volumes of Working Solutions with a 10uL dead volume
p.add_ingredient(OrangeG10,OrangeG10,16)
p.add_ingredient(OrangeG100,OrangeG100,70)
p.add_ingredient(OrangeG200,OrangeG200,1330)
p.add_ingredient(OrangeG40,OrangeG40,250)
p.add_ingredient(OrangeG400_1,OrangeG400_1,1210)
p.add_ingredient(OrangeG400_2,OrangeG400_2,1210)

p.assign_container(OrangeG10,WS,"A1")
p.assign_container(OrangeG40,WS,"A2")
p.assign_container(OrangeG100,WS,"A3")
p.assign_container(OrangeG200,WS,"A4")
p.assign_container(OrangeG400_1,WS,"A5")
p.assign_container(OrangeG400_2,WS,"A6")

p.assign_labware(WS,"tube-rack-2ml")

# transfer groups
for well in test_wells:
    p.add_transfer_group(well["WS"],well["well"],well["testVol"])

pp.pprint(p.deck)
#pp.pprint(p.locations)
#pp.pprint(p.ingredients)
pp.pprint(p.ingredients_export)
print("-----------------------------")
print(p.list_unassigned_locations())
print(p.list_unassigned_containers())
print("-----------------------------")
pp.pprint(p.instructions)

p.export_to_JSON('AnP_test.json')

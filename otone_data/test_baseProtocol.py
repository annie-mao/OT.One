from baseProtocol import BaseProtocol, InvalidEntry, Override
import pprint

pp = pprint.PrettyPrinter(indent=2)
b = BaseProtocol("testprotocol","this is a test","note: testing")

'''
ingr = "OrangeG"
fromLocs = ["A1","A2","A3"]
toLocs = ["B1","B2","B3"]
volumes = ["200","100","20"]
changeSettings=[{},{"from":{"touch-tip":True}},{"blowout":False}]


transferGroup = b.make_transfer_group(ingr,fromLocs,toLocs,volumes,changeSettings)
pp.pprint(transferGroup)
'''

i1 = "Ingr_1"
i2 = "Ingr_2"
i3 = "Ingr_3"

l1 = "Loc_1"
l2 = "Loc_2"
l3 = "Loc_3"

c1 = "Container_1"

# new ingredient to unspecified location
print("-----------------------------")
print(b.add_ingredient(i1,None,100))
pp.pprint(b.locations) # check for "Ingr_1_initial" location
pp.pprint(b.ingredients) # check for added "Ingr_1: vol
# new ingredient to new location
print("-----------------------------")
print(b.add_ingredient(i2,l1,100))
pp.pprint(b.locations) # check l1 location
pp.pprint(b.ingredients) # check for added "Ingr_2: vol
# new ingredient to existing location
print("-----------------------------")
print(b.add_ingredient(i3,l1,100))
pp.pprint(b.locations) # check for new i3 initial pool and updated l1
pp.pprint(b.ingredients) # check for new i3
pp.pprint(b.instructions) # check for new transfer group
# existing ingredient to unspecified location
print("-----------------------------")
print(b.add_ingredient(i1,None,100))
pp.pprint(b.locations) # check for updated i1 initial pool
pp.pprint(b.ingredients) # check for updated i1 initial pool
# existing ingredient to initial pool
print("-----------------------------")
print(b.add_ingredient(i1,i1+"_initial",100))
pp.pprint(b.locations) # check for updated i1 initial pool
pp.pprint(b.ingredients) # check for updated i1 initial pool
# existing ingredient to existing location
print("-----------------------------")
print(b.add_ingredient(i1,l1,100))
pp.pprint(b.locations) # updated l1 and i1 initial
pp.pprint(b.ingredients) # updated l1 and i1 initial
pp.pprint(b.instructions) # check for i1 initial to l1 transfer group
# existing ingredient to existing location, specify container
print("-----------------------------")
print(b.add_ingredient(i1,l1,100,c1,'A1'))
pp.pprint(b.locations) # updated l1 and i1 initial
pp.pprint(b.ingredients) # updated l1 and i1 initial
pp.pprint(b.instructions) #check for container in all l1
pp.pprint(b.ingredients_export)
# try to specify container for a location which is already assigned
print("-----------------------------")
# should raise Override
try:
    b.assign_container(l1,c1,'A2')
except Override:
    print('override error')
# transfer without specifying location of already assoc. location
print("-----------------------------")
print(b.add_transfer_group([i1+'_initial'],[l1],[100]))
pp.pprint(b.locations)
pp.pprint(b.ingredients)
pp.pprint(b.instructions)
# transfer to new location and multiple transfers
print("-----------------------------")
print(b.add_transfer_group([l1,l1],[l2,l2],[100,100]))
pp.pprint(b.locations)
pp.pprint(b.ingredients)
pp.pprint(b.instructions)
# transfer large volume > 200, should split into multiple transfers
print("-----------------------------")
print(b.add_transfer_group([l1],[l2],[201]))
pp.pprint(b.locations)
pp.pprint(b.ingredients)
pp.pprint(b.instructions)
# transfer resulting in negative volume, should raise InvalidEntry
print("-----------------------------")
try:
    b.add_transfer_group([l1,l1],[l2,l2],[50,50])
except InvalidEntry as e:
    print(e.value)
# transfer in between 10ul and 20ul , should split into multiple p10s
print("-----------------------------")
print(b.add_transfer_group([l1],[l2],[10.1]))
pp.pprint(b.locations)
pp.pprint(b.ingredients)
pp.pprint(b.instructions)
# transfer with custom settings
print("-----------------------------")
print(b.add_transfer_group([l1,l2],[l2,l1],[10,10],[{'from':{'touch-tip':True},'to':{'touch-tip':False}},None]))
pp.pprint(b.locations)
pp.pprint(b.ingredients)
pp.pprint(b.instructions)
print("*****************************")
print(b.add_mix_group([l1],[100],[{"repetitions":10}]))
pp.pprint(b.locations)
pp.pprint(b.instructions)
pp.pprint(b.ingredients_export)
print("-----------------------------")
b.add_cycler_prog('PFUNKEL1',63.6)
b.add_cycler_group(['PFUNKEL1'])
pp.pprint(b.instructions)
pp.pprint(b.cycler)
# list unassigned locations
print("-----------------------------")
print(b.list_unassigned_locations())

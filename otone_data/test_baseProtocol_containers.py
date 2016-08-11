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

print(b.add_ingredient(i1,None,100))
print(b.add_ingredient(i2,l1,100))
print(b.add_ingredient(i3,l1,100))
print(b.add_ingredient(i1,None,100))
print(b.add_ingredient(i1,i1+"_initial",100))
print(b.add_ingredient(i1,l1,100))
print(b.add_ingredient(i1,l1,100,c1,'A1'))
print(b.add_transfer_group([i1+'_initial'],[l1],[100]))
print(b.add_transfer_group([l1,l1],[l2,l2],[100,100]))
print(b.add_transfer_group([l1],[l2],[201]))
print(b.add_mix_group([l1],[100],[{"repetitions":10}]))
b.add_cycler_prog('PFUNKEL1',63.6)
b.add_cycler_group(['PFUNKEL1'])
pp.pprint(b.locations)
pp.pprint(b.ingredients)
pp.pprint(b.ingredients_export)
print("-----------------------------")
print(b.list_unassigned_locations())
print("-----------------------------")
b.add_container_to_deck(c1,'96-PCR-flat')
pp.pprint(b.deck)

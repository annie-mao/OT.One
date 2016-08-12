from baseProtocol import BaseProtocol, InvalidEntry, Prompt
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
c2 = "Container_2"

print(b.add_ingredient(i1,None,100))
print(b.add_ingredient(i2,l1,100))
print(b.add_ingredient(i3,l1,100))
print(b.add_ingredient(i1,None,100))
print(b.add_ingredient(i1,i1+"_initial",100))
print(b.add_ingredient(i1,l1,100))
print(b.add_ingredient(i1,l1,100,c1,'A1'))
print(b.add_transfer_group([i1+'_initial'],[l1],[100]))
print(b.add_transfer_group([l1,l1,l1],[l2,l2,l2],[100,100,100]))
d1 = []
d2 = []
d1.append(b.transfer_dict(l1,l1,100))
d2.append(b.mix_dict(l1,100,{"repetitions":10}))
#print(d1)
#print(d2)
print('-----------')
inst = b.assign_pipette(["transfer","mix"],[d1,d2])
b.instructions.append(inst)
b.add_cycler_prog('PFUNKEL1',63.6)
b.add_cycler_group(['PFUNKEL1'])
pp.pprint(b.locations)
pp.pprint(b.ingredients)
pp.pprint(b.ingredients_export)
print("-----------------------------")
print(b.list_unassigned_locations())
print(b.list_unassigned_containers())
print("-----------------------------")
b.assign_labware(c1,'tube-rack-2ml')
b.assign_container(l1,c2,'A1')
pp.pprint(b.deck)
pp.pprint(b.locations)
pp.pprint(b.instructions)
b.new_instruction_stream()

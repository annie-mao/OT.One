from baseProtocol import BaseProtocol, InvalidEntry
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

ingr = "OrangeG"

print(b.add_ingredient(ingr,None,1000))
pp.pprint(b.locations)
print("-----------------------------")
pp.pprint(b.ingredients)
print("-----------------------------")
pp.pprint(b.instructions)
print("*****************************")
print(b.add_ingredient(ingr,None,100))
pp.pprint(b.locations)
print("-----------------------------")
pp.pprint(b.ingredients)
print("-----------------------------")
pp.pprint(b.instructions)
print("*****************************")
print(b.add_ingredient(ingr,"NewLoc",100))
pp.pprint(b.locations)
print("-----------------------------")
pp.pprint(b.ingredients)
print("-----------------------------")
pp.pprint(b.instructions)
print("*****************************")
print(b.add_ingredient(ingr,"NewLoc",100))
pp.pprint(b.locations)
print("-----------------------------")
pp.pprint(b.ingredients)
print("-----------------------------")
pp.pprint(b.instructions)
print("*****************************")
try:
    print(b.add_transfer_group([ingr+"_initial",ingr+"_initial",ingr+"_initial"],["NewLoc","NewLoc","NewLoc"],[20,30,40]))
except InvalidEntry as e:
    print('Error: {0}'.format(e.value))
pp.pprint(b.locations)
print("-----------------------------")
pp.pprint(b.ingredients)
print("-----------------------------")
pp.pprint(b.instructions)
print("*****************************")
print(b.add_mix_group(["NewLoc"],[100],[{"repetitions":6}]))
pp.pprint(b.locations)
print("-----------------------------")
pp.pprint(b.ingredients)
print("-----------------------------")
b.add_cycler_prog('PFUNKEL1',63.6)
b.add_cycler_group(['PFUNKEL1'])
pp.pprint(b.instructions)
print("*****************************")
b.assign_container("NewLoc","container1","A1")
print(b.ingredients_export)

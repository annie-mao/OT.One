from baseProtocol import BaseProtocol
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

print(b.add_ingredient(ingr,None,100))
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
print(b.add_transfer_group([ingr+"_initial"],["NewLoc"],[100]))
pp.pprint(b.locations)
print("-----------------------------")
pp.pprint(b.ingredients)
print("-----------------------------")
pp.pprint(b.instructions)
print("*****************************")

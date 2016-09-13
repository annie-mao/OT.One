from baseProtocol import BaseProtocol, InvalidEntry, Prompt
import pprint

pp = pprint.PrettyPrinter(indent=2)
pf = BaseProtocol("PFunkel","PFunkel Mutagenesis starting from master mix","note: testing")
pf.set_container_library("containers.json")

# ingredients
mm = 'master_mix'
water = 'water'
oligo1 = 'CDRH3-NNK'
ssDNA = 'ssDNA'
enzymes = 'polymerase_ligase_mix'
#polymerase = 'PfuTurbo_Cx_polymerase'
#ligase = 'Taq_ligase'
exo = 'exonuclease_mix'
#NEBuffer_1 = 'NEBuffer_1'
#Exo3 = 'Exonuclease_III'
#UDG = 'UDG'
#dil_Exo3 = 'diluted_Exonuclease_III'
#Exo1 = 'Exonuclease_I'
al1 = 'aliquot_1'
al2 = 'aliquot_2'
al3 = 'aliquot_3'
oligo2 = 'P23-Amp-rev'
c_tube = 'cycler_tube'
oil = 'oil'
dye = 'loading_dye'


# cycler
pf.add_cycler_prog('PFUNKEL1',4,2+60+15+10+2+15)
pf.add_cycler_prog('PFUNKEL2',4,80)
pf.add_cycler_prog('PFUNKEL3',4,47)
pf.add_cycler_prog('4')
pp.pprint(pf.cycler)

# containers
ice = 'ice'
cycler = 'cycler'

# prepare ingredients
pf.add_ingredient(mm,mm,22)
pf.add_ingredient(ssDNA,ssDNA,10)
pf.add_ingredient(enzymes,enzymes,10)

pf.add_ingredient(exo,exo,10)
#pf.add_ingredient(Exo1,Exo1,10)
#pf.add_ingredient(Exo3,Exo3,10)
#pf.add_ingredient(NEBuffer_1,NEBuffer_1,10)
#pf.add_ingredient(UDG,UDG,10)

pf.add_ingredient(oligo1,oligo1,10)
pf.add_ingredient(oligo2,oligo2,10)

pf.add_ingredient(water,water,200)
pf.add_ingredient(oil,oil,100)
pf.add_ingredient(dye,dye,50)
# assign containers to ingredients
pf.assign_container(mm,ice,'C4')
pf.assign_container(ssDNA,ice,'C5')
pf.assign_container(enzymes,ice,'C6')

pf.assign_container(exo,ice,'C7')
#pf.assign_container(Exo1,ice,'D4')
#pf.assign_container(Exo3,ice,'D5')
#pf.assign_container(NEBuffer_1,ice,'D6')
#pf.assign_container(UDG,ice,'D7')

pf.assign_container(oligo1,ice,'D4')
pf.assign_container(oligo2,ice,'D5')

pf.assign_container(water,ice,'E4')
pf.assign_container(oil,ice,'E5')
pf.assign_container(dye,ice,'E6')
pf.assign_labware(ice,'96-PCR-tubes')

# master mix
pf.add_transfer_group(water,mm,66.18,{'to':{'touch-tip':False}})
pf.add_transfer_group(oligo1,mm,1.47)
pf.add_transfer_group(ssDNA,mm,4.35)
pf.add_transfer_with_mix(enzymes,mm,6)

# exo III dilution
#pf.add_transfer_group(water,dil_Exo3,3.75)
#pf.add_transfer_group(NEBuffer_1,dil_Exo3,0.5)
#pf.add_transfer_with_mix(Exo3,dil_Exo3,0.75)

#pf.assign_container(dil_Exo3,ice,'D8')

# transfer to cycler
pf.add_transfer_group(mm,c_tube,100)
pf.add_transfer_group(oil,c_tube,50,{'extra-pull':True,'to':{'tip-offset':5,'touch-tip':False}})

pf.assign_container(c_tube,cycler,'A1')
pf.assign_labware(cycler,'8-tube-strip')

# first cycler instruction
pf.add_cycler_group('PFUNKEL1')

# aliquot 1
pf.add_transfer_group(c_tube,al1,5,{'from':{'tip-offset':-5}})
pf.assign_container(al1,ice,'F4')

# add exo I and III to cycler tube
pf.add_transfer_with_mix(exo,c_tube,4.1,{'to':{'tip-offset':-5,'touch-tip':False}})
#pf.add_transfer_group(UDG,c_tube,1.9,{'to':{'tip-offset':-5,'touch-tip':False}})
#pf.add_transfer_group(dil_Exo3,c_tube,1.9,{'to':{'tip-offset':-5,'touch-tip':False}})
#pf.add_transfer_with_mix(Exo1,c_tube,1.9,{'to':{'tip-offset':-5,'touch-tip':False}})

# second cycler instruction
pf.add_cycler_group('PFUNKEL2')

# aliquot 2
pf.add_transfer_group(c_tube,al2,5,{'from':{'tip-offset':-5}})
pf.assign_container(al2,ice,'F5')

# add secondary oligo to cycler tube
pf.add_transfer_with_mix(oligo2,c_tube,0.71,{'to':{'tip-offset':-5,'touch-tip':False}})

# third cycler instruction
pf.add_cycler_group('PFUNKEL3')

# aliquot 3
pf.add_transfer_group(c_tube,al3,5,{'from':{'tip-offset':-5}})
pf.assign_container(al3,ice,'F6')

# load aliquots with dye
pf.add_transfer_group(dye,al1,3.33)
pf.add_transfer_group(dye,al2,3.33)
pf.add_transfer_group(dye,al2,3.33)
pf.add_transfer_group(water,al1,11.66)
pf.add_transfer_group(water,al2,11.66)
pf.add_transfer_group(water,al3,11.66)

# hold cycler at 4 deg C
pf.add_cycler_group('4')

pp.pprint(pf.deck)
pp.pprint(pf.locations)
pp.pprint(pf.ingredients)
pp.pprint(pf.ingredients_export)
print("-----------------------------")
print(pf.list_unassigned_locations())
print(pf.list_unassigned_containers())
print("-----------------------------")
pp.pprint(pf.instructions)

pf.export_to_JSON('PFunkel.json')

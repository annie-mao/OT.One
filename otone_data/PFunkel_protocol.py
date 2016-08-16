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
polymerase = 'PfuTurbo_Cx_polymerase'
ligase = 'Taq_ligase'
NEBuffer_1 = 'NEBuffer_1'
Exo3 = 'Exonuclease_III'
UDG = 'UDG'
dil_Exo3 = 'diluted_Exonuclease_III'
Exo1 = 'Exonuclease_I'
al1 = 'aliquot_1'
al2 = 'aliquot_2'
al3 = 'aliquot_3'
oligo2 = 'P23-Amp-rev'
c_tube = 'cycler_tube'

# cycler
pf.add_cycler_prog('PFUNKEL1',4,2+60+15+10+2+15)
pf.add_cycler_prog('PFUNKEL2',4,80)
pf.add_cycler_prog('PFUNKEL3',4,47)
pp.pprint(pf.cycler)

# containers
ice = 'ice'
cycler = 'cycler'

# prepare ingredients
print(pf.add_ingredient(mm,mm,34))
print(pf.add_ingredient(water,water,100))
print(pf.add_ingredient(oligo1,oligo1,5))
print(pf.add_ingredient(ssDNA,ssDNA,20))
print(pf.add_ingredient(polymerase,polymerase,5))
print(pf.add_ingredient(ligase,ligase,5))
print(pf.add_ingredient(NEBuffer_1,NEBuffer_1,5))
print(pf.add_ingredient(Exo3,Exo3,5))
print(pf.add_ingredient(UDG,UDG,5))
print(pf.add_ingredient(Exo1,Exo1,5))
print(pf.add_ingredient(oligo2,oligo2,5))
print(pf.transfer_with_mix(water,mm,45.69))
print(pf.transfer_with_mix(oligo1,mm,1.65))
print(pf.transfer_with_mix(ssDNA,mm,12.66))
print(pf.transfer_with_mix(polymerase,mm,1))
print(pf.transfer_with_mix(ligase,mm,5))
pf.assign_container(mm,ice,'A1')
pf.assign_container(water,ice,'A2')
pf.assign_container(oligo1,ice,'A3')
pf.assign_container(ssDNA,ice,'A4')
pf.assign_labware(ice,'96-PCR-tubes')
pf.assign_container(polymerase,ice,'A5')
pf.assign_container(ligase,ice,'A6')
pf.assign_container(NEBuffer_1,ice,'B1')
pf.assign_container(Exo3,ice,'B2')
pf.assign_container(UDG,ice,'B3')
pf.assign_container(Exo1,ice,'B4')
pf.assign_container(oligo2,ice,'C1')

# exo III dilution
print(pf.add_transfer_group(water,dil_Exo3,3.75))
print(pf.add_transfer_group(NEBuffer_1,dil_Exo3,0.5))
print(pf.transfer_with_mix(Exo3,dil_Exo3,0.75))
pf.assign_container(dil_Exo3,ice,'B5')

# transfer to cycler
print(pf.add_transfer_group(mm,c_tube,100))
pf.assign_container(c_tube,cycler,'A1')
pf.assign_labware(cycler,'8-tube-strip')

# first cycler instruction
pf.add_cycler_group('PFUNKEL1')

# aliquot 1
pf.add_transfer_group(c_tube,al1,5)
pf.assign_container(al1,ice,'D1')

# add exo I and III to cycler tube
print(pf.transfer_with_mix(UDG,c_tube,1.9))
print(pf.transfer_with_mix(dil_Exo3,c_tube,1.9))
print(pf.transfer_with_mix(Exo1,c_tube,1.9))

# second cycler instruction
pf.add_cycler_group('PFUNKEL2')

# aliquot 2
print(pf.add_transfer_group(c_tube,al2,5))
pf.assign_container(al2,ice,'D2')

# add secondary oligo to cycler tube
print(pf.transfer_with_mix(oligo2,c_tube,0.71))

# third cycler instruction
pf.add_cycler_group('PFUNKEL3')

# aliquot 3
print(pf.add_transfer_group(c_tube,al3,5))
pf.assign_container(al3,ice,'D3')

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

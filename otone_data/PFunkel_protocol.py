from baseProtocol import BaseProtocol, InvalidEntry, Prompt
import pprint

pp = pprint.PrettyPrinter(indent=2)
pf = BaseProtocol("PFunkel","PFunkel Mutagenesis starting from master mix","note: testing")

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

# containers
ice = 'ice'

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
print(pf.add_transfer_group(water,mm,45.69))
print(pf.add_transfer_group(oligo1,mm,1.65))
print(pf.add_transfer_group(ssDNA,mm,12.66))
print(pf.add_transfer_group(polymerase,ligase,1))
pf.assign_container(mm,ice,'A1')
pf.assign_container(water,ice,'A2')
pf.assign_container(oligo1,ice,'A3')
pf.assign_container(ssDNA,ice,'A4')
pf.assign_container(polymerase,ice,'A5')
pf.assign_container(ligase,ice,'A6')
pf.assign_container(NEBuffer_1,ice,'A7')
pf.assign_container(Exo3,ice,'A8')
pf.assign_container(UDG,ice,'A9')
pf.assign_container(Exo1,ice,'A10')
pf.assign_container(oligo2,ice,'A11')
#d1 = []
#d2 = []
#d1.append(pf.transfer_dict(l1,l1,100))
#d2.append(pf.mix_dict(l1,100,{"repetitions":10}))
#print(d1)
#print(d2)
print('-----------')
#inst = b.assign_pipette(["transfer","mix"],[d1,d2])
#b.instructions.append(inst)
#b.add_cycler_prog('PFUNKEL1',63.6)
#b.add_cycler_group(['PFUNKEL1'])
pp.pprint(pf.locations)
pp.pprint(pf.ingredients)
pp.pprint(pf.ingredients_export)
print("-----------------------------")
print(pf.list_unassigned_locations())
print(pf.list_unassigned_containers())
print("-----------------------------")
#b.assign_labware(c1,'tube-rack-2ml')
#b.assign_container(l1,c2,'A1')
#pp.pprint(pf.deck)
#pp.pprint(pf.locations)
pp.pprint(pf.instructions)
#b.new_instruction_stream()
#pp.pprint(pf.instructions)

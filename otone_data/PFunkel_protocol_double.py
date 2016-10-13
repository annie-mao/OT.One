from baseProtocol import BaseProtocol, InvalidEntry, Prompt
import pprint

pp = pprint.PrettyPrinter(indent=2)
pf = BaseProtocol("PFunkel","PFunkel Mutagenesis starting from master mix","note: testing")
pf.set_container_library("containers.json")

# ingredients
oligo1_1 = 'oligo1_1'
oligo1_2 = 'oligo1_2'
ssDNA_1 = 'ssDNA_1'
ssDNA_2 = 'ssDNA_2'
oligo2_1 = 'oligo2_1'
oligo2_2 = 'oligo2_2'

al_1 = 'aliquot_1'
al_2 = 'aliquot_2'

c_tube_1 = 'cycler_tube_1'
c_tube_2 = 'cycler_tube_2'

mm = 'master_mix'
water = 'water'
enzymes = 'polymerase_ligase_mix'
exo = 'exonuclease_mix'
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
pf.add_ingredient(mm,mm,50)
pf.add_ingredient(enzymes,enzymes,15)
pf.add_ingredient(exo,exo,10)
pf.add_ingredient(water,water,200)
pf.add_ingredient(oil,oil,200)
pf.add_ingredient(dye,dye,20)

pf.add_ingredient(oligo1_1,oligo1_1,10)
pf.add_ingredient(oligo2_1,oligo2_1,10)
pf.add_ingredient(oligo1_2,oligo1_2,10)
pf.add_ingredient(oligo2_2,oligo2_2,10)

pf.add_ingredient(ssDNA_1,ssDNA_1,30)
pf.add_ingredient(ssDNA_2,ssDNA_2,30)

# assign containers to ingredients
pf.assign_container(mm,ice,'C3')
pf.assign_container(enzymes,ice,'C4')
pf.assign_container(exo,ice,'C5')
pf.assign_container(water,ice,'C6')
pf.assign_container(oil,ice,'C7')
pf.assign_container(dye,ice,'C8')


pf.assign_container(oligo1_1,ice,'D4')
pf.assign_container(oligo2_1,ice,'D5')
pf.assign_container(oligo1_2,ice,'E4')
pf.assign_container(oligo2_2,ice,'E5')

pf.assign_container(ssDNA_1,ice,'D6')
pf.assign_container(ssDNA_2,ice,'E6')

pf.assign_labware(ice,'96-PCR-tubes')

# make mix in cycler
pf.add_transfer_group(water,c_tube_1,36.72,{'to':{'touch-tip':False}})
pf.add_transfer_group(water,c_tube_2,36.72,{'to':{'touch-tip':False}})

pf.add_transfer_group(mm,c_tube_1,16.5)
pf.add_transfer_group(mm,c_tube_2,16.5)
pf.add_transfer_group(ssDNA_1,c_tube_1,21.43)
pf.add_transfer_group(ssDNA_2,c_tube_2,21.43)
pf.add_transfer_group(oligo1_1,c_tube_1,0.35)
pf.add_transfer_group(oligo1_2,c_tube_2,0.35)
pf.add_transfer_group(enzymes,c_tube_1,4.5)
pf.add_transfer_group(enzymes,c_tube_2,4.5)

pf.add_mix_group(c_tube_1,40)
pf.add_mix_group(c_tube_2,40)

pf.assign_container(c_tube_1,cycler,'A1')
pf.assign_container(c_tube_2,cycler,'A2')

pf.assign_labware(cycler,'8-tube-strip')

# add oil
oilSettings = {'extra-pull':True,'to':{'tip-offset':5,'touch-tip':False}}
pf.add_transfer_group(oil,c_tube_1,60,oilSettings)
pf.add_transfer_group(oil,c_tube_2,60,oilSettings)

# first cycler instruction
pf.add_cycler_group('PFUNKEL1')

# add exo I and III to cycler tube
afterOilSettings_tr = {'to':{'tip-offset':-10,'touch-tip':False}}
afterOilSettings_mix = {'tip-offset':-10}

pf.add_transfer_group(exo,c_tube_1,2.95,afterOilSettings_tr)
pf.add_transfer_group(exo,c_tube_2,2.95,afterOilSettings_tr)

pf.add_mix_group(c_tube_1,40,afterOilSettings_mix)
pf.add_mix_group(c_tube_2,40,afterOilSettings_mix)

# second cycler instruction
pf.add_cycler_group('PFUNKEL2')

# add secondary oligo to cycler tube
pf.add_transfer_group(oligo2_1,c_tube_1,0.32,afterOilSettings_tr)
pf.add_transfer_group(oligo2_2,c_tube_2,0.32,afterOilSettings_tr)

pf.add_mix_group(c_tube_1,40,afterOilSettings_mix)
pf.add_mix_group(c_tube_2,40,afterOilSettings_mix)

# third cycler instruction
pf.add_cycler_group('PFUNKEL3')

# aliquot
aliquotSettings = {'from':{'tip-offset':-10}}
pf.add_transfer_group(c_tube_1,al_1,5)
pf.add_transfer_group(c_tube_2,al_2,5)

# load aliquots with dye
pf.add_transfer_group(dye,al_1,3.33)
pf.add_transfer_group(dye,al_2,3.33)
pf.add_transfer_group(water,al_1,11.66)
pf.add_transfer_group(water,al_2,11.66)

pf.assign_container(al_1,ice,'D7')
pf.assign_container(al_2,ice,'E7')

# close cycler lid
pf.add_cycler_lid_cmd(True);

pp.pprint(pf.deck)
pp.pprint(pf.locations)
pp.pprint(pf.ingredients)
pp.pprint(pf.ingredients_export)
print("-----------------------------")
print(pf.list_unassigned_locations())
print(pf.list_unassigned_containers())
print("-----------------------------")
pp.pprint(pf.instructions)

pf.export_to_JSON('PFunkel_double_0927.json')

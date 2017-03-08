from pcr import PCR

a = PCR('robot_protocol_ORM30C_01_17_17','from robot_protocol_ORM30C.xlsx','created 01/17/17')
a.import_from_excel('robot_protocol_ORM30C_01_17_17.xlsx')
a.duplicate(4);
#a.printer.pprint(a.groups)
a.convert_to_protocol();
#print('------------------------------------------')
#print(a.p.list_unassigned_locations());
#print(a.p.list_unassigned_containers());
#print('------------------------------------------')
#a.printer.pprint(a.p.locations);
#print('------------------------------------------')
#a.printer.pprint(a.p.deck);
a.export_to_JSON("robot_protocol_testingnewcode.json");

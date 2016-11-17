from pcr import PCR

a = PCR('robot_protocol_11_15','from robot_protocol_11_15.xlsx','test')
a.import_from_excel('robot_protocol_11_15.xlsx')
a.duplicate(2);
a.printer.pprint(a.groups)
a.convert_to_protocol();
#print('------------------------------------------')
#print(a.p.list_unassigned_locations());
#print(a.p.list_unassigned_containers());
#print('------------------------------------------')
#a.printer.pprint(a.p.locations);
#print('------------------------------------------')
#a.printer.pprint(a.p.deck);
a.export_to_JSON("test.json");

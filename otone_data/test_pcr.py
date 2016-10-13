from pcr import PCR

a = PCR('test','test','test')
a.import_from_excel('robot_protocol_simple.xlsx')
a.duplicate(12);
a.printer.pprint(a.groups)
a.convert_to_protocol();
print('------------------------------------------')
print(a.p.list_unassigned_locations());
print(a.p.list_unassigned_containers());
print('------------------------------------------')
a.printer.pprint(a.p.locations);
print('------------------------------------------')
a.printer.pprint(a.p.deck);
a.p.export_to_JSON("test.json");

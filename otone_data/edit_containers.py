from containers import Containers

c = Containers("containers.json")

c.edit_container_yInc("tube-rack-2ml",19.5)
c.edit_container_xInc("tube-rack-2ml",19.5)
c.edit_container_val("tube-rack-2ml","depth",34)

c.edit_container_yInc("tiprack-200ul",9)
c.edit_container_xInc("tiprack-200ul",9.2)

c.edit_container_yInc("tiprack-10ul",9)
c.edit_container_xInc("tiprack-10ul",9.2)

c.edit_container_val("96-PCR-flat","depth",10)
c.edit_container_val("96-PCR-flat","total-liquid-volume",360)

'''
c.add_container("tiprack-200ul-diag",1,9,0,9,0,0,None,0,None)
for i in range(0,8):
	diag_loc=chr(ord('A')+i)+str(i+1)
	diag_x = c.get_val("tiprack-200ul",diag_loc,"x")
	c.edit_location_val("tiprack-200ul-diag","A"+str(i+1),"x",diag_x)
c.edit_location_val("tiprack-200ul-diag","A9","y",c.get_val("tiprack-200ul","A12","y"))
print(c.get_val("tiprack-200ul","A12","y"))
print(c.get_val("tiprack-200ul-diag","A9","y"))

for i in range(0,9):
	c.print_container_info("tiprack-200ul-diag","A"+str(i+1))
'''

c.container_corners("tiprack-200ul")
c.container_corners("tiprack-10ul")
c.export_to_JSON("containers.json")

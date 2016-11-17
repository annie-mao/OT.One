from containers import Containers

c = Containers("containers.json")

c.edit_container_yInc("tube-rack-2ml",19.5)
c.edit_container_xInc("tube-rack-2ml",19.5)
c.edit_container_val("tube-rack-2ml","depth",39)
c.edit_container_val("tube-rack-2ml","total-liquid-volume",2400)

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

c.add_container("8-tube-strip",1,8,0,9,0,0,20,5,300)
c.add_container("2-8-tube-strip",2,8,9,9,0,0,20,5,300)
c.add_container("96-PCR-tubes",8,12,9,9,0,0,20,5,300)
c.add_container("tube-rack-600ul",4,6,19.5,19.5,0,0,29.5,6,650)
c.add_container("tube-rack-1.5ml",4,6,19.5,19.5,0,0,37.5,9,1700)
c.add_container("tube-strip-600ul",1,6,19.5,19.5,0,0,29.5,6,650)
c.add_container("tube-strip-1.5ml",1,6,19.5,19.5,0,0,37.5,9,1700)
c.add_container("tube-strip-2ml",4,6,19.5,19.5,0,0,39,9,2400)
c.export_to_JSON("containers.json")

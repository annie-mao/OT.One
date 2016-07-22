# Testing function for Containers class
from containers import Containers

c = Containers()

# load_JSON
print("---------------------------------------------")
c.load_JSON("nonexistent.json")
c.load_JSON("containers.json")

# print_container_info
print("---------------------------------------------")
c.print_container_info("tiprack-200ul","A1")
c.print_container_info("tiprack-200ul","H12")
c.print_container_info("tiprack-200ul","Z1")
c.print_container_info("tiprack-2ul","A1")

# print_container_names
print("---------------------------------------------")
c.print_container_names()

# add_container
print("---------------------------------------------")
c.add_container("tiprack-200ul",8,12,8,8,0,0,None,4,None)
c.print_container_info("tiprack-200ul","A1")
c.print_container_info("tiprack-200ul","B2")
c.print_container_info("tiprack-200ul","C3")
c.print_container_info("tiprack-200ul","D4")
c.print_container_info("tiprack-200ul","E5")
c.print_container_info("tiprack-200ul","F6")
c.print_container_info("tiprack-200ul","G7")
c.print_container_info("tiprack-200ul","H8")
c.print_container_info("tiprack-200ul","A12")

# edit_container_xInc
print("---------------------------------------------")
c.edit_container_xInc("tiprack-200ul",9.25)
c.print_container_info("tiprack-200ul","A1")
c.print_container_info("tiprack-200ul","B2")
c.print_container_info("tiprack-200ul","C3")
c.print_container_info("tiprack-200ul","D4")
c.print_container_info("tiprack-200ul","E5")
c.print_container_info("tiprack-200ul","F6")
c.print_container_info("tiprack-200ul","G7")
c.print_container_info("tiprack-200ul","H8")
c.print_container_info("tiprack-200ul","A12")

# edit_container_yInc
print("---------------------------------------------")
c.edit_container_yInc("tiprack-200ul",9)
c.print_container_info("tiprack-200ul","A1")
c.print_container_info("tiprack-200ul","B2")
c.print_container_info("tiprack-200ul","C3")
c.print_container_info("tiprack-200ul","D4")
c.print_container_info("tiprack-200ul","E5")
c.print_container_info("tiprack-200ul","F6")
c.print_container_info("tiprack-200ul","G7")
c.print_container_info("tiprack-200ul","H8")
c.print_container_info("tiprack-200ul","A12")

# edit_container_val
c.edit_container_val("tube-rack-2ml","diameter",3)
c.edit_container_val("tube-rack-2ml","depth",1)
c.edit_container_val("tube-rack-2ml","total-liquid-volume",2001)
c.print_container_info("tube-rack-2ml","A1")

# get_val
print(c.get_val("tube-rack-2ml","A1","diameter"))

# container_corners
corner=c.container_corners("tiprack-200ul")
c.print_container_info(corner,"A1")
c.print_container_info(corner,"A2")
c.print_container_info(corner,"B1")
c.print_container_info(corner,"B2")

# del_container
#c.del_container("nonexistent")
#c.del_container(corner)
#c.print_container_info(corner,"A1")

import sys
sys.path.insert(0,'../otone_backend/backend')
from file_io import FileIO
import json

# container class facilitating update/generation of containers.json file

class Containers:
    """ Python way to generate/update containers.JSON """
    def __init__(self,fname):
        self.containersDict ={"containers":{}}
        if fname is not None:
            self.load_JSON(fname)
	
    def load_JSON(self,fname):
        """ Read in current containers.json and convert 
        from JSON to python dict
        """
        self.containersDict = FileIO.get_dict_from_json(fname)
        #fout=open("exportorder.json","w")
        #json.dump(self.containersDict,fout)

    def print_container_info(self,containerName,location):
        try:
            print("{0}, {1}:".format(containerName,location))
            for fieldStr,fieldVal in self.containersDict["containers"][containerName]["locations"][location].items():
                print("{0}: {1}".format(fieldStr,fieldVal))
            print("\n")
        except(KeyError):
            print("{0}, {1} does not exist.\n".format(containerName,location))

    def print_container_names(self):
        try:	
            print("All containers: ")
            for containerName,v in self.containersDict["containers"].items():
                print(containerName)
        except(KeyError):
            print("No containers in dictionary.\n")

    def add_container(self,containerName,numRows,numColumns,xInc,yInc,zInc_x,zInc_y,depth,diameter,TLV):
        if self.is_in_dict(containerName):
            overwrite = input("{0} already in dictionary. Overwrite? (Y/N):  ".format(containerName))
            if overwrite == 'N':
                return
        self.containersDict["containers"][containerName]={"locations":{}}
        # columns=numbers/y axis, rows=letters/x axis
        for col in range(0,numColumns):
            for row in range (0,numRows):
                locName=chr(ord('A')+row) + str(col+1)
                newLocation={"x":row*xInc, "y":col*yInc, "z":(row*zInc_x + col*zInc_y), "depth":depth, "diameter":diameter, "total-liquid-volume":TLV}
                self.containersDict["containers"][containerName]["locations"][locName]=newLocation
        return containerName		

    def edit_container_xInc(self,containerName,xInc):
        try:
            for location,v in self.containersDict["containers"][containerName]["locations"].items():
                rowNum = ord(location[0])-ord('A')
                v["x"]=rowNum*xInc
            print("{0} x-spacing changed to {1} mm\n".format(containerName,xInc))
        except(KeyError):
            print("{0} does not exist.\n".format(containerName))

    def edit_container_yInc(self,containerName,yInc):
        try:
            for location,v in self.containersDict["containers"][containerName]["locations"].items():
                colNum = int(location[1:])-1
                v["y"]=colNum*yInc
            print("{0} y-spacing changed to {1} mm\n".format(containerName,yInc))
        except(KeyError):
            print("{0} is not in dictionary.\n".format(containerName))

    def edit_container_val(self,containerName,fieldStr,newVal):
        try:
            for location,v, in self.containersDict["containers"][containerName]["locations"].items():
                self.edit_location_val(containerName,location,fieldStr,newVal)
            print("{0} {1} changed to {2}.\n".format(containerName,fieldStr,newVal))
        except(KeyError):
            print("{0} does not exist.\n".format(containerName))

    def edit_location_val(self,containerName,location,fieldStr,newVal):
        try:
            self.containersDict["containers"][containerName]["locations"][location][fieldStr] = newVal
        except(KeyError):
            print("{0}, {1} does not exist.\n".format(containerName,location))	

    def get_val(self,containerName,location,fieldStr):
        try:
            return self.containersDict["containers"][containerName]["locations"][location][fieldStr]
        except(KeyError):
            print("{0} {1} {2} does not exist.\n".format(containerName,location,fieldStr))

    def container_corners(self,containerName):
        ''' create container of the four corner positions in a container to test calibrations'''
        try:
        # get locations of four corners of original container and put in list
            listLocs = list(self.containersDict["containers"][containerName]["locations"].keys())
            rowLim='A'
            colLim=1
            for location in listLocs:
                row = location[0]
                col = int(location[1:])
                if(row>rowLim):
                    rowLim=row
                if(col>colLim):
                    colLim=col
            cornerLocs = ["A1",'A'+str(colLim),rowLim+'1',rowLim+str(colLim)]
            # create new container and copy values from corner locations of original container
            newName=containerName+"-corner-test"
            self.add_container(newName,2,2,0,0,0,0,None,None,None)
            i=0
            for location,info in self.containersDict["containers"][newName]["locations"].items():
                for fieldStr,fieldVal in info.items():
                    if(fieldStr in self.containersDict["containers"][containerName]["locations"][cornerLocs[i]]):
                        cornerVal=self.containersDict["containers"][containerName]["locations"][cornerLocs[i]][fieldStr]
                        self.containersDict["containers"][newName]["locations"][location][fieldStr]=cornerVal
                i+=1
            return newName
        except(KeyError):
            print("{0} does not exist.\n".format(containerName))
#TODO
#	def del_container(self,containerName):
#		try:
#			del(self.containersDict[containerName])
#		except(KeyError):
#			print("{0} does not exist.\n".format(containerName))

	
    def is_in_dict(self,containerName):
        if containerName in self.containersDict["containers"]:
            return True
        else:
            return False

    def export_to_JSON(self,fname):
        try:
            out_file=open(fname,"w")
            json.dump(self.containersDict,out_file,indent=4);
            print("Exported Python dict to {0}\n".format(fname))    
        except EnvironmentError as err:
            print("Error exporting Python dict to JSON\n")
            raise
        finally:
            if out_file is not None:
                out_file.close()


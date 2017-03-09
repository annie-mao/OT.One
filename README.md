# OT.One
Edited code from the Opentrons OT.One  

# Overview
## otone_backend
The backend of the robot, receives the job file and controls the movement  
of the robot via a ser2net connection to the Smoothieboard.  
The majority of my edits to the original OT.One code are found here in  
otone_backend/backend     

## otone_frontend
The frontend of the robot. Procesess user-input JSON protocols  
into a job file sent to the OT-One NodeJS script   
The only edits I made to this section are in   
otone_frontend/web/js/createJobFile.js  

## otone_data
Contains the container dimensions library used by the OT.One, containers.json  
Added a Python class facilitating update/generation of container libraries   
and a script converting the default containers.json to our custom library.   
Also contains a Python class representation of a standard liquid-handling   
protocol to facilitate working with JSONs, with scripts for automatic PCR/PFunkel   
protocol generation.         

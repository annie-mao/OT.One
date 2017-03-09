# Overview
Pythonic ways to work with JSONs and the OT.One container library  
## Containers
The container dimensions used by the robot are found in containers.json
The Containers class in containers.py facilitates update/generation of the JSON
file via Python dictionaries.
The edit_containers.py script converts the default containers library into our
custom library.

Files:
- containers.json
- containers.py
- edit_containers.py

## Protocol
The BaseProtocol class in baseProtocol.py is a Python dictionary-based
representation of a JSON protocol file. It makes it easier to manipulate
protocols with functions for common things like dynamically adding instruction
groups while keeping track of the volumes of different locations. Also enables
smart container selection, pipette selection, and automatic conversion into a
valid JSON protocol with all the required settings. TODO: distribute and
consolidate not currently supported.

protocol_ui.py and editor.py are the beginnings of a command-line protocol editor.

Files:
- baseProtocol.py
- editor.py
- protocolUI.py

## PCR and PFunkel
The PCR class in pcr.py uses BaseProtocol to generate PCR/PFunkel-specific JSONs
The excel2json.py script pulls information from a standard PFunkel excel protocol and
automatically generates a JSON to run on the robot. It also enables duplication of
the reaction specified in the excel file to run multiple reactions in parallel.
It takes care of container selection, deck layout, aliquots, robot settings, and
other PCR/PFunkel-specific parameters.
The PFunkel_protocol.py script is a line by line implementation of PFunkel JSON
generation from a BaseProtocol.

Files:
- pcr.py
- excel2json.py
- PFunkel_protocol.py

## Other scripts
Files:
The AnP_protocol.py script outputs AnP_test.json, a protocol for assessing the
accuracy and precision of volume transfer on the OT.One using dye photometry.

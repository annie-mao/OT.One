from baseProtocol import BaseProtocol, InvalidEntry

class PCR:
    def __init__(self, name, description, notes):
        self.p = BaseProtocol(name, description, notes)
        p.set_container_library("containers.json")

        self.name = name
        self.reagents = {}
        self.oligo1 = {}
        self.oligo2 = {}
        self.ssDNA = {}
        self.copies = 1
        self.rxns = [name+"_1"]

    def make_reagent_group(reagents,volumes):
        reagents = BaseProtocol.listify(reagents)
        volumes = BaseProtocol.listify(volumes)
        reagentDict = {}
        for reagent in reagents:
            reagentDict[reagent] = volumes
        self.reagents.append(reagentDict)

    def set_oligos(self,oligos):
        self.oligos = BaseProtocol.listify(oligos)

    def set_template(self,ssDNA):


    def set_cycler_steps(self,csteps):
        self.csteps = BaseProtocol.listify(csteps)

    def aliquot(self):


    def duplicate(self,n):



import os
import galspec.mpgadget.Field as fld

class _RKSGroups:
    def __init__(self,parent_dir):
        self.path = parent_dir + os.sep + "RKSGroups"
        self.parentpath = parent_dir

        self.GroupID                    = fld._GroupID(self.path)
        self.InternalGroupID            = fld._InternalGroupID(self.path)
        self.Length                     = fld._Length(self.path)
        self.VirialMass                 = fld._VirialMass(self.path)
        self.VirialRadius               = fld._VirialRadius(self.path)

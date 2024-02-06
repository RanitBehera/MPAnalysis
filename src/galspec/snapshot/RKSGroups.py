import os
import galspec.IO.Field as fld

class _RKSGroups:
    def __init__(self,parent_dir):
        self.path = parent_dir + os.sep + "RKSGroups"
        self.parentpath = parent_dir

        self.HaloID             = fld._HaloID(self.path)
        self.InternalHaloID     = fld._InternalHaloID(self.path)
        self.Length             = fld._Length(self.path)
        self.VirialMass         = fld._VirialMass(self.path)
        self.VirialRadius       = fld._VirialRadius(self.path)
        self.Position           = fld._Position(self.path)
        self.Velocity           = fld._Velocity(self.path)

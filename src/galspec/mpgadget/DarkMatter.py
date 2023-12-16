import os
import galspec.mpgadget.Field as fld

class _DarkMatter:
    def __init__(self,parent_dir):
        self.path = parent_dir + os.sep + "1"
        self.parentpath = parent_dir

        self.GroupID                     = fld._GroupID(self.path)
        self.ID                          = fld._ID(self.path)
        self.Mass                        = fld._Mass(self.path)
        self.Position                    = fld._Position(self.path)
        self.Potential                   = fld._Potential(self.path)
        self.Velocity                    = fld._Velocity(self.path)
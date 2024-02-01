import os
# from galspec.mpgadget.Gas import _Gas
# from galspec.mpgadget.DarkMatter import _DarkMatter
# from galspec.mpgadget.Neutrino import _Neutrino
# from galspec.mpgadget.Star import _Star
# from galspec.mpgadget.Blackhole import _BlackHole
from galspec.mpgadget.RKSGroups import _RKSGroups

# --- Temporary solution
import galspec.mpgadget.Field as fld
class _TempRSGPartDump:
    def __init__(self,parent_dir,part_type_int):
        self.path = parent_dir + os.sep + str(part_type_int)
        self.parentpath = parent_dir

        self.HaloID                     = fld._HaloID(self.path)
        self.InternalHaloID             = fld._InternalHaloID(self.path)
        self.AssignedInternalHaloID     = fld._AssignedInternalHaloID(self.path)
        self.ID                          = fld._ID(self.path)
        self.Mass                        = fld._Mass(self.path)
        # self.Position                    = fld._Position(self.path)
        # self.Velocity                    = fld._Velocity(self.path)
# --- Temporary solution 


class _RSG:
    def __init__(self,snap_num,base_dir):
        snap_num_fix='{:03}'.format(snap_num)
        self.path       = base_dir + os.sep + "RSG_" + snap_num_fix
        self.parentpath = base_dir
        self.snap_num   = snap_num

        self.Gas        = _TempRSGPartDump(self.path,0)
        self.DarkMatter = _TempRSGPartDump(self.path,1)
        # self.Neutrino   = _TempRSGPartDump(self.path,2)
        self.Star       = _TempRSGPartDump(self.path,4)
        self.BlackHole  = _TempRSGPartDump(self.path,5)
        self.RKSGroups  = _RKSGroups(self.path)

    # def ReadAttribute(self):
    #     return mp.ReadAttribute(self)
        

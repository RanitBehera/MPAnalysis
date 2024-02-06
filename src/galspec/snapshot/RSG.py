import os
import numpy
# from galspec.mpgadget.Gas import _Gas
# from galspec.mpgadget.DarkMatter import _DarkMatter
# from galspec.mpgadget.Neutrino import _Neutrino
# from galspec.mpgadget.Star import _Star
# from galspec.mpgadget.Blackhole import _BlackHole
from galspec.snapshot.RKSGroups import _RKSGroups
from galspec.snapshot.RSGAttribute import _RSGAttribute


# --- Temporary solution
# RSG particle fields are different from GADGET particle fields
# Proper is to make RSGGas and RSGDarkMatter class and its file
# Also have to modify original Gas to PARTGas then
import galspec.snapshot.Field as fld
class _TempRSGPartDump:
    def __init__(self,parent_dir,part_type_int):
        self.path = parent_dir + os.sep + str(part_type_int)
        self.parentpath = parent_dir

        self.HaloID                     = fld._HaloID(self.path)
        self.InternalHaloID             = fld._InternalHaloID(self.path)
        self.AssignedInternalHaloID     = fld._AssignedInternalHaloID(self.path)
        self.ID                         = fld._ID(self.path)
        self.Mass                       = fld._Mass(self.path)
        self.Position                    = fld._Position(self.path)
        self.Velocity                    = fld._Velocity(self.path)
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

        self.Attribute  = _RSGAttribute(self.path + "/Header/attr-v2")
        self.Utility    = _RGSUtility(self)



# Can not transfer this class to its own file due to circular import
# RGS needs RSGUtility for Utility meber and
# RSGUtility needs RSG for type hinting and intellisense
# If intellisense not needed we can transfer it to its own file
# if file make it in Utility folder

from galspec.utility.MassFunction import _mass_function_from_mass_list


class _RGSUtility:
    def __init__(self,RSG:_RSG) -> None:
        self.RSG = RSG

    def MassFunction(self,LogBinStep=0.5):
        mass_list = self.RSG.RKSGroups.VirialMass()
        volume = (self.RSG.Attribute.BoxSize()/1000)**3
        log_M, dn_dlogM,error = _mass_function_from_mass_list(mass_list,volume,LogBinStep)

        M = numpy.exp(log_M)
        return M,dn_dlogM






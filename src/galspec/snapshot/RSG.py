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

        self.Attribute  = _RSGAttribute(self.path + "/Header/attr-v2")
        self.Utility    = _RGSUtility(self)



# Can not transfer this class to its own file due to circular import
# RGS needs RSGUtility for Utility meber and
# RSGUtility needs RSG for type hinting and intellisense
# If intellisense not needed we can transfer it to its own file


from galspec.utility.MassFunction import mass_function_from_mass_list, mass_function_litreture
from typing import Literal



user_to_colossus_model_name_map =  { 
                "Press-Schechter" : "press74",
                "Seith-Tormen"    : "sheth99",
            }

user_to_colossus_qout_map =  { 
                "dn/dlnM" : "dndlnM",
                "(M2/rho0)*(dn/dm)"    : "M2dndM",
            }



class _RGSUtility:
    def __init__(self,RSG:_RSG) -> None:
        self.RSG = RSG

    def MassFunction(self,LogBinStep=0.5):
        mass_list = self.RSG.RKSGroups.VirialMass()
        volume = self.RSG.Attribute.BoxSize()
        log_M, dn_dlogM,error = mass_function_from_mass_list(mass_list,volume,LogBinStep)

        M = numpy.exp(log_M)
        return M,dn_dlogM
    
    def MassFunctionLitreture(self,
                              model_name : Literal["Press-Schechter","Seith-Tormen"],
                              mass_range,
                              output : Literal["dn/dlnM","(M2/rho0)*(dn/dm)"]
                              ):
        sim_cosmo = {
            'flat': True,   # Link this too
            'H0': self.RSG.Attribute.HubbleParam() * 100,
            'Om0': self.RSG.Attribute.Omega0(),
            'Ob0': self.RSG.Attribute.OmegaBaryon(),
            'sigma8': 0.81, # Link this too
            'ns': 0.971     # Link this too
            }

        model = user_to_colossus_model_name_map[model_name]
        q_out = user_to_colossus_qout_map[output]
        redshift = (1/self.RSG.Attribute.Time())-1

        return mass_function_litreture(sim_cosmo, model,redshift,mass_range,q_out)





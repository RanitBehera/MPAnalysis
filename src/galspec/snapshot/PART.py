import os
from galspec.snapshot.Gas import _Gas
from galspec.snapshot.DarkMatter import _DarkMatter
from galspec.snapshot.Neutrino import _Neutrino
from galspec.snapshot.Star import _Star
from galspec.snapshot.Blackhole import _BlackHole
from galspec.snapshot.PARTAttribute import _PARTAttribute

class _PART:
    def __init__(self,snap_num,base_dir):
        snap_num_fix='{:03}'.format(snap_num)
        self.path       = base_dir + os.sep + "PART_" + snap_num_fix
        self.parentpath = base_dir
        self.snap_num   = snap_num

        self.Gas        = _Gas(self.path)
        self.DarkMatter = _DarkMatter(self.path)
        self.Neutrino   = _Neutrino(self.path)
        self.Star       = _Star(self.path)
        self.BlackHole  = _BlackHole(self.path)

        self.Header     = _PARTAttribute(self.path + os.sep + "Header" + os.sep + "attr-v2")

    # def ReadAttribute(self):
    #     return mp.ReadAttribute(self)
    
    # def OutputRockstarHDF5(self,savepath,filename:str="",include_gas:bool=False,include_dm:bool=True,include_star:bool=False,include_bh:bool=False):
    #     if filename=="":filename="PART_"+'{:03}'.format(self.snap_num)+".hdf5"
    #     if not filename[-5:]==".hdf5":filename += ".hdf5"
    #     if not savepath[-1]==os.sep:savepath += os.sep
    #     filepath=savepath+filename
    #     mp.OutputRockstarHDF5(self,filepath,include_gas,include_dm,include_star,include_bh)
    #     return filepath

    # def OutputRockstarConfig(self,filename:str):
    #     pass
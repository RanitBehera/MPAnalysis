import os
from galspec.navigation.base.Folder import _Folder

from galspec.navigation.MPGADGET.PART.PART import _PART
from galspec.navigation.MPGADGET.PIG.PIG import _PIG
from galspec.navigation.MPGADGET.RSG.RSG import _RSG

from typing import Literal

class _Sim(_Folder):
    def __init__(self,path):
        super().__init__(path)

    def PART(self,snap_num:int):
        if not isinstance(snap_num,int):raise TypeError
        return _PART(os.path.join(self.path,"PART_" + self._FixedFormatSnapNumber(snap_num)))

    def PIG(self,snap_num:int):
        if not isinstance(snap_num,int):raise TypeError
        return _PIG(os.path.join(self.path,"PIG_" + self._FixedFormatSnapNumber(snap_num)))
    
    def RSG(self,snap_num:int):
        if not isinstance(snap_num,int):raise TypeError
        return _RSG(os.path.join(self.path,"RSG_" + self._FixedFormatSnapNumber(snap_num)))
    
    def _FixedFormatSnapNumber(self, snap_num):
        return '{:03}'.format(snap_num)



    def GetCosmology(self,purpose:Literal["MassFunctionLitrature"]):
        # Generate dictionary ready-to-input in purpose related function
        if (purpose=="MassFunctionLitrature"):    
            return {
                # Get these from simulation run files
                'flat': True,
                'H0': 69.7,
                'Om0': 0.2814,
                'Ob0': 0.0464,
                'sigma8': 0.81,
                'ns': 0.971
                }
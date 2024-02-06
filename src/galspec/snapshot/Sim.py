from galspec.snapshot.PART import _PART
from galspec.snapshot.PIG import _PIG
from galspec.snapshot.RSG import _RSG

from typing import Literal

class _Sim:
    def __init__(self,output_dir:str):
        if not isinstance(output_dir,str):raise TypeError
        self.path = output_dir

    def PART(self,snap_num:int):
        if not isinstance(snap_num,int):raise TypeError
        return _PART(snap_num,self.path)

    def PIG(self,snap_num:int):
        if not isinstance(snap_num,int):raise TypeError
        return _PIG(snap_num,self.path)
    
    def RSG(self,snap_num:int):
        if not isinstance(snap_num,int):raise TypeError
        return _RSG(snap_num,self.path)

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
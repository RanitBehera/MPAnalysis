
import os,numpy
from galspec.navigation.MPGADGET.RSG.RSG import _RSG
from galspec.navigation.MPGADGET.PART.PART import _PART
from galspec.IO.BinaryFile import WriteField

NUM_TYPES = 6   # Number of particle types in MPGADGET


class UL_RSG:
    def __init__(self,path,linked_part_path:None) -> None:
        self.RSG = _RSG(path)
        self.PART =  _PART(linked_part_path)

    def GetIds(self,tihid,ptype):
        # validate target ihid
        gihids = self.RSG.RKSGroups.InternalHaloID()
        if not tihid in gihids :
            print("Target IHID not present in Group catalogue.")
            return

        # validate particle type
        if not ptype in [0,1,4,5]:
            print("Unknown particle type in Group catalogue.")
            return
        
        # Get IDs
        if ptype==0:
            pihids  = self.RSG.Gas.InternalHaloID()
            pids    = self.RSG.Gas.ID()
        if ptype==1:
            pihids  = self.RSG.DarkMatter.InternalHaloID()
            pids    = self.RSG.DarkMatter.ID()
        if ptype==4:
            pihids  = self.RSG.Star.InternalHaloID()
            pids    = self.RSG.Star.ID()
        if ptype==5:
            pihids  = self.RSG.BlackHole.InternalHaloID()
            pids    = self.RSG.BlackHole.ID()

        mask = (pihids==tihid)
        pids = pids[mask]

        return pids


    



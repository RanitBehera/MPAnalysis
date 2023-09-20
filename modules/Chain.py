import sys
import os
sys.path.append(os.getcwd())

import numpy as np
import modules as mp


class HaloIDChain:
    def __init__(self,basedir,sid,gid):
        self.basedir=basedir
        self.sid=sid
        self.gid=gid
        self._CreateChain()

    def _CreateChain(self):
        # find sibling snapshot numbers
        sibs=[d for d in os.listdir(self.basedir.path) if os.path.isdir(os.path.join(self.basedir.path,d))]
        sibs=[int(d.split("PIG_")[-1]) for d in sibs if 'PIG_' in d]
        
        # get all stars in given halo
        stars_id=mp.ReadField(self.basedir.PIG(17).Star.ID)
        stars_gid=mp.ReadField(self.basedir.PIG(17).Star.GroupID)
        fids=np.where(stars_gid==self.gid)
        stars_fid=stars_id[fids]
        
        # for each sibling get all the star ids with group ids gid
        # for sib in sibs:
        print(stars_fid)

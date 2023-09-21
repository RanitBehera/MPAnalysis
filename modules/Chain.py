import sys
import os
sys.path.append(os.getcwd())

import numpy as np
import modules as mp

def GetSiblingSnapshots(basedir:mp.BaseDirectory,fgid):
    sibs=[d for d in os.listdir(basedir.path) if os.path.isdir(os.path.join(basedir.path,d))]
    return np.array([int(d.split("PIG_")[-1]) for d in sibs if 'PIG_' in d])

def GetStarsInGroup(basedir:mp.BaseDirectory,sid,fgid):
    id_stars=mp.ReadField(basedir.PIG(sid).Star.ID)
    gid_stars=mp.ReadField(basedir.PIG(sid).Star.GroupID)
    return id_stars[np.where(gid_stars==fgid)]   #fid_stars

def GetOverlapingStars(basedir:mp.BaseDirectory,sid1,fgid1,sid2,fgid2):
    fid_stars1=GetStarsInGroup(basedir,sid1,fgid1)
    fid_stars2=GetStarsInGroup(basedir,sid2,fgid2)
    return np.intersect1d(fid_stars1,fid_stars2) #cid_stars

def GetNearbyHalos():
    pass
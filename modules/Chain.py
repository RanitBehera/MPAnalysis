import sys
import os
sys.path.append(os.getcwd())

import numpy as np
import modules as mp


def GetStarsInGroup(basedir:mp.BaseDirectory,sid,fgid):
    id_stars=basedir.PIG(sid).Star.ID.ReadValues()
    gid_stars=basedir.PIG(sid).Star.GroupID.ReadValues()
    return id_stars[np.where(gid_stars==fgid)]   #fid_stars

def GetOverlapingStars(basedir:mp.BaseDirectory,sid1,fgid1,sid2,fgid2):
    fid_stars1=GetStarsInGroup(basedir,sid1,fgid1)
    fid_stars2=GetStarsInGroup(basedir,sid2,fgid2)
    return np.intersect1d(fid_stars1,fid_stars2) #cid_stars

def GetSiblingSnapshots(basedir:mp.BaseDirectory):
    sibs=[d for d in os.listdir(basedir.path) if os.path.isdir(os.path.join(basedir.path,d))]
    fsibs=[int(d.split("PIG_")[-1]) for d in sibs if 'PIG_' in d]
    # [print(s,type(s)) for s in fsibs]
    return fsibs 

def GetNearbyHalos(basedir:mp.BaseDirectory,sid,search_pos,search_rad):
    group_com=basedir.PIG(sid).FOFGroups.MassCenterPosition.ReadValues()
    group_ids=basedir.PIG(sid).FOFGroups.GroupID.ReadValues()-1    
    d=np.array([np.linalg.norm(pos-search_pos) for pos in group_com])
    nei=group_ids[np.where(d<=search_rad)]
    # nei=group_ids[np.where(np.abs(group_com[:,0]-search_pos[0])<search_rad)]
    return [int(x) for x in nei]


def GetChain(basedir:mp.BaseDirectory,tsid,tgid,search_rad=4000):
    pos=basedir.PIG(tsid).FOFGroups.MassCenterPosition.ReadValues()[tgid-1]
    sibs=GetSiblingSnapshots(basedir)
    chain_gid=np.full(len(sibs),np.nan)

    for s in range(len(sibs)):
        # print(sibs[s])
        neig_halo=GetNearbyHalos(basedir,sibs[s],pos,search_rad)
        ov_star_count=np.empty(len(neig_halo))
        for i in range(len(neig_halo)):
            ov_star_count[i]=len(GetOverlapingStars(basedir,tsid,tgid,sibs[s],neig_halo[i]))
        
        if len(ov_star_count)>0:
            max_ol_index=np.where(ov_star_count==np.max(ov_star_count))
            if len(max_ol_index[0])>1:
                continue
            else:
                # print("max",max_ol_index[0],len(max_ol_index[0]))
                chain_gid[s]=neig_halo[max_ol_index[0][0]]
    return chain_gid
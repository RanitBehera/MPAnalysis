import numpy,sys,os
from multiprocessing import Pool

sys.path.append("/home/ranitbehera/MyDrive/Repos/MPAnalysis/")
import galspec as mp


# --- CONFIG PARAMETERS
ROCKSTAR_PATH           = "/home/ranitbehera/MyDrive/Data/RKS_NEW/rks/output2/"
ROCKSTAR_HALO_FILENAME  = "halos_0.0.ascii"
ROCKSTAR_PART_FILENAME  = "halos_0.0.particles"



# --- DERIVED PARAMETERS
HFILEPATH               = ROCKSTAR_PATH + os.sep + ROCKSTAR_HALO_FILENAME
PFILEPATH               = ROCKSTAR_PATH + os.sep + ROCKSTAR_PART_FILENAME
SAVE_PATH               = ROCKSTAR_PATH + os.sep + "ehid_num_part.txt" 

# --- DATA BANK
print("Loading halos data ... ",end="")
halos=numpy.loadtxt(HFILEPATH)
print("Done")

print("Loading particle data ... ",end="")
particles=numpy.loadtxt(PFILEPATH)
print("Done")


# --- FILTER
def GetMaskFromIndices(length,indices):
    mask=numpy.zeros(length)
    mask[indices]=True
    return mask

def GetParticlesIN(EHID):
    EHID_mask=(particles[:,mp.particles.external_haloid]==EHID)
    EHID_pids=particles[EHID_mask,mp.particles.particle_id]

    # EHID_unique_pids_index=numpy.unique(EHID_pids,return_index=True)[1]
    # EHID_umask=GetMaskFromIndices(len(particles),EHID_unique_pids_index)
    
    # dm_mask=(particles[:,])



    # EHID_DM_mask=(particles[EHID_mask,mp.particles.type][EHID_unique_pids_index]==0)
    # EHID_DM_mask=(particles[EHID_mask,mp.particles.type][EHID_unique_pids_index]==1)
    # EHID_DM_mask=(particles[EHID_mask,mp.particles.type][EHID_unique_pids_index]==2)
    # EHID_DM_mask=(particles[EHID_mask,mp.particles.type][EHID_unique_pids_index]==3)







# f=open(SAVE_PATH,"w")
# numpy.savetxt(f,numpy.int64(t0_c),fmt="%d")
# f.close()


GetParticlesIN(2088)













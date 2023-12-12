import numpy,sys,os
from multiprocessing import Pool

sys.path.append("/mnt/home/student/cranit/Repo/MPAnalysis")
import galspecold as mp


# --- CONFIG PARAMETERS
ROCKSTAR_PATH           = "/mnt/home/student/cranit/Work/RKSG_Benchmark/L50N640c/RKSG_S36LL20_WP"
ROCKSTAR_HALO_FILENAME  = "halos_PART_036.hdf5.0.ascii"
ROCKSTAR_PART_FILENAME  = "halos_PART_036.hdf5.0.particles"



# --- DERIVED PARAMETERS
HFILEPATH               = ROCKSTAR_PATH + os.sep + ROCKSTAR_HALO_FILENAME
PFILEPATH               = ROCKSTAR_PATH + os.sep + ROCKSTAR_PART_FILENAME
SAVE_PATH               = ROCKSTAR_PATH + os.sep + "LengthByTypeSpdChk.txt" 

# --- DATA BANK
print("Loading halos data ... ",end="")
halos=numpy.loadtxt(HFILEPATH)
print("Done")

print("Loading particle data ... ",end="")
particles=numpy.loadtxt(PFILEPATH)
print("Done")

LEN=len(halos)

# --- FILTER
def GetMaskFromIndices(length,indices):
    mask=numpy.zeros(length)
    mask[indices]=True
    return numpy.bool_(mask)

def GetParticlesIN(EHID):
    EHID_mask=(particles[:,mp.particles.external_haloid]==EHID)
    EHID_pids=particles[EHID_mask,mp.particles.particle_id]

 
    unique_index=numpy.unique(EHID_pids,return_index=True)[1]
    unique_mask=GetMaskFromIndices(len(EHID_pids),unique_index)
    
    h_cx,h_cy,h_cz,h_rv = halos[EHID,[mp.ascii.x,mp.ascii.y,mp.ascii.z,mp.ascii.rvir]] 

    def GetNumPart(ptype):
        part_mask=(particles[EHID_mask,mp.particles.type][unique_mask]==ptype)

        x=(particles[EHID_mask,mp.particles.x][unique_mask][part_mask])-h_cx
        y=(particles[EHID_mask,mp.particles.y][unique_mask][part_mask])-h_cy
        z=(particles[EHID_mask,mp.particles.z][unique_mask][part_mask])-h_cz

        points=numpy.column_stack((x,y,z))
        distance=numpy.linalg.norm(points,axis=1)*1000
        virsphere_mask=(distance<=h_rv)

        final_mask_ids=particles[EHID_mask,mp.particles.particle_id][unique_mask][part_mask][virsphere_mask]
        # return ids to locate the particles which is not here

        return len(final_mask_ids)

    N_DM=GetNumPart(0)
    N_Gas=GetNumPart(1)
    N_Star=GetNumPart(2)
    N_BH=GetNumPart(3)

    print("EHID".ljust(4),(str(EHID)).rjust(16),"/",(str(LEN)).ljust(16),"Done")
    return N_DM,N_Gas,N_Star,N_BH

# print(GetParticlesIN(3972))

# --- Parallel Computation

from multiprocessing import Pool
def main():
    inputs=numpy.int64(halos[:,mp.ascii.id])
    print("Computing parallelly ... ",len(inputs))
    p=Pool(32)
    outputs=p.map(GetParticlesIN,inputs)
    # print("Done")

    print("Saving to file ...",end="")
    f=open(SAVE_PATH,"w")
    numpy.savetxt(f,numpy.int64(outputs),fmt="%d")
    f.close()
    print("Done")

    print("Saved To :",SAVE_PATH)


if __name__=="__main__":
    main()


















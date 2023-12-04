import numpy,sys,os
from multiprocessing import Pool

sys.path.append("/home/ranitbehera/MyDrive/Repos/MPAnalysis/")
import modules as mp


# --- CONFIG PARAMETERS
ROCKSTAR_PATH           = "/mnt/home/student/cranit/Work/RKSG_Benchmark/L50N640c/RKSG_036_VAR"
ROCKSTAR_HALO_FILENAME  = "halos_0.0.ascii"
ROCKSTAR_PART_FILENAME  = "halos_0.0.particles"



# --- DERIVED PARAMETERS
HFILEPATH               = ROCKSTAR_PATH + os.sep + ROCKSTAR_HALO_FILENAME
PFILEPATH               = ROCKSTAR_PATH + os.sep + ROCKSTAR_PART_FILENAME
SAVE_PATH               = ROCKSTAR_PATH + os.sep + "ehid_num_part.txt" 

# --- DATA BANK
print("Loading halo data ...")
halos=numpy.loadtxt(HFILEPATH)
print("Loading part data ...")
particles=numpy.loadtxt(PFILEPATH)

# --- Implementation 1
# HALO_LEN=len(halos)
# def Get_Number_of_Particles_in_Implement1(EHID,exclude_sub=False):
#     try:
#         print("EHID :",EHID," /",HALO_LEN," ... ",end="")
#         ehid_mask   = particles[:,mp.particles.external_haloid]==EHID
#         type0_mask   = particles[:,mp.particles.type]==0
#         type1_mask   = particles[:,mp.particles.type]==1
#         type2_mask   = particles[:,mp.particles.type]==2
#         type3_mask   = particles[:,mp.particles.type]==3
#         mask0        = ehid_mask & type0_mask
#         mask1        = ehid_mask & type1_mask
#         mask2        = ehid_mask & type2_mask
#         mask3        = ehid_mask & type3_mask
#         if exclude_sub:
#             ihids       = particles[ehid_mask,mp.particles.internal_haloid]
#             ihid        = int(numpy.unique(ihids)[0])
#             ihid_mask   = particles[:,mp.particles.assigned_internal_haloid]==ihid
#             mask0        = mask0 & ihid_mask
#             mask1        = mask1 & ihid_mask
#             mask2        = mask2 & ihid_mask
#             mask3        = mask3 & ihid_mask
#         nums=numpy.array([EHID,sum(mask0),sum(mask1),sum(mask2),sum(mask3)])
#         print("Done")
#         return nums
#     except:
#         return -1


# def main():
#     pool_input_ehid=range(100)
#     pool_output=0
#     p=Pool(8)
#     pool_output=p.map(Get_Number_of_Particles_in_Implement1,pool_input_ehid)
#     print(pool_output)


#     f=open(SAVE_PATH,"w")
#     numpy.savetxt(f,pool_output,fmt="%d")
#     f.close()

# if __name__=='__main__':
#     main()


# --- Implementation 2
part_type=particles[:,mp.particles.type]
int_HID=particles[:,mp.particles.internal_haloid]
asn_int_HID=particles[:,mp.particles.assigned_internal_haloid]

print("Filtering ...",end="")

# Filter 1, no substructuress, only dm
# root_mask=(int_HID==asn_int_HID)
# type0_mask=(part_type==0)
# type0_root_mask = root_mask & type0_mask
# ext_HID=particles[type0_root_mask,mp.particles.external_haloid]

# filter 2, include substructures only dm
type0_mask=(part_type==0)
ext_HID=particles[type0_mask,mp.particles.external_haloid]



print("Done")
t0_u,t0_c=numpy.unique(ext_HID,return_counts=True)

# id=numpy.where(t0_u==2088)
# print(t0_u[id],t0_c[id])


f=open(SAVE_PATH,"w")
numpy.savetxt(f,numpy.int64(t0_c),fmt="%d")
f.close()
















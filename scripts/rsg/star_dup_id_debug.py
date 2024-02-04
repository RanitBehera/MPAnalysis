import galspec
import numpy
import matplotlib.pyplot as plt



# galspec.CONFIG.MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/Work/ResetRKSG/rsg_L50MpcN640c"
galspec.CONFIG.MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/Work/ResetRKSG/rsg_L10MpcN64c"
sim = galspec.InitConfig()

SNAP_NO = 17


mass=sim.RSG(SNAP_NO).RKSGroups.VirialMass()
sa=numpy.argsort(mass)[::-1]

igid=sim.RSG(SNAP_NO).RKSGroups.InternalHaloID()
igid = igid[sa]

# ----- Connect to rockstar part
id=0
igid_star=sim.RSG(SNAP_NO).Star.InternalHaloID()                                 #<---
halo_star_ids = sim.RSG(SNAP_NO).Star.ID()[numpy.where(igid_star==igid[id])]     #<---
# numpy.savetxt("/mnt/home/student/cranit/Repo/MPAnalysis/temp_debug/hs_ids_sorted.txt",numpy.sort(halo_star_ids),fmt="%d")


# ----- Connect to part
galspec.CONFIG.MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L10Mpc_N64c/output"
sim = galspec.InitConfig()

all_star_ids = sim.PART(SNAP_NO).Star.ID()                                       #<---
# numpy.savetxt("/mnt/home/student/cranit/Repo/MPAnalysis/temp_debug/as_ids_sorted.txt",numpy.sort(all_star_ids),fmt="%d")




# check
print("ID Lengths : ")
print(len(halo_star_ids))
print(len(all_star_ids))

print("\nUnique ID Lengths : ")
print(len(numpy.unique(halo_star_ids)))
print(len(numpy.unique(all_star_ids)))


#----------------------------------------------

# match_hs=[]
# match_as=[]
# for hs in halo_star_ids:
#     for s in all_star_ids:
#         if hs==s:
#             match_hs.append(hs)
#             match_as.append(s)
#             # mstar.append([hs,s,count])
# match_hs = numpy.sort(match_hs)
# match_as = numpy.sort(match_as)

# numpy.savetxt("/mnt/home/student/cranit/Repo/MPAnalysis/temp_debug/match_hs_ids_sorted.txt",numpy.sort(match_hs),fmt="%d")
# numpy.savetxt("/mnt/home/student/cranit/Repo/MPAnalysis/temp_debug/match_as_ids_sorted.txt",numpy.sort(match_as),fmt="%d")



# -----------------------------------------------------

print("\nIsIn : ")

halo_star_ids = numpy.int64(halo_star_ids)
all_star_ids = numpy.int64(all_star_ids)

part_mask = numpy.isin(all_star_ids,halo_star_ids)
selected_stars = all_star_ids[part_mask]
print(len(selected_stars))

print("\nDebug : ")

u,c = numpy.unique(part_mask,return_counts=True)

print(u)
print(c)

# hs=numpy.sort(halo_star_ids)
# ss=numpy.sort(selected_stars)


# print(ss[55:65])

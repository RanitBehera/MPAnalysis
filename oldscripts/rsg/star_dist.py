import galspec
import numpy
import matplotlib.pyplot as plt



galspec.CONFIG.MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/Work/ResetRKSG/rsg_L50MpcN640c"
# galspec.CONFIG.MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/Work/ResetRKSG/rsg_L10MpcN64c"
sim = galspec.InitConfig()

mass=sim.RSG(36).RKSGroups.VirialMass()
sa=numpy.argsort(mass)[::-1]

igid=sim.RSG(36).RKSGroups.InternalGroupID()
igid = igid[sa]

# ----- Connect to rockstar part
id=0
igid_star=sim.RSG(36).Star.InternalGroupID()
halo_mask = numpy.where(igid_star==igid[id])
halo_star_ids = sim.RSG(36).Star.ID()[halo_mask]



# ----- Connect to part
galspec.CONFIG.MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L50Mpc_N640"
sim = galspec.InitConfig()

star_ids = sim.PART(36).Star.ID()
# star_ids = numpy.unique(star_ids)

# part_mask = numpy.in1d(star_ids,halo_star_ids)


# ---- Extract data
# sft=sim.PART(36).Star.StarFormationTime()[part_mask]
# z_sft = (1/sft)-1

# print(z_sft)


# check
print(len(halo_star_ids))
print(len(star_ids))
# print(len(sft))

exit()



# --- Save
SAVE_PATH = "/mnt/home/student/cranit/Work/ResetRKSG/Result/"

z_bins=numpy.linspace(int(min(z_sft))-1,int(max(z_sft))+1,20)
plt.hist(z_sft,bins=z_bins)

plt.xlabel("Star Formation Redshift")
plt.ylabel("Numbers of Star Formed")
# plt.axhline(100,ls='--',lw=1,color='k')
# plt.axhline(10000,ls='--',lw=1,color='k')

plt.title("L=50Mpc , N=$640^3$ , z=8 , $\\text{N}_{\\text{min}}^{\\text{halo}}=50$ , HID=" + str(id) + " , $\\text{N}_{\\text{star}}^{\\text{halo}}=$" + str(len(z_sft)),pad=10)

plt.savefig(SAVE_PATH + "star_formation_time_dist.png",dpi=200)
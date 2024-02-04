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
id=1
igid_gas=sim.RSG(36).Gas.InternalGroupID()
halo_mask = numpy.where(igid_gas==igid[id])
halo_gas_ids = sim.RSG(36).Gas.ID()[halo_mask]


# ----- Connect to part
galspec.CONFIG.MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L50Mpc_N640"
sim = galspec.InitConfig()

gas_ids = sim.PART(36).Gas.ID()

part_mask = numpy.in1d(gas_ids,halo_gas_ids)

# print(part_mask)
# print(len(part_mask))

# ---- Extract data
temp=sim.PART(36).Gas.InternalEnergy()[part_mask]
dens=sim.PART(36).Gas.Density()[part_mask]


# check
print(len(halo_gas_ids))
print(len(gas_ids))
print(len(temp))



# --- Save
SAVE_PATH = "/mnt/home/student/cranit/Work/ResetRKSG/Result/"

plt.plot(dens,temp,'.',ms=2)
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Density (??)")
plt.ylabel("Temperature (K)")
plt.axhline(100,ls='--',lw=1,color='k')
plt.axhline(10000,ls='--',lw=1,color='k')

plt.title("L=50Mpc , N=$640^3$ , z=8 , $\\text{N}_{\\text{min}}^{\\text{halo}}=50$ , HID=" + str(id) + " , $\\text{N}_{\\text{gas}}^{\\text{halo}}=$" + str(len(temp)),pad=10)

plt.savefig(SAVE_PATH + "temp_vs_dens_2.png",dpi=200)
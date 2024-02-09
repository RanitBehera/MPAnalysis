import galspec
import numpy
import matplotlib.pyplot as plt


# --- FLAGS : Set flags
SNAP_NUM    = 36
HALO_OFFSET = 0

# --- SIMS
L50N640     = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640/")

# --- AUTO-FLAGS
COSMOLOGY   = L50N640.GetCosmology("MassFunctionLitrature")
SNAP        = L50N640.RSG(SNAP_NUM)
REDSHIFT    = (1/SNAP.Attribute.Time())-1


# --- REORDER
ORDER       = numpy.argsort(SNAP.RKSGroups.VirialMass())[::-1]    # Reorders as decreasing mass

# --- PROCESS

# Get target halo fields
TIHID       = L50N640.RSG(SNAP_NUM).RKSGroups.InternalHaloID()[ORDER][HALO_OFFSET]
VMASS       = L50N640.RSG(SNAP_NUM).RKSGroups.VirialMass()[ORDER][HALO_OFFSET]


# Get linked
GAS_IHIDS   = L50N640.RSG(SNAP_NUM).Gas.InternalHaloID()
DM_IHIDS    = L50N640.RSG(SNAP_NUM).DarkMatter.InternalHaloID()
STAR_IHIDS  = L50N640.RSG(SNAP_NUM).Star.InternalHaloID()
BH_IHIDS    = L50N640.RSG(SNAP_NUM).BlackHole.InternalHaloID()

# --- GET PARTICLE ID FILTERING FOR TARGET
TGAS_IDS    = L50N640.RSG(SNAP_NUM).Gas.ID()()[(GAS_IHIDS==TIHID)]
TDM_IDS     = DM_IDS[(DM_IDS==TIHID)]
TSTAR_IDS   = STAR_IDS[(STAR_IDS==TIHID)]
TBH_IDS     = BH_IDS[(BH_IDS==TIHID)]

print(TDM_IDS)

exit()


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
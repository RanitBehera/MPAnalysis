import galspec
import numpy
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')


# --- SIMS
BOX         = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640/")
PARTBOX     = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/L50N640/")

# --- FLAGS : Set flags
SNAP_NUM    = 36
SAVE_PATH   = "/mnt/home/student/cranit/Work/RSGBank/Results/density_vs_temprature.png" 
HALO_OFFSET = 0


# --- AUTO-FLAGS
COSMOLOGY   = BOX.GetCosmology("MassFunctionLitrature")
SNAP        = BOX.RSG(SNAP_NUM)
PSNAP       = PARTBOX.PART(SNAP_NUM)
REDSHIFT    = (1/SNAP.Attribute.Time())-1


# --- REORDER
ORDER       = numpy.argsort(SNAP.RKSGroups.VirialMass())[::-1]    # Reorders as decreasing mass

# TARGET HALO FEILDS
TIHID       = BOX.RSG(SNAP_NUM).RKSGroups.InternalHaloID()[ORDER][HALO_OFFSET]
VMASS       = BOX.RSG(SNAP_NUM).RKSGroups.VirialMass()[ORDER][HALO_OFFSET]


# FILTER PARTICLE ROWS
GAS_IHIDS   = BOX.RSG(SNAP_NUM).Gas.InternalHaloID()
DM_IHIDS    = BOX.RSG(SNAP_NUM).DarkMatter.InternalHaloID()
STAR_IHIDS  = BOX.RSG(SNAP_NUM).Star.InternalHaloID()
BH_IHIDS    = BOX.RSG(SNAP_NUM).BlackHole.InternalHaloID()

# --- GET PARTICLE ID FILTERING FOR TARGET
TGAS_IDS    = SNAP.Gas.ID()[GAS_IHIDS==TIHID]
TDM_IDS     = SNAP.DarkMatter.ID()[DM_IHIDS==TIHID]
TSTAR_IDS   = SNAP.Star.ID()[(STAR_IHIDS==TIHID)]
TBH_IDS     = SNAP.BlackHole.ID()[(BH_IHIDS==TIHID)]


# GET TEMPERATURE & DENSITY
GAS_IDS     = PSNAP.Gas.ID()
TMASK       = numpy.isin(numpy.int64(GAS_IDS),numpy.int64(TGAS_IDS))

TEMP        = PSNAP.Gas.InternalEnergy()[TMASK] 
DENS        = PSNAP.Gas.Density()[TMASK] 

# PLOT
plt.plot(DENS,TEMP,'.',ms=2)

# --- BEAUTIFY
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Density (??)")
plt.ylabel("Temperature (K)")
plt.axhline(100,ls='--',lw=1,color='k')
plt.axhline(10000,ls='--',lw=1,color='k')

plt.title("L=50Mpc , N=$640^3$ , z=8 , $\\text{N}_{\\text{min}}^{\\text{halo}}=50$ , HID=" + str(TIHID) + " , $\\text{N}_{\\text{gas}}^{\\text{halo}}=$" + str(len(TEMP)),pad=10)


# --- SAVE
plt.savefig(SAVE_PATH,dpi=200)
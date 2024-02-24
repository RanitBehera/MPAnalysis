import numpy, galspec, os
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.gridspec import GridSpec


import matplotlib
matplotlib.use('Agg')

# --- SIMULATIONS
# Rockstar dump folder
# Make sure corresponding snapshorts are at same time
L50N640     = "/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640"
L140N700    = "/mnt/home/student/cranit/Work/RSGBank/OUT_L140N700"
L140N896    = "/mnt/home/student/cranit/Work/RSGBank/OUT_L140N896"
L140N1008   = "/mnt/home/student/cranit/Work/RSGBank/OUT_L140N1008"

# --- FLAGS
CFG         = galspec.RockstarCFG(L50N640)
SNAP_NUM    = 36
SAVE_PATH   = "/mnt/home/student/cranit/Work/RSGBank/Results_PMCAM/baryon_fraction_distribution.png" 
MASS_BINS = numpy.arange(7,12,1)
FB_BIN_START = -10
FB_BIN_END = 10
FB_BIN_NUM = 100


# --- AUTO-FLAGS
BOX_TEXT    = os.path.basename(CFG.INBASE)
BOX         = galspec.NavigationRoot(CFG.OUTBASE)
LINKED_BOX  = galspec.NavigationRoot(CFG.INBASE)
COSMOLOGY   = BOX.GetCosmology("MassFunctionLitrature")
SNAP        = BOX.RSG(SNAP_NUM)
REDSHIFT    = (1/SNAP.Attribute.Time())-1
BOX_SIZE    = SNAP.Attribute.BoxSize()/1000
MASS_UNIT   = 10**10
MASS_TABLE  = SNAP.Attribute.MassTable()
BOX_TEXT    = BOX.path.split("_")[-1]       # Special Case Work Only
HUBBLE      = SNAP.Attribute.HubbleParam()
FB_BIN_STEP    = ( FB_BIN_END-FB_BIN_START ) / FB_BIN_NUM


# --- GET FIELDS
M = SNAP.RKSGroups.MassByTypeInRvirWC()
M_gas, M_dm, M_u1, M_u2, M_star, M_bh = numpy.transpose(M) * MASS_UNIT
# Baryon fraction : Accretion efficiency
fb = (M_gas+M_star)/M_dm
exp_fb = SNAP.Attribute.OmegaBaryon()/SNAP.Attribute.Omega0()
# Stellar fration : Stelar conversion efficiency
# review
nz_mask = ((M_star+M_gas)!=0)
sf = (M_star[nz_mask])/(M_star+M_gas)[nz_mask] 


# --- PLOT
fig,ax = plt.subplots(4,1,sharex=True)

# --- HELPER FUNCTION
logm_dm = numpy.log10(M_dm)
# print(M_gas)
# exit()
def FB_HISTOGRAM(ax,logm_dm_s,logm_dm_e):
    mass_mask = ((logm_dm_s<=logm_dm) & (logm_dm<logm_dm_e))
    mass_in_range = logm_dm[mass_mask]
    fb_in_range = fb[mass_mask]
    ax.hist(fb_in_range,bins=40)
    ax.axvline(exp_fb,color="k")


def SF_HISTOGRAM(ax,logm_dm_s,logm_dm_e):  # review
    logm_dm_nz = logm_dm[nz_mask]
    mass_mask = ((logm_dm_s<=logm_dm_nz) & (logm_dm_nz<logm_dm_e))
    mass_in_range = logm_dm_nz[mass_mask]
    sf_in_range = sf[mass_mask]
    ax.hist(sf_in_range,bins=40)
    # ax.axvline(exp_fb,color="k")





for i in range(len(MASS_BINS)-1):
    FB_HISTOGRAM(ax[i],MASS_BINS[i],MASS_BINS[i+1])
    ax[i].set_yscale('log')

plt.savefig(SAVE_PATH,dpi=300)







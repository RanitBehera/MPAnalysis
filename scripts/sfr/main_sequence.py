import numpy, galspec
import matplotlib.pyplot as plt


import matplotlib
matplotlib.use('Agg')


# --- FLAGS
SNAP_NUM    = 36
SAVE_PATH   = "/mnt/home/student/cranit/Work/RSGBank/Results/sfr_distribution.png" 

# --- SIMULATIONS
BOX         = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640")

# --- AUTO-FLAGS
# Make sure cosmology in all simulations are same
COSMOLOGY   = BOX.GetCosmology("MassFunctionLitrature")
SNAP        = BOX.RSG(SNAP_NUM)
REDSHIFT    = (1/SNAP.Attribute.Time())-1
BOX_SIZE    = SNAP.Attribute.BoxSize()/1000
MASS_UNIT   = 10**10
MASS_TABLE  = SNAP.Attribute.MassTable() * MASS_UNIT
BOX_TEXT    = BOX.path.split("_")[-1]       # Special Case Work Only
HUBBLE      = SNAP.Attribute.HubbleParam()

# --- GET FIELDS
MVIR        = BOX.RSG(SNAP_NUM).RKSGroups.VirialMass()
LBT         = BOX.RSG(SNAP_NUM).RKSGroups.LengthByTypeInRvirWC()
SFR         = BOX.RSG(SNAP_NUM).RKSGroups.StarFormationRate()

# --- GET BUDGET
GAS,DM,U1,U2,STAR,BH = numpy.transpose(LBT)
GAS     *=  MASS_TABLE[0]
DM      *=  MASS_TABLE[1]
STAR    *=  MASS_TABLE[4]
BH      *=  MASS_TABLE[5]
MTOTAL  = GAS + DM + STAR + BH
RATIO = MTOTAL/MVIR


# --- SFR DISTRIBUTION
mask = (MVIR>3e10)
plt.plot(STAR[mask],SFR[mask],'.',ms=2)



# --- BEUTIFY
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.xlabel("$M_{*}/M_{\odot}$")
plt.ylabel("$SFR (M_{\odot} yr^{-1})$")
# plt.title(f"SFR DISTRIBUTION\n BOX : {BOX_TEXT} ; z={numpy.round(REDSHIFT,2)}")

# --- SAVE
plt.savefig(SAVE_PATH,dpi=200)
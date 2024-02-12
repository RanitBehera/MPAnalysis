import galspec
import numpy
import matplotlib.pyplot as plt
from galspec.visualization.Matcube import PlotCube

import matplotlib
matplotlib.use('Agg')


# --- SIMS
BOX         = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640/")
PARTBOX     = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/L50N640/")

# --- FLAGS : Set flags
SNAP_NUM    = 36
SAVE_PATH   = "/mnt/home/student/cranit/Work/RSGBank/Results/spatial_distribution.png" 
HALO_OFFSET = 0


# --- AUTO-FLAGS
COSMOLOGY   = BOX.GetCosmology("MassFunctionLitrature")
SNAP        = BOX.RSG(SNAP_NUM)
PSNAP       = PARTBOX.PART(SNAP_NUM)
REDSHIFT    = (1/SNAP.Attribute.Time())-1
BOX_SIZE    = SNAP.Attribute.BoxSize()/1000


# --- REORDER
ORDER       = numpy.argsort(SNAP.RKSGroups.VirialMass())[::-1]    # Reorders as decreasing mass

# TARGET HALO FEILDS
TIHID       = SNAP.RKSGroups.InternalHaloID()[ORDER][HALO_OFFSET]
TMVIR       = SNAP.RKSGroups.VirialMass()[ORDER][HALO_OFFSET]
TRVIR       = SNAP.RKSGroups.VirialRadius()[ORDER][HALO_OFFSET]
TPOS        = SNAP.RKSGroups.Position()[ORDER][HALO_OFFSET]


# FILTER PARTICLE ROWS
GAS_IHIDS   = SNAP.Gas.InternalHaloID()
DM_IHIDS    = SNAP.DarkMatter.InternalHaloID()
STAR_IHIDS  = SNAP.Star.InternalHaloID()
BH_IHIDS    = SNAP.BlackHole.InternalHaloID()

# --- GET PARTICLE ID FILTERING FOR TARGET
TGAS_POS    = SNAP.Gas.Position()[GAS_IHIDS==TIHID]
TDM_POS     = SNAP.DarkMatter.Position()[DM_IHIDS==TIHID]
TSTAR_POS   = SNAP.Star.Position()[(STAR_IHIDS==TIHID)]
TBH_POS     = SNAP.BlackHole.Position()[(BH_IHIDS==TIHID)]

# --- GET RELATIVE POSITION
TGAS_POS    -= TPOS
TDM_POS     -= TPOS
TSTAR_POS   -= TPOS
TBH_POS     -= TPOS


# PLOT
fig = plt.figure()
ax = plt.axes(projection='3d')

PlotCube(ax,TDM_POS,5*TRVIR/1000,2,'m')
PlotCube(ax,TGAS_POS,5*TRVIR/1000,2,'y')
PlotCube(ax,TSTAR_POS,5*TRVIR/1000,2,'b')
PlotCube(ax,TBH_POS,5*TRVIR/1000,2,'k')
# --- BEAUTIFY

# print(TRVIR)
# print(TDM_POS)

# --- SAVE
# plt.show()

plt.savefig(SAVE_PATH,dpi=200)
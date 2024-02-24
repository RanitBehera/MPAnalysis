import galspec
import numpy
import matplotlib.pyplot as plt
from galspec.visualization.Matcube import PlotCube

# import matplotlib
# matplotlib.use('Agg')


# --- SIMS
BOX         = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640/")
PARTBOX     = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/L50N640/")

# --- FLAGS : Set flags
SAVE_PATH   = "/mnt/home/student/cranit/Work/RSGBank/Results_PMCAM/halo_bh.png" 
SNAP_NUM    = 36
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

# --- GET RELATIVE DISTANCE
R_TGAS      = numpy.linalg.norm(TGAS_POS,axis=1)
R_TDM       = numpy.linalg.norm(TDM_POS,axis=1)
R_TSTAR     = numpy.linalg.norm(TSTAR_POS,axis=1)
R_TBH       = numpy.linalg.norm(TBH_POS,axis=1)

# --- GET RELATIVE POSITION BOUNDS
BOUND          = 2 * max(max(R_TGAS),max(R_TDM),max(R_TSTAR),max(R_TBH))

# PLOT
fig = plt.figure()

ax1 = fig.add_subplot(111,projection='3d')

# ax1 = fig.add_subplot(141,projection='3d')
# ax2 = fig.add_subplot(142,projection='3d')
# ax3 = fig.add_subplot(143,projection='3d')
# ax4 = fig.add_subplot(144,projection='3d')

# OFFSET
TRANSLATE    = numpy.ones(3)*(BOUND/2)
ZOOM_SCALE          = 1

# PlotCube(ax1,(TGAS_POS*ZOOM_SCALE) +TRANSLATE,BOUND,1,'m')
# PlotCube(ax1,(TGAS_POS*ZOOM_SCALE) +TRANSLATE,BOUND,1,'c')
# PlotCube(ax1,(TSTAR_POS*ZOOM_SCALE)+TRANSLATE,BOUND,5,'y')
PlotCube(ax1,(TBH_POS*ZOOM_SCALE)  +TRANSLATE,BOUND,[100,80],'k')

#  For blackhole size scaling
# bh_mask = (BH_IHIDS==TIHID)
# bh_mass = SNAP.BlackHole.Mass()[bh_mask]
# print(numpy.log10(bh_mass))
# For offset_id=1 blackhole mass almost macth


# --- BEAUTIFY
# ax1.set_title("Dark Matter")
# ax1.set_title("Gas")
# ax1.set_title("Star")
# ax1.set_title("Blackhole")

# print(TRVIR)
# print(TDM_POS)

# --- SAVE
for ax in [ax1]:
    ax.set_xlim(0,BOUND)
    ax.set_ylim(0,BOUND)
    ax.set_zlim(0,BOUND)
    ax.set_box_aspect([1.0, 1.0, 1.0])

plt.tight_layout()
# plt.show()

plt.savefig(SAVE_PATH,dpi=300)
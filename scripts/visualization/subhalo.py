import galspec,os
import numpy
import matplotlib.pyplot as plt
from galspec.visualization.Matcube import PlotCube

from treelib import Tree, Node


# --- SIMS
BOX         = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640")
PARTBOX     = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/L50N640")

# --- FLAGS : Set flags
SAVE_PATH   = "/mnt/home/student/cranit/Work/RSGBank/Results_PMCAM/subhalo_tree.png" 
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

# GET PARTICLE
DM_IHIDS    = SNAP.DarkMatter.InternalHaloID()
DM_AIHIDS   = SNAP.DarkMatter.AssignedInternalHaloID()
# Filter for asciated particles
thalo_mask  = (DM_IHIDS==TIHID)
TDM_POS     = SNAP.DarkMatter.Position()[thalo_mask]
# Get relative position
TDM_POS    -= TPOS


# ===================== SUBHALO BOX
def Get_Child_IHID(fihid): #facosued ihid (halo)
    fihid_mask = (DM_IHIDS==fihid)
    all_aihid  = DM_AIHIDS[fihid_mask]
    u,c = numpy.unique(all_aihid,return_counts=True)
    return u 

print(Get_Child_IHID(TIHID))
WHICH_SUB = 209

# sub_halo_mask

DM_IHIDS = DM_IHIDS[thalo_mask]
shalo_mask = (DM_AIHIDS[thalo_mask]==WHICH_SUB)


R_TDM       = numpy.linalg.norm(TDM_POS,axis=1)
BOUND          = 2 * max(R_TDM)

# PLOT
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')

# OFFSET
TRANSLATE    = numpy.ones(3)*(BOUND/2)
ZOOM_SCALE          = 1

# DRAW
PlotCube(ax,((TDM_POS*ZOOM_SCALE)+TRANSLATE)[shalo_mask],BOUND,3,'m')  # selected
PlotCube(ax,((TDM_POS*ZOOM_SCALE)+TRANSLATE)[~shalo_mask],BOUND,2,'k',alpha=0.2) # other


# --- BEAUTIFY
ax.set_xlim(0,BOUND)
ax.set_ylim(0,BOUND)
ax.set_zlim(0,BOUND)
ax.set_box_aspect([1.0, 1.0, 1.0])

plt.tight_layout()
plt.show()

# plt.savefig(SAVE_PATH,dpi=200)



        









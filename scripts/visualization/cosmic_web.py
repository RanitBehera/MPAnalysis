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
SAVE_PATH   = "/mnt/home/student/cranit/Work/RSGBank/Results_PMCAM/web_z8.png" 
SNAP_NUM    = 36


# --- AUTO-FLAGS
COSMOLOGY   = BOX.GetCosmology("MassFunctionLitrature")
SNAP        = BOX.RSG(SNAP_NUM)
PSNAP       = PARTBOX.PART(SNAP_NUM)
REDSHIFT    = (1/SNAP.Attribute.Time())-1
BOX_SIZE    = SNAP.Attribute.BoxSize()/1000


# FIELDS
MVIR        = SNAP.RKSGroups.VirialMass()
HALO_POS    = SNAP.RKSGroups.Position()

# MASK
MASK_MASS   = (MVIR>10**10)
mask        = MASK_MASS



# PLOT
fig = plt.figure(figsize=(8,8))
ax = plt.axes(projection='3d')

TRANSLATE    = numpy.zeros(3)
ZOOM_SCALE   = 1

# SCALE
logM = numpy.log10(MVIR)
logMmin = 7;logMmax = 11
Smin = 2;Smax = 20
Psize = Smin + ((Smax-Smin)/(logMmax-logMmin))*(logM-logMmin)
Psize = 20*(Psize/max(Psize))**4
PlotCube(ax,HALO_POS,BOX_SIZE,Psize,'k',0.3)
# PlotCube(ax,HALO_POS[~mask],BOX_SIZE,2,'k',0.01)

# --- BEAUTIFY
ax.set_xlim(0,BOX_SIZE)
ax.set_ylim(0,BOX_SIZE)
ax.set_zlim(0,BOX_SIZE)
ax.set_box_aspect([1.0, 1.0, 1.0])
# plt.tight_layout()
plt.title("L50N640\nz="+str(round(REDSHIFT,2))+"\n$N_{\\text{halo}}$ = "+ str(len(MVIR)),fontsize=16)

# --- SAVE

# --- STATIC FRAME
plt.show()
# plt.savefig(SAVE_PATH,dpi=200)

# --- FOR ANIMATION
# import os
# FRAME_OUT_PATH = "/mnt/home/student/cranit/Work/RSGBank/Results_PMCAM/frames"
# angles = numpy.linspace(0,359,360)
# for i,ang in enumerate(angles):
#     ax.view_init(20,40 + ang)
#     plt.savefig(os.path.join(FRAME_OUT_PATH,"fr_"+str(i+1)+".png"),dpi=300)
#     print("fr_"+str(i+1)+".png (",i+1,"/",len(angles),")")

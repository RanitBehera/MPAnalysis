import galspec
import numpy
import matplotlib.pyplot as plt
from galspec.visualization.Matcube import PlotCube




# --- SIMS
PARTBOX     = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/L10N64/output/")


# --- FLAGS : Set flags
SAVE_PATH   = "/mnt/home/student/cranit/Work/RSGBank/Results_PMCAM/web_z8.png" 
SNAP_NUM    = 17


# --- AUTO-FLAGS
SNAP       = PARTBOX.PART(SNAP_NUM)
REDSHIFT    = (1/SNAP.Attribute.Time())-1
BOX_SIZE    = SNAP.Attribute.BoxSize()/1000


# --- FIELDS
PART_POS    = SNAP.DarkMatter.Position()


# PLOT
fig = plt.figure(figsize=(8,8))
ax = plt.axes(projection='3d')

TRANSLATE    = numpy.zeros(3)
ZOOM_SCALE   = 1

# SCALE
PlotCube(ax,PART_POS/1000,BOX_SIZE,10,'k',0.03)

# --- BEAUTIFY
ax.set_xlim(0,BOX_SIZE)
ax.set_ylim(0,BOX_SIZE)
ax.set_zlim(0,BOX_SIZE)
ax.set_box_aspect([1.0, 1.0, 1.0])
# plt.tight_layout()
# plt.title("L50N640\nz="+str(round(REDSHIFT,2))+"\n$N_{\\text{halo}}$ = "+ str(len(MVIR)),fontsize=16)

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

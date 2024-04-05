import galspec
import numpy
import matplotlib.pyplot as plt
from galspec.visualization.Matcube import PlotCube


# --- SIMS
BOX         = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N1008")
PARTBOX     = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/L50N1008")

# --- FLAGS : Set flags
SAVE_PATH   = "/mnt/home/student/cranit/Work/RSGBank/Results_PMCAM/halo_bh.png" 
SNAP_NUM    = 36

# --- AUTO-FLAGS
SNAP        = BOX.RSG(SNAP_NUM)
PSNAP       = PARTBOX.PART(SNAP_NUM)
BOX_SIZE    = SNAP.Attribute.BoxSize()/1000



# GET SUBS
def GetPosOf(HID,Exclusive=True):
    ihid = SNAP.DarkMatter.InternalHaloID()
    aihid = SNAP.DarkMatter.AssignedInternalHaloID()
    t_mask  = (ihid==HID)
    mask = t_mask
    if Exclusive:
        ex_mask = (ihid==aihid)
        mask = mask & ex_mask
    pos = SNAP.DarkMatter.Position()[mask]
    return pos


# PLOTS
# Single
fig = plt.figure()
ax1 = fig.add_subplot(121,projection='3d')
ax2 = fig.add_subplot(122,projection='3d')
fig.set_facecolor((0.95,0.95,0.95))
# ax1.set_facecolor('black')

# === L50N1008
# # FOF
# PlotCube(ax1,GetPosOf(613,False),BOX_SIZE,1,'k',alpha=0.5)
# # Sub
# PlotCube(ax2,GetPosOf(613),BOX_SIZE,1,'r',alpha=0.5)
# PlotCube(ax2,GetPosOf(610),BOX_SIZE,1,'b',alpha=0.5)
# ------
# FOF
PlotCube(ax1,GetPosOf(544,False),BOX_SIZE,1,'k',alpha=0.2)
# Sub
PlotCube(ax2,GetPosOf(544),BOX_SIZE,1,'r',alpha=0.2)
PlotCube(ax2,GetPosOf(530),BOX_SIZE,1,'b',alpha=0.2)
PlotCube(ax2,GetPosOf(542),BOX_SIZE,1,'m',alpha=0.2)






plt.tight_layout()
plt.show()





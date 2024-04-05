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




# Animation

# def GetIDsOf(HID):
#     ihid = SNAP.DarkMatter.InternalHaloID()
#     aihid = SNAP.DarkMatter.AssignedInternalHaloID()
#     ex_mask = (ihid==aihid)
#     t_mask  = (ihid==HID)
#     mask = (ex_mask & t_mask)
#     id = SNAP.DarkMatter.ID()[mask]
#     return id

# def GetPosbyID(snap,id):
#     all_id = PARTBOX.PART(snap).DarkMatter.ID()
#     all_pos = PARTBOX.PART(snap).DarkMatter.Position()
#     mask = numpy.isin(numpy.int64(all_id),numpy.int64(id))
#     return all_pos[mask]

# ids = GetIDsOf(0)
# for snap in range(18):
#     fig = plt.figure()
#     ax1 = fig.add_subplot(111,projection='3d')
#     # fig.set_facecolor('black')
#     # ax1.set_facecolor('black')
    
#     plt.savefig("/mnt/home/student/cranit/Repo/MPAnalysis/temp/anim/subhalo_track/fr_"+str(snap)+".png",dpi=200)
#     plt.clf()
#     print(snap)
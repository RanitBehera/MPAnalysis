import numpy, galspec

# --- FLAGS
SNAP_NUM    = 17

# --- SIMULATIONS
L10N64     = galspec.NavigationRoot("/mnt/home/student/cranit/Work/ResetRKSG/RSG_L10N64")

ID = L10N64.RSG(SNAP_NUM).BlackHole.ID()
AIHID = L10N64.RSG(SNAP_NUM).BlackHole.AssignedInternalHaloID()
IHID = L10N64.RSG(SNAP_NUM).BlackHole.InternalHaloID()
EHID = L10N64.RSG(SNAP_NUM).BlackHole.HaloID()

# print(len(ID))
# print(len(AIHID))
# print(len(IHID))
# print(len(EHID))

fp = open("/mnt/home/student/cranit/Work/ResetRKSG/RSG_L10N64/converted.txt","w")

numpy.savetxt(fp,numpy.column_stack([ID,AIHID,IHID,EHID]),fmt="%d")


fp.close()
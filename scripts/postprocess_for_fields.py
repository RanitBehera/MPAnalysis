import galspec
from galspec.postprocess.PP_RSG import PP_RSG



L50N640     = "/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640"
L140N700    = "/mnt/home/student/cranit/Work/RSGBank/OUT_L140N700"
L140N896    = "/mnt/home/student/cranit/Work/RSGBank/OUT_L140N896"
L140N1008   = "/mnt/home/student/cranit/Work/RSGBank/OUT_L140N1008"

CFG         = galspec.RockstarCFG(L50N640)   # <---

SNAP_NUM    = 171
BOX         = galspec.NavigationRoot(CFG.OUTBASE)
LINKED_BOX  = galspec.NavigationRoot(CFG.INBASE)

pp = PP_RSG(BOX.RSG(SNAP_NUM).path,linked_part_path=LINKED_BOX.PART(SNAP_NUM).path)
pp.StartAll()
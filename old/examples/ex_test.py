import sys
import os
sys.path.append(os.getcwd())

import numpy as np
import modules as mp

# op=mp.BaseDirectory(r"D:\Ubuntu Back\Desktop\Sim\hydro\std_hydro\seed_181170\fg11\output")
op=mp.BaseDirectory(r"D:\Ubuntu Back\Desktop\Sim_640")

for s in [24]:#[24,30,36,42,50,60,71,83,99,127,171]:
    g=op.PIG(s).FOFGroups
    sfr=mp.ReadField(g.StarFormationRate)
    gid=mp.ReadField(g.GroupID)
    print(len(gid))
    print(sfr)
    # mass=mp.ReadField(op.PIG(36).FOFGroups.Mass)




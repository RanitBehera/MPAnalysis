import sys
import os
sys.path.append(os.getcwd())

import numpy as np
import galspec as mp
import matplotlib.pyplot as plt
import platform
ptfm=platform.system()
if ptfm=="Windows":
    op=mp.BaseDirectory(r"d:\Ubuntu Back\Desktop\Sim\hydro\std_hydro\seed_181170\fg11\output")    # Windows
    # op=mp.BaseDirectory(r"D:\Ubuntu Back\Desktop\Sim_640")    # Windows
elif ptfm=="Linux":
    op=mp.BaseDirectory("/home/ranitbehera/Drive Ranit/Data/MP-Gadget/Sim_L10N64/" )        # Linux

# a=op.PIG(17).FOFGroups.MassCenterPosition.showInCube(fids=[[1,2,3],[4,5],[6,7]],fcolor=['r','g','b'])

# pos=op.PIG(17).FOFGroups.MassCenterPosition.ReadValues()[0]
# groups=mp.GetNearbyHalos(op,17,pos,2000)
# op.PIG(17).FOFGroups.MassCenterPosition.showInCube(fids=[0],fcolor=['r'])

chain=mp.GetChain(op,17,1)
print(chain)
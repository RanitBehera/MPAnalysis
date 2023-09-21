import sys
import os
sys.path.append(os.getcwd())

import numpy as np
import modules as mp
import matplotlib.pyplot as plt
import platform
ptfm=platform.system()
if ptfm=="Windows":
    op=mp.BaseDirectory(r"d:\Ubuntu Back\Desktop\Sim\hydro\std_hydro\seed_181170\fg11\output")    # Windows
elif ptfm=="Linux":
    op=mp.BaseDirectory("/home/ranitbehera/Drive Ranit/Data/MP-Gadget/Sim_L10N64/" )        # Linux

a=op.PIG(17).FOFGroups.MassCenterPosition.showInCube(fids=[[1,2,3],[4,5],[6,7]],fcolor=['r','g','b'])
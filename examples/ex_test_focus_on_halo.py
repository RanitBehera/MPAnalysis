import sys
import os
sys.path.append(os.getcwd())

import numpy as np
import modules as mp
import matplotlib.pyplot as plt
op=mp.BaseDirectory(r"d:\Ubuntu Back\Desktop\Sim\hydro\std_hydro\seed_181170\fg11\output")
# op=mp.BaseDirectory(r"D:\Ubuntu Back\Desktop\Sim_640")

## Out - 0
# for i in range(18):
#     g=op.PIG(i).FOFGroups
#     gc=mp.ReadField(g.MassCenterPosition)
#     mass=mp.ReadField(g.Mass)

#     x=gc[:,0]
#     y=gc[:,1]
#     z=gc[:,2]

#     # print(x)

#     fig=plt.figure()
#     ax = plt.axes(projection='3d')

#     mp.PlotBox(ax,10000,x,y,z,10*(mass**(1/2)))

#     plt.savefig(r"D:\\frm\\fr"+str(i)+".png",dpi=300)
#     print(i)

# print(op.PIG(17).FOFGroups.MassCenterPosition)

# gid=mp.ReadField(op.PIG(17).FOFGroups.GroupID)

stars=mp.ReadField(op.PIG(17).Star.ID)



print(stars)
print(len(stars),len(np.unique(stars)))

# a=mp.HaloIDChain(op,17,1)
# print(a.sib)

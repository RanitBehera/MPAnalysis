import sys
import os
sys.path.append(os.getcwd())

import numpy as np
import modules as mp
import matplotlib.pyplot as plt
op=mp.BaseDirectory("/home/ranitbehera/MyDrive/Data/MP-Gadget/Sim_L10N64/")
# op=mp.BaseDirectory(r"D:\Ubuntu Back\Desktop\Sim_640")

# ## Out - 0
# for i in range(18):
#     ax=op.PIG(i).FOFGroups.MassCenterPosition.showInCube([0],['r'])
#     plt.savefig(r"D:\\frm\\fr"+str(i)+".png",dpi=300)
#     print(i)


## Out - 0
focus=0
# chain=mp.GetChain(op,17,focus+1)
chain=[[4],[9],[4],[6],[17],[2],[0],[0],[0],[0],[0],[0]]
for i in range(6,18):
    print(i)
    # print(type(chain[i]))
    # if not chain[i]==nan:
    #     c=[int(chain[i])]
    #     print(c)

    ax=op.PIG(i).FOFGroups.MassCenterPosition.showInCube(chain[i-6],['r'])
    plt.savefig("/home/ranitbehera/MyDrive/Results/"+str(i)+".png",dpi=300)




# #5.0
# 10.0
# 5.0
# 7.0
# 18.0
# 3.0
# 1.0
# 1.0
# 1.0
# 1.0
# 1.0
# 1.0

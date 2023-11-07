import sys
import os
sys.path.append(os.getcwd())

import numpy as np
import modules as mp
import matplotlib.pyplot as plt
op=mp.BaseDirectory("/home/ranitbehera/MyDrive/Data/MP-Gadget/Sim_L10N64/")


ax=op.PIG(17).FOFGroups.MassCenterPosition.showInCube([0],['r'])

plt.show()
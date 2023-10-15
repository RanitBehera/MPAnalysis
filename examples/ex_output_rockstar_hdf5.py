import sys
import os
sys.path.append(os.getcwd())

import numpy as np
import modules as mp

op=mp.BaseDirectory("/home/ranitbehera/MyDrive/Data/MP-Gadget/Sim_L10N64/")
saved_at=op.PART(17).OutputRockstarHDF5("/home/ranitbehera/MyDrive/Data/RKSTEST",include_gas=True,include_star=True,include_bh=True)
print("HDF5 Output Path :",saved_at)




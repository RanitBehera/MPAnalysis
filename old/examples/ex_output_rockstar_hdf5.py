import sys
import os
sys.path.append(os.getcwd())

import numpy as np
import galspec as mp

op=mp.BaseDirectory("/home/ranitbehera/MyDrive/Data/MP-Gadget/L50N640/")
saved_at=op.PART(36).OutputRockstarHDF5("/home/ranitbehera/MyDrive/Data/RKSTEST/CompareBig/",include_gas=True,include_star=True,include_bh=True)
print("HDF5 Output Path :",saved_at)




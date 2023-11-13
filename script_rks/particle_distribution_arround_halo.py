import numpy as np
import os


# Base directory
bd="/home/ranitbehera/MyDrive/Data/RKS_NEW/rks/output"

#files
fl="halos_PART_017.0.ascii"

# - Read Halo details
data=np.loadtxt(bd+os.sep+fl)


print(data)
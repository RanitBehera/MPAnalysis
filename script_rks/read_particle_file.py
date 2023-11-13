import numpy as np
import os


bd="/home/ranitbehera/MyDrive/Data/RKS_NEW/rks/output2"
# fl="halos_PART_017.0.ascii"
fl="halos_0.0.particles"
file=bd+os.sep+fl

data=np.loadtxt(file)

# id = data[:,0]
pid = data[:,8]
types = data[:,9]
# int_hid=data[:,]
# aint_hid=data[:,]

uni,uid=np.unique(pid,return_index=True)
types=types[uid]
uni,counts=np.unique(types,return_counts=True)



print(uni)
print(counts)


# print(type)
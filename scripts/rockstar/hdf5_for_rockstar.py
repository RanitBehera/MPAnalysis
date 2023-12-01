import sys
import os
sys.path.append(os.getcwd())
import modules as mp


# bd=input("Base Directory : ")

op=mp.BaseDirectory("/home/ranitbehera/MyDrive/Data/MP-Gadget/L10N64/")
saved_at=op.PART(16).OutputRockstarHDF5("/home/ranitbehera/MyDrive/Data/RKS_NEW/rks",include_gas=True,include_star=True,include_bh=True)
print("HDF5 Output Path :",saved_at)
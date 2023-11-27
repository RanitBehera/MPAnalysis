import sys
import os
sys.path.append(os.getcwd())
import modules as mp


# bd=input("Base Directory : ")

op=mp.BaseDirectory("/home/ranitbehera/MyDrive/Work/RKS_Benchmark/data/L10N64_PART_017/")
saved_at=op.PART(17).OutputRockstarHDF5("/home/ranitbehera/MyDrive/Work/RKS_Benchmark/data/",include_gas=True,include_star=True,include_bh=True)
print("HDF5 Output Path :",saved_at)
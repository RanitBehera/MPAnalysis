import sys
import os
sys.path.append(os.getcwd())
import modules as mp


# bd=input("Base Directory : ")

op=mp.BaseDirectory("/home/ranitbehera/MyDrive/Work/RKSG_Benchmark_2/L50N640c/")
saved_at=op.PART(36).OutputRockstarHDF5("/home/ranitbehera/MyDrive/Work/RKSG_Benchmark_2/L50N640c/Dump",include_gas=True,include_star=True,include_bh=True)
print("HDF5 Output Path :",saved_at)
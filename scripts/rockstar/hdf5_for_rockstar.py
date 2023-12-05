import sys
import os
sys.path.append(os.getcwd())
import modules as mp


# bd=input("Base Directory : ")

op=mp.BaseDirectory("/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L50Mpc_N640")
# for s in range (0,18):
saved_at=op.PART(16).OutputRockstarHDF5("/mnt/home/student/cranit/Work/RKSG_Benchmark/L50N640c",include_gas=True,include_star=True,include_bh=True)
print("HDF5 Output Path :",saved_at)
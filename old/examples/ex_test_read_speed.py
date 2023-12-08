import sys
import os
sys.path.append(os.getcwd())

import datetime

import numpy as np
import galspecold as mp

op=mp.BaseDirectory("/home/ranitbehera/MyDrive/Data/MP-Gadget/L50N640/")
# print("start : "+str(datetime.datetime.now().time()))
# out=op.PART(36).DarkMatter.Position.ReadValues()
# print("To Read  : "+str(datetime.datetime.now().time()))  # Taked about 1 min to read
# op=out*2
# print("To Operate  : "+str(datetime.datetime.now().time()))  # Taked about 1 min to read

print("start : "+str(datetime.datetime.now().time()))
saved_at=op.PART(36).OutputRockstarHDF5("/home/ranitbehera/MyDrive/Data/MP-Gadget/L50N640/RKS_036/",include_gas=True)
print("end : "+str(datetime.datetime.now().time()))

print("HDF5 Output Path :",saved_at)





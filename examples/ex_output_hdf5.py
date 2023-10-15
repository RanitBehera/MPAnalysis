import sys
import os
sys.path.append(os.getcwd())

import numpy as np
import modules as mp

op=mp.BaseDirectory("/home/ranitbehera/MyDrive/Data/MP-Gadget/Sim_L10N64/")

pos=op.PART(17).DarkMatter.Position.ReadValues()
vel=op.PART(17).DarkMatter.Velocity.ReadValues()
id=op.PART(17).DarkMatter.ID.ReadValues()

mp.SaveRockstarHDF5(id,pos,vel,"/home/ranitbehera/MyDrive/Data/RKSTEST/HDF/part017.hdf5")


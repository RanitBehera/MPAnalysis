import numpy as np

import sys
import os
sys.path.append(os.getcwd())
import modules as mp

op=mp.BaseDirectory("/home/ranitbehera/MyDrive/Data/MP-Gadget/Sim_L10N64/")

attr=op.PART(17).ReadAttribute()
print("BoxSize =",attr.BoxSize)
print("Hubble parameter =",attr.HubbleParam)
print("Total Number of Particle =", attr.TotNumPart)
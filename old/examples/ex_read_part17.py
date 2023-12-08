import numpy as np

import sys
import os
sys.path.append(os.getcwd())
import galspec as mp


op=mp.BaseDirectory(r"D:\Ubuntu Back\Desktop\Sim\hydro\std_hydro\seed_181170\fg11\output")
pos=op.PART(17).BlackHole.Position.ReadValues()
vel=op.PART(17).BlackHole.Velocity.ReadValues()
id=op.PART(17).BlackHole.ID.ReadValues()
mass=op.PART(17).BlackHole.Mass.ReadValues()

di=int(input("Debug Index :"))
while(di>-1):
    print("ID: ",id[di])
    print("mass: ",mass[di])
    print("Pos: ",pos[di])
    print("Vel: ",vel[di])
    di=int(input("Debug Index :"))

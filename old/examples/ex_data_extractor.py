import sys
import os
sys.path.append(os.getcwd())

import numpy as np
import galspecold as mp

op=mp.BaseDirectory(r"D:\Ubuntu Back\Desktop\Sim\hydro\std_hydro\seed_181170\fg11\output")
# op=mp.BaseDirectory(r"D:\Ubuntu Back\Desktop\Sim_640")


pos=op.PART(17).DarkMatter.Velocity.ReadValues()

at=0
while(at>=0):
    at=input("index : ")
    at=int(at)
    print(pos[at])
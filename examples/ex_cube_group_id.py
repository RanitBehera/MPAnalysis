import sys
import os
sys.path.append(os.getcwd())

import numpy as np
import modules as mp
import matplotlib.pyplot as plt
op=mp.BaseDirectory(r"d:\Ubuntu Back\Desktop\Sim\hydro\std_hydro\seed_181170\fg11\output")

a=op.PIG(17).FOFGroups.MassCenterPosition.showInCube()


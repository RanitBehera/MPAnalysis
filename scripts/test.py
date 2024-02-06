import numpy, galspec
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')



# --- SIMULATIONS
L10N64     = galspec.NavigationRoot("/mnt/home/student/cranit/Work/ResetRKSG/RSG_L10N64")

s=L10N64.RSG(17).Star.InternalHaloID()




print(s)
import numpy, galspec
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')



# --- SIMULATIONS
BOX     = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640")

count = BOX.RSG(36).RKSGroups.LengthByTypeInRvirWC()

gas = count[:,0]
dm = count[:,1]
st = count[:,4]

gas *= BOX.RSG(36).Attribute.MassTable()[0]
dm *= BOX.RSG(36).Attribute.MassTable()[1]
st *= BOX.RSG(36).Attribute.MassTable()[4]

ratio = (gas+st)/dm
# ratio = (gas)/(gas+st+0.0001)

ex_ratio = BOX.RSG(36).Attribute.OmegaBaryon()/BOX.RSG(36).Attribute.Omega0()

plt.hist(ratio,bins=100)
plt.axvline(ex_ratio,color="k")
plt.yscale('log')
# plt.xscale('log')

plt.savefig("/mnt/home/student/cranit/Work/RSGBank/Results/test.png")







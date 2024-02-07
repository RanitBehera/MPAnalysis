import numpy, galspec
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')



# --- SIMULATIONS
L10N64     = galspec.NavigationRoot("/mnt/home/student/cranit/Work/ResetRKSG/RSG_L10N64")

mass = L10N64.RSG(17).RKSGroups.VirialMass()

from galspec.IO.Field import _Field
lbt = _Field("/mnt/home/student/cranit/Work/ResetRKSG/RSG_L10N64/RSG_017/RKSGroups/LengthByTypeInRvirWC")()

gas,dm,u1,u2,star,bh = numpy.transpose(lbt)

gas  = gas * L10N64.RSG(17).Attribute.MassTable()[0]
dm   = dm * L10N64.RSG(17).Attribute.MassTable()[1]
star = star * L10N64.RSG(17).Attribute.MassTable()[4]
bh   = bh * L10N64.RSG(17).Attribute.MassTable()[5]

total = gas + dm + star + bh
total *= 10**10


ratio = total/mass

asort = numpy.argsort(mass)
mass  = mass[asort]
ratio = ratio[asort]

import matplotlib.pyplot as plt

plt.hist(ratio,bins=100)
plt.yscale('log')

plt.savefig("/mnt/home/student/cranit/Work/ResetRKSG/Result/check_mvir_calc_hist.png",dpi=200)




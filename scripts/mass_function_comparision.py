import galspec
import numpy
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')


sim = galspec.NavigationRoot("/mnt/home/student/cranit/Work/ResetRKSG/RSG_L50N640")


log_M, dn_dlogM = sim.RSG(36).Utility.MassFunction()
plt.plot(log_M,dn_dlogM)

mass_hr = numpy.logspace(7,12,100)

log_M, dn_dlogM = sim.RSG(36).Utility.MassFunctionLitreture('Press-Schechter',mass_hr,'dn/dlnM')
plt.plot(log_M,dn_dlogM)

log_M, dn_dlogM = sim.RSG(36).Utility.MassFunctionLitreture('Seith-Tormen',mass_hr,'dn/dlnM')
plt.plot(log_M,dn_dlogM)

sim.RSG(36)



plt.xscale('log')
plt.yscale('log')

plt.savefig("/mnt/home/student/cranit/Work/ResetRKSG/Result/check_mass_function.png",dpi=200)

print(log_M)

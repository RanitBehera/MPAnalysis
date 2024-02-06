import numpy, galspec
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')

# --- FLAGS
SNAP_NUM    = 36
HR_MASS     = numpy.logspace(7,13,100) # High resolution mass for litrature mass function plot

# --- SIMULATIONS
L50N640     = galspec.NavigationRoot("/mnt/home/student/cranit/Work/ResetRKSG/RSG_L50N640")
L140N1008   = galspec.NavigationRoot("/mnt/home/student/cranit/Work/ResetRKSG/RSG_L140N1008")

# --- AUTO-FLAGS
# Make sure cosmology in all simulations are same
COSMOLOGY   = L50N640.GetCosmology("MassFunctionLitrature")
REDSHIFT    = (1/L50N640.RSG(SNAP_NUM).Attribute.Time())-1



# --- SIMULATION MASS FUNCTIONS
log_M, dn_dlogM = L50N640.RSG(SNAP_NUM).Utility.MassFunction()
plt.plot(log_M,dn_dlogM,label="L50N640",lw=1)

log_M, dn_dlogM = L140N1008.RSG(SNAP_NUM).Utility.MassFunction()
plt.plot(log_M,dn_dlogM,label="L140N1008",lw=1)

# --- LITRARTURE MASS FUNCTIONS
log_M, dn_dlogM = galspec.Utility.MassFunctionLitreture("Seith-Tormen",COSMOLOGY,REDSHIFT,HR_MASS,"dn/dlnM")
plt.plot(log_M,dn_dlogM*0.697,'k',label="Seith-Tormen",lw=1,zorder=-1)


# --- PLOT ENHANCE
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.xlabel("Mass $(M/M_\odot)$")

plt.savefig("/mnt/home/student/cranit/Work/ResetRKSG/Result/check_mass_function.png",dpi=200)


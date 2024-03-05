import numpy
import matplotlib.pyplot as plt
import astropy
from astropy.cosmology import FlatLambdaCDM


filepath = "/mnt/home/student/cranit/Work/RSGBank/TBSFR_Bank/luminosities.txt"

off,ed,sfr=numpy.loadtxt(filepath).T


# Ed to lum by multipkying luminosisty disnatce
import astropy
HUBBLE = 69.7
OMEGA_M = 0.2814
CMBT = 2.7255
REDSHIFT = 8
cosmo = FlatLambdaCDM(H0=HUBBLE, Om0=OMEGA_M, Tcmb0=CMBT)
DL=cosmo.luminosity_distance(REDSHIFT).value
Mpc_2_cm = 3.086e24
DL *= Mpc_2_cm
Area = 4*numpy.pi*(DL**2)

lum = Area*ed*(1+REDSHIFT)

# igm correction





plt.plot(sfr,lum,'.')


# Eq 12 of Harikane Et al. https://iopscience.iop.org/article/10.3847/1538-4365/acaaa9
# SFR (M0 yr-1) = (K_UV) * L_UV(ergs s-1 Hz-1)
# K_UV = 1.15e-28 ( M0 yr-1 / ergs s-1 Hz-1) : UV = 1500A
lam = 1450e-10*(1)
c = 3e10*1e-8
nu = c/lam
K_UV = 1.15e-28
K_UV /= (nu**2/c)

X = numpy.array([min(sfr),max(sfr)])
Y = X/K_UV
plt.plot(X,Y)

plt.xlabel("SFR")
plt.ylabel("$L_{UV}$")
plt.xscale('log')
plt.yscale('log')
plt.show()
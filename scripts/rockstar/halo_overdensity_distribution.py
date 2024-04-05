import galspec
import numpy
import matplotlib.pyplot as plt

BOX = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640")
SNAP = BOX.RSG(36)


# --- Cosmology
h   = 1
Om, Ol  = 0.2814, 0.7186

# Mean universal matter density
rho_crit = 2.7754e11 * h**2 # M_solar / Mpc**3
rho_m = rho_crit * Om

# Overdensity of all halos
rvir = SNAP.RKSGroups.VirialRadius()/1000 # Kpc to Mpc
mvir = SNAP.RKSGroups.VirialMass()
mv_sort = numpy.argsort(mvir)[::-1]
halo_density = mvir / ((4/3)*numpy.pi*rvir**3)
halo_density = halo_density[mv_sort]

# already Sorted by mvir
Delta_halo = halo_density/rho_m


# masks
mask = (mvir>1e10)
# Delta_halo = Delta_halo[mask]

print(numpy.where(Delta_halo>250))

plt.hist(Delta_halo,bins=100)
plt.yscale("log")
plt.show()

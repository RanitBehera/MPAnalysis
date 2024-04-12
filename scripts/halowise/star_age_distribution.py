import numpy,galspec
import matplotlib.pyplot as plt
import bagpipes as pipes
import astropy

# SIMULATION
L50N640     = "/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640"

# FLAGS
CFG = galspec.RockstarCFG(L50N640)
SNAP_NUM = 36
HALO_OFFSET = 0

# Connect
BOX = galspec.NavigationRoot(CFG.OUTBASE)
LINKED_BOX = galspec.NavigationRoot(CFG.INBASE)
SNAP = BOX.RSG(SNAP_NUM)
LINKED_SNAP = LINKED_BOX.PART(SNAP_NUM)

# AUTO-FLAGS
HUBBLE = SNAP.Attribute.HubbleParam() *100
OMEGA_M = SNAP.Attribute.Omega0()
CMBT = SNAP.Attribute.CMBTemperature()
REDSHIFT    = (1/SNAP.Attribute.Time())-1

# Get list of halos
halos = SNAP.RKSGroups.VirialMass()

# Argument sort
mvir_sort = numpy.argsort(halos)[::-1]

# Sorted halo ids
IHIDS = SNAP.RKSGroups.InternalHaloID()[mvir_sort]

# Target one halo by offset
TIHID = IHIDS[HALO_OFFSET]

# Get all star particles
IHIDS_star  = SNAP.Star.InternalHaloID()

# Locate target stars
target_mask = (IHIDS_star==TIHID)

# Get target star ids
TIDs = SNAP.Star.ID()[target_mask]

# Get part star ids
IDs_star = LINKED_SNAP.Star.ID()

# Get selcted mask
selection_mask = numpy.isin(numpy.int64(IDs_star),numpy.int64(TIDs))

# Get formation redhifts
times = LINKED_SNAP.Star.StarFormationTime()[selection_mask]
redshifts = (1/times)-1

# Get ages
from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=HUBBLE, Om0=OMEGA_M, Tcmb0=CMBT)
def get_age(redshift):
    ages = [(cosmo.age(z)).value for z in redshift]
    return numpy.array(ages)

star_birth_univ_age = get_age(redshifts)*1e9
tsnap_univ_age = get_age([REDSHIFT])*1e9

age = tsnap_univ_age-star_birth_univ_age
age_Myr = age/1e6

plt.hist(age_Myr,bins=30)


plt.title("Stellar age distribution\nHID="+str(TIHID)+" ; z="+str(numpy.round(REDSHIFT,2)) + " ; $N_{*}$=" + str(len(age)))
plt.ylabel("Count")
plt.xlabel("Age (Myr)")

plt.show()
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

plt.hist(age/1e9,bins=100)

# ========================= upto this same as star_age_distribution.py

# Get Metalicity
metallicity = LINKED_SNAP.Star.Metallicity()[selection_mask]


goodss_filt_list = numpy.loadtxt("/mnt/home/student/cranit/Repo/MPAnalysis/oldscripts/bagpipes/filters/myfilters.txt", dtype="str")

dust = {}                         
dust["type"] = "Calzetti"         
dust["Av"] = 0.2                  
dust["eta"] = 3.                  

nebular = {}                      
nebular["logU"] = -3.             


model_components = {}                   
model_components["redshift"] = 8
# model_components["t_bc"] = 0.01         
# model_components["veldisp"] = 200. 
model_components["dust"] = dust
model_components["nebular"] = nebular


M_UNIT = 10**10
M_STAR = SNAP.Attribute.MassTable()[4] * M_UNIT
for i,a in enumerate(age):
    burst={}
    burst["massformed"] = numpy.log10(M_STAR) 
    burst["metallicity"] = 0.1# metallicity[i]
    burst["age"] = age[i]/1e9
    model_components["burst"+str(i+1)]=burst

model = pipes.model_galaxy(model_components, filt_list=goodss_filt_list,spec_wavs=numpy.logspace(3.5,4.5,10000))


sfh_fig,sfh_ax = model.sfh.plot(show=False)

xdata=sfh_ax.lines[0].get_xdata()
ydata=sfh_ax.lines[0].get_ydata()

plt.plot(xdata,ydata)
# plt.yscale('log')


plt.show()
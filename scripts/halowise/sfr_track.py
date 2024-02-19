import galspec
import numpy
import matplotlib.pyplot as plt



# --- SIMS
BOX         = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640/")
PARTBOX     = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/L50N640/")

# --- FLAGS : Set flags
SNAP_NUM    = 36
SAVE_PATH   = "/mnt/home/student/cranit/Work/RSGBank/Results/sfr_trackback.png" 
HALO_OFFSET = 1


# --- AUTO-FLAGS
COSMOLOGY   = BOX.GetCosmology("MassFunctionLitrature")
SNAP        = BOX.RSG(SNAP_NUM)
REDSHIFT    = (1/SNAP.Attribute.Time())-1
HUBBLE      = SNAP.Attribute.HubbleParam() * 100
OMEGA_M     = SNAP.Attribute.Omega0()
CMBT        = SNAP.Attribute.CMBTemperature()
MASSTABLE   = SNAP.Attribute.MassTable() * 1e10


# --- REORDER
ORDER       = numpy.argsort(SNAP.RKSGroups.VirialMass())[::-1]    # Reorders as decreasing mass

# TARGET HALO FEILDS
TIHID       = SNAP.RKSGroups.InternalHaloID()[ORDER][HALO_OFFSET]
VMASS       = SNAP.RKSGroups.VirialMass()[ORDER][HALO_OFFSET]

VNUM        = SNAP.RKSGroups.LengthByTypeInRvirWC()[ORDER][HALO_OFFSET]
STAR        = VNUM[4] * MASSTABLE[4]


# FILTER PARTICLE ROWS
GAS_IHIDS   = BOX.RSG(SNAP_NUM).Gas.InternalHaloID()


# --- GET PARTICLE ID FILTERING FOR TARGET
TGAS_IDS    = SNAP.Gas.ID()[GAS_IHIDS==TIHID]



# GET
TRACK_BACK_SNAP_NUM = [36,30,24,20,16]
TBSFR =[]
TBZ   =[]
for sn in TRACK_BACK_SNAP_NUM:
    PSNAP       = PARTBOX.PART(sn)
    GAS_IDS     = PSNAP.Gas.ID()
    TMASK       = numpy.isin(numpy.int64(GAS_IDS),numpy.int64(TGAS_IDS))

    TSFRs       = PSNAP.Gas.StarFormationRate()[TMASK] 
    TSFR         = numpy.sum(TSFRs)
    TBSFR.append(TSFR)
    TBZ.append((1/PSNAP.Header.Time())-1)





# Store for bagpipes
from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=HUBBLE, Om0=OMEGA_M, Tcmb0=CMBT)
def get_age(redshift):
    ages = [(cosmo.age(z)).value for z in redshift]
    return numpy.array(ages)

AGES = get_age(TBZ)*1e9

T_OBS = get_age([REDSHIFT])*1e9

AGES = T_OBS - AGES


numpy.savetxt("sfh.txt",numpy.column_stack((AGES,TBSFR)),fmt="%f %f",header="M*" + str(numpy.log10(STAR)))
# print(AGES)


# PLOT
plt.plot(AGES,TBSFR,'.-',ms=2)





# --- BEAUTIFY
# plt.xscale('log')
# plt.yscale('log')
# plt.xlabel("Density (??)")
# plt.ylabel("Temperature (K)")
# plt.axhline(100,ls='--',lw=1,color='k')
# plt.axhline(10000,ls='--',lw=1,color='k')

# plt.title("L=50Mpc , N=$640^3$ , z=8 , $\\text{N}_{\\text{min}}^{\\text{halo}}=50$ , HID=" + str(TIHID) + " , $\\text{N}_{\\text{gas}}^{\\text{halo}}=$" + str(len(TEMP)),pad=10)


# --- SAVE
plt.show()
# plt.savefig(SAVE_PATH,dpi=200)
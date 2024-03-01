import galspec
import numpy,os
import matplotlib.pyplot as plt
from astropy.cosmology import FlatLambdaCDM


# --- SIMS
CFG     = galspec.RockstarCFG("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640/")
BOX     = galspec.NavigationRoot(CFG.OUTBASE)
LBOX    = galspec.NavigationRoot(CFG.INBASE)

# --- FLAGS : Set flags
TSNAP_NUM   = 36    # Target snap num from which we will back track
SAVE_PATH   = "/mnt/home/student/cranit/Work/RSGBank/TBSFR_Bank" 
NUM_HALO    = 100   # Number of halos to track

# Must be in desending order, like [25,20,15]
TRACK_BACK_SNAP_NUMS = numpy.arange(36,15,-1).tolist()

# --- AUTO-FLAGS
TSNAP       = BOX.RSG(TSNAP_NUM)
TREDSHIFT    = (1/TSNAP.Attribute.Time())-1
HUBBLE      = TSNAP.Attribute.HubbleParam() * 100
OMEGA_M     = TSNAP.Attribute.Omega0()
CMBT        = TSNAP.Attribute.CMBTemperature()
MUNIT       = 1e10
MASSTABLE   = TSNAP.Attribute.MassTable()
COSMOLOGY   = FlatLambdaCDM(H0=HUBBLE, Om0=OMEGA_M, Tcmb0=CMBT)


# Find redshifts and age only once
tracked_redshift   = numpy.empty(len(TRACK_BACK_SNAP_NUMS))
tracked_age        = numpy.empty(len(TRACK_BACK_SNAP_NUMS))
tracked_lbage      = numpy.empty(len(TRACK_BACK_SNAP_NUMS))
for i,snap_num in enumerate(TRACK_BACK_SNAP_NUMS):
    PSNAP           = LBOX.PART(snap_num)
    tracked_redshift[i] = (1/PSNAP.Header.Time())-1

# Redshift to lookbackage as bagpipes want
def get_ages(redshifts):
    return numpy.array([(COSMOLOGY.age(z)).value for z in redshifts])

tracked_age     = get_ages(tracked_redshift)*1e9
target_age      = get_ages([TREDSHIFT])*1e9
tracked_lbage   = target_age - tracked_age



# --- MASS SORT
ORDER       = numpy.argsort(TSNAP.RKSGroups.VirialMass())[::-1]    # Reorders as decreasing mass

def TrackBack_TargetHaloSFR_OffsetBy(offset):
    # TARGET HALO FEILDS
    RKS                     = TSNAP.RKSGroups
    target_ihid             = RKS.InternalHaloID()[ORDER][offset]
    target_virial_mass      = RKS.VirialMass()[ORDER][offset]
    target_type_mass        = RKS.MassByTypeInRvirWC()[ORDER][offset]
    target_gas_mass         = target_type_mass[0] * MUNIT
    target_stellar_mass_formed = target_type_mass[4] * MUNIT

    # Filter target particle rows
    gas_ihids       = TSNAP.Gas.InternalHaloID()
    target_gas_ids  = TSNAP.Gas.ID()[gas_ihids==target_ihid]

    tracked_SFR = numpy.empty(len(TRACK_BACK_SNAP_NUMS))
    for i,snap_num in enumerate(TRACK_BACK_SNAP_NUMS):
        PSNAP           = LBOX.PART(snap_num)
        gas_ids         = PSNAP.Gas.ID()
        target_mask     = numpy.isin(numpy.int64(gas_ids),numpy.int64(target_gas_ids))
        tracked_SFR[i]  = numpy.sum(PSNAP.Gas.StarFormationRate()[target_mask])
        
    # Save 
    numpy.savetxt(os.path.join(SAVE_PATH,"off_"+str(offset)+".txt"),numpy.column_stack((tracked_lbage,tracked_SFR)),fmt="%f %f",header="M*" + str(numpy.log10(target_stellar_mass_formed)))


# COMPUTE and DUMP
if False:
    for offset in range(NUM_HALO):
        print(offset+1,"/",NUM_HALO,end='',flush=True)
        TrackBack_TargetHaloSFR_OffsetBy(offset)
        print(": Done",flush=True)


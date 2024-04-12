import numpy, galspec
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')


# --- FLAGS
SNAP_NUM    = 17
HR_MASS     = numpy.logspace(7,13,100) # High resolution mass for litrature mass function plot


# --- SIMULATIONS
L50N640     = galspec.NavigationRoot("/mnt/home/student/cranit/Work/ResetRKSG/RSG_L10N64")

# --- AUTO-FLAGS
# Make sure cosmology in all simulations are same
COSMOLOGY   = L50N640.GetCosmology("MassFunctionLitrature")
SNAP        = L50N640.RSG(SNAP_NUM)
REDSHIFT    = (1/SNAP.Attribute.Time())-1



# --- SORT AS DECREASING MASS
VirialMass = SNAP.RKSGroups.VirialMass()
vm_sort = numpy.argsort(VirialMass)[::-1]
VirialMass = VirialMass[vm_sort]

select_offset = 3
print(len(SNAP.RKSGroups.HaloID()))


# --- FOCOUSED HALO PROPERTIES
IHID = SNAP.RKSGroups.InternalHaloID()[vm_sort][select_offset]
HPOS = SNAP.RKSGroups.Position()[vm_sort][select_offset]
RVIR = SNAP.RKSGroups.VirialRadius()[vm_sort][select_offset] / 1000 # Kpc to Mpc


# --- COUNT PARTICLES
# Returns number of occurance of "ihid" in list of particle ihid
from galspec.navigation.MPGADGET.RSG.RSG import _TempRSGPartDump as pt
def ReturnCount(ptype:pt,ihid):
    ihid_mask = (ptype.InternalHaloID()==ihid)
    pos = ptype.Position()[ihid_mask]
    rvir_mask = (numpy.linalg.norm(pos-HPOS,axis=1)<RVIR)
    ids = ptype.ID()[ihid_mask][rvir_mask]
    return len(ids)

N_GAS   = ReturnCount(SNAP.Gas,IHID)
N_DM    = ReturnCount(SNAP.DarkMatter,IHID)
N_STAR  = ReturnCount(SNAP.Star,IHID)
N_BH    = ReturnCount(SNAP.BlackHole,IHID)

# --- MASS FROM COUNT
# M_UNIT = 10**10
# M_GAS   = N_GAS     * SNAP.Attribute.MassTable()[0] * M_UNIT
# M_DM    = N_DM      * SNAP.Attribute.MassTable()[1] * M_UNIT
# M_STAR  = N_STAR    * SNAP.Attribute.MassTable()[4] * M_UNIT
# M_BH    = N_BH      * SNAP.Attribute.MassTable()[5] * M_UNIT

M_GAS   = N_GAS     * SNAP.Gas.Mass()[0]
M_DM    = N_DM      * SNAP.DarkMatter.Mass()[0]
M_STAR  = N_STAR    * SNAP.Star.Mass()[0]
M_BH    = N_BH      * SNAP.BlackHole.Mass()[0]

M_TOTAL = M_GAS + M_DM + M_STAR + M_BH
 

print("-----")
print(N_GAS,N_DM,N_STAR,N_BH)

print("\nVirial Mass : ",VirialMass[select_offset])
print("Total Mass : ",M_TOTAL)
print("Ratio : ",  M_TOTAL / VirialMass[select_offset])

# print(len(SNAP.RKSGroups.HaloID()))

# --- SIMULATION MASS FUNCTIONS




# --- PLOT ENHANCE
# plt.xscale('log')
# plt.yscale('log')
# plt.legend()
# plt.xlabel("Mass $(M/M_\odot)$")

# plt.savefig("/mnt/home/student/cranit/Work/ResetRKSG/Result/check_mass_function.png",dpi=200)


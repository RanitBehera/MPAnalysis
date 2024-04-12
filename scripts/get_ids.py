import numpy
import galspec

BOX = galspec.NavigationRoot("/scratch/cranit/RSGBank/OUT_L50N640")

# Feed Group data from "RSG_000/RKSGroups"
G_IHIDs = BOX.RSG(36).RKSGroups.InternalHaloID()  # InternalHaloID
M_VIR_SORT = numpy.argsort(BOX.RSG(36).RKSGroups.VirialMass())[::-1] 
G_IHIDs = G_IHIDs[M_VIR_SORT]

# Feed Particle data from "RSG_000/0,1,4,5"
P_IHIDs = BOX.RSG(36).Gas.InternalHaloID() # InternalHaloID
P_IDs   = BOX.RSG(36).Gas.ID() # ID

# This function will return all the particle ids associated with a halo
def GetIds(IHID):
    if IHID not in G_IHIDs:return ValueError(f"Invalid Internal Halo ID {IHID}")
    if IHID not in P_IHIDs:return RuntimeError(f"No Particles associated with Internal Halo ID {IHID}.")
    mask = (P_IHIDs==IHID)
    return P_IDs[mask]

offset=9
print(len(GetIds(G_IHIDs[offset])))

print(BOX.RSG(36).RKSGroups.LengthByTypeWC()[M_VIR_SORT][offset][0])
import sys, os, numpy

sys.path.append(os.getcwd())
import modules as mp

# --- CONFIG PARAMETERS
OUTPUTDIR               = "/home/ranitbehera/MyDrive/Data/RKS_NEW/rks/output2/"
HALO_FILENAME           = "halos_0.0.ascii"
PARTICLE_FILENAME       = "halos_0.0.particles"
EHID                    = 2088
EXCLUDE_SUBSTRUCTURES   = True

# --- DERIVED PARAMETRS
HFILEPATH               = OUTPUTDIR + os.sep + HALO_FILENAME
PFILEPATH               = OUTPUTDIR + os.sep + PARTICLE_FILENAME
op                      = mp.BaseDirectory("/home/ranitbehera/MyDrive/Data/MP-Gadget/L10N64/")
MASSTABLE               = op.PART(17).ReadAttribute().MassTable

# --- DATA BANK
halos                   = numpy.loadtxt(HFILEPATH)
particles               = numpy.loadtxt(PFILEPATH)

# --- FILTER
def Get_Number_of_Particles_in(EHID,type,exclude_sub=False):
    ehid_mask   = particles[:,mp.particles.external_haloid]==EHID
    type_mask   = particles[:,mp.particles.type]==type
    mask        = ehid_mask & type_mask
    if exclude_sub:
        ihids       = particles[ehid_mask,mp.particles.internal_haloid]
        ihid        = int(numpy.unique(ihids)[0])
        ihid_mask   = particles[:,mp.particles.assigned_internal_haloid]==ihid
        mask        = mask & ihid_mask
    return sum(mask)



N_DM    = Get_Number_of_Particles_in(EHID,0,EXCLUDE_SUBSTRUCTURES)
N_GAS   = Get_Number_of_Particles_in(EHID,1,EXCLUDE_SUBSTRUCTURES)
N_STAR  = Get_Number_of_Particles_in(EHID,2,EXCLUDE_SUBSTRUCTURES)
N_BH    = Get_Number_of_Particles_in(EHID,3,EXCLUDE_SUBSTRUCTURES)

M_DM    = N_DM * MASSTABLE[1]
M_GAS   = N_GAS * MASSTABLE[0]
M_STAR  = N_STAR * MASSTABLE[4]
M_BH    = N_BH * MASSTABLE[5]






print("Number of particles",end="")
if EXCLUDE_SUBSTRUCTURES:print("(Excluding Substructures)")
else: print("(Including Substructures)")
print("In external halo id :",str(EHID))
print("Number of Particles = ",int(halos[EHID,mp.ascii.num_p]))
print("Virial Mass = ",halos[EHID,mp.ascii.mvir]/1e10)
print("Bound Mass = ",halos[EHID,mp.ascii.mbound_vir]/1e10)
print("M200b Mass = ",halos[EHID,mp.ascii.m200b]/1e10)
print("M200c Mass = ",halos[EHID,mp.ascii.m200c]/1e10)


print("-------------------------------------------------------")
print("Type".ljust(8)   ,":","Number".ljust(12)     ,"x","Mass Fraction".ljust(16)  ,"=","Type Mass")
print("-------------------------------------------------------")
print("DM".ljust(8)     ,":",str(N_DM).ljust(12)    ,"x",str(MASSTABLE[1]).ljust(16),"=",numpy.round(M_DM,3))
print("GAS".ljust(8)    ,":",str(N_GAS).ljust(12)   ,"x",str(MASSTABLE[0]).ljust(16),"=",numpy.round(M_GAS,3))
print("STAR".ljust(8)   ,":",str(N_STAR).ljust(12)  ,"x",str(MASSTABLE[4]).ljust(16),"=",numpy.round(M_STAR,3))
print("BH".ljust(8)     ,":",str(N_BH).ljust(12)    ,"x",str(MASSTABLE[5]).ljust(16),"=",numpy.round(M_BH,3))
print("-------------------------------------------------------")
print("Total".ljust(8)  ,":",str(N_BH+N_GAS+N_STAR+N_DM).ljust(12)," ","".ljust(16) ,"=",numpy.round(sum((M_DM,M_GAS,M_STAR,M_BH)),3),end="\n\n")



print(N_DM*MASSTABLE[1]*1e10/halos[EHID,mp.ascii.mvir])
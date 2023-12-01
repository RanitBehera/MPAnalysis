import sys, os, numpy

sys.path.append(os.getcwd())
import modules as mp

# --- CONFIG PARAMETERS
# OUTPUTDIR               = "/home/ranitbehera/MyDrive/Work/RKSG_Benchmark_2/L50N640c/RKSG_036/"
OUTPUTDIR               = "/home/ranitbehera/MyDrive/Data/RKS_NEW/rks/output2/"
HALO_FILENAME           = "halos_0.0.ascii"
PARTICLE_FILENAME       = "halos_0.0.particles"
EHID                    = 221133
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

# Type 1

# def Get_Number_of_Particles_in(EHID,type,exclude_sub=False):
#     ehid_mask   = particles[:,mp.particles.external_haloid]==EHID
#     type_mask   = particles[:,mp.particles.type]==type
#     mask        = ehid_mask & type_mask
#     if exclude_sub:
#         ihids       = particles[ehid_mask,mp.particles.internal_haloid]
#         ihid        = int(numpy.unique(ihids)[0])
#         ihid_mask   = particles[:,mp.particles.assigned_internal_haloid]==ihid
#         mask        = mask & ihid_mask
#     return sum(mask)



# N_DM    = Get_Number_of_Particles_in(EHID,0,EXCLUDE_SUBSTRUCTURES)
# N_GAS   = Get_Number_of_Particles_in(EHID,1,EXCLUDE_SUBSTRUCTURES)
# N_STAR  = Get_Number_of_Particles_in(EHID,2,EXCLUDE_SUBSTRUCTURES)
# N_BH    = Get_Number_of_Particles_in(EHID,3,EXCLUDE_SUBSTRUCTURES)
# N_TOTAL = N_DM + N_GAS + N_STAR + N_BH

# M_DM    = N_DM * MASSTABLE[1]
# M_GAS   = N_GAS * MASSTABLE[0]
# M_STAR  = N_STAR * MASSTABLE[4]
# M_BH    = N_BH * MASSTABLE[5]

# M_TOTAL = M_DM + M_GAS + M_STAR + M_BH

# print("Number of particles",end="")
# if EXCLUDE_SUBSTRUCTURES:print("(Excluding Substructures)")
# else: print("(Including Substructures)")
# print("In external halo id :",str(EHID))
# print("Number of Particles = ",int(halos[EHID,mp.ascii.num_p]))
# print("Virial Mass = ",halos[EHID,mp.ascii.mvir]/1e10)
# print("Bound Mass = ",halos[EHID,mp.ascii.mbound_vir]/1e10)
# print("M200b Mass = ",halos[EHID,mp.ascii.m200b]/1e10)
# print("M200c Mass = ",halos[EHID,mp.ascii.m200c]/1e10)
# print("Virial Radius = ",halos[EHID,mp.ascii.rvir])


# print("-------------------------------------------------------")
# print("Type".ljust(8)   ,":","Number".ljust(12)     ,"x","Mass Fraction".ljust(16)  ,"=","Type Mass")
# print("-------------------------------------------------------")
# print("DM".ljust(8)     ,":",str(N_DM).ljust(12)    ,"x",str(MASSTABLE[1]).ljust(16),"=",numpy.round(M_DM,3))
# print("GAS".ljust(8)    ,":",str(N_GAS).ljust(12)   ,"x",str(MASSTABLE[0]).ljust(16),"=",numpy.round(M_GAS,3))
# print("STAR".ljust(8)   ,":",str(N_STAR).ljust(12)  ,"x",str(MASSTABLE[4]).ljust(16),"=",numpy.round(M_STAR,3))
# print("BH".ljust(8)     ,":",str(N_BH).ljust(12)    ,"x",str(MASSTABLE[5]).ljust(16),"=",numpy.round(M_BH,3))
# print("-------------------------------------------------------")
# print("Total".ljust(8)  ,":",str(N_TOTAL).ljust(12)," ","".ljust(16) ,"=",numpy.round(M_TOTAL,3))
# print("".ljust(8)       ," ",str(N_TOTAL).ljust(12),"x",str(MASSTABLE[1]).ljust(16),"=",numpy.round(N_TOTAL*MASSTABLE[1],3),end="\n\n")


# Type 2

def Find_Sub_Of_EHID(EHID):
    ehid_mask=(particles[:,mp.particles.external_haloid]==EHID)
    type0_mask=(particles[:,mp.particles.type]==0)

    mask=ehid_mask & type0_mask

    as_ihid=particles[mask,mp.particles.assigned_internal_haloid]

    u=numpy.unique(as_ihid)
    return u


def Find_Sub_Of_IHID(IHID):
    ihid_mask=(particles[:,mp.particles.internal_haloid]==IHID)
    type0_mask=(particles[:,mp.particles.type]==0)

    mask=ihid_mask & type0_mask

    as_ihid=particles[mask,mp.particles.assigned_internal_haloid]


    u=numpy.unique(as_ihid)
    self_mask=~(u==IHID)
    return u[self_mask]


def Find_Pure_Number_of(IHID):
    asihid_mask   = particles[:,mp.particles.assigned_internal_haloid]==IHID
    ihid_mask   = particles[:,mp.particles.internal_haloid]==IHID
    type_mask   = (particles[:,mp.particles.type]==0)
    mask        = asihid_mask & ihid_mask & type_mask
    
    return sum(mask)





def FindNum(IHID):
    num=0
    num+=Find_Pure_Number_of(IHID)
    subs=Find_Sub_Of_IHID(IHID)
    if len(subs)>0:
        for sub in subs:
            num+=FindNum(sub)
    return num


num=FindNum(7770)
mt=0.0248811

print(num*mt)



























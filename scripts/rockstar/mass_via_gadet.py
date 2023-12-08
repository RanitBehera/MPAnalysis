import sys, os, numpy

sys.path.append(os.getcwd())
import galspecold as mp

# --- CONFIG PARAMETERS
# OUTPUTDIR               = "/home/ranitbehera/MyDrive/Work/RKSG_Benchmark_2/L50N640c/RKSG_036/"
OUTPUTDIR               = "/home/ranitbehera/MyDrive/Data/RKS_NEW/rks/output2/"
HALO_FILENAME           = "halos_0.0.ascii"
PARTICLE_FILENAME       = "halos_0.0.particles"
EHID                    = 3972
EXCLUDE_SUBSTRUCTURES   = True

# --- DERIVED PARAMETRS
HFILEPATH               = OUTPUTDIR + os.sep + HALO_FILENAME
PFILEPATH               = OUTPUTDIR + os.sep + PARTICLE_FILENAME
op                      = mp.BaseDirectory("/home/ranitbehera/MyDrive/Data/MP-Gadget/L10N64/")
MASSTABLE               = op.PART(17).ReadAttribute().MassTable

# --- DATA BANK
halos                   = numpy.loadtxt(HFILEPATH)
particles               = numpy.loadtxt(PFILEPATH)

# if EXCLUDE_SUBSTRUCTURES:print("(Excluding Substructures)")
# else: print("(Including Substructures)")
print("External Halo ID".ljust(20)," : ",str(EHID),"\n")
print("Virial Mass".ljust(20)," : ",halos[EHID,mp.ascii.mvir]/1e10)
print("Bound Mass".ljust(20)," : ",halos[EHID,mp.ascii.mbound_vir]/1e10)
print("M200b Mass".ljust(20)," : ",halos[EHID,mp.ascii.m200b]/1e10)
print("M200c Mass".ljust(20)," : ",halos[EHID,mp.ascii.m200c]/1e10,"\n")
print("Virial Radius".ljust(20)," : ",numpy.round(halos[EHID,mp.ascii.rvir],2),"kpc\n")

# print("-------------------------------------------------\n")

# Filter particles
ehid_mask=(particles[:,mp.particles.external_haloid]==EHID)
ehid_parts_id=particles[ehid_mask,mp.particles.particle_id]

# These two lines make it unique
uni,uindex=numpy.unique(ehid_parts_id,return_index=True)
ids=ehid_parts_id[uindex]


type0_mask=(particles[ehid_mask,mp.particles.type][uindex]==0)
type1_mask=(particles[ehid_mask,mp.particles.type][uindex]==1)
type2_mask=(particles[ehid_mask,mp.particles.type][uindex]==2)
type3_mask=(particles[ehid_mask,mp.particles.type][uindex]==3)

h_cx=halos[EHID,mp.ascii.x]
h_cy=halos[EHID,mp.ascii.y]
h_cz=halos[EHID,mp.ascii.z]
h_rv=halos[EHID,mp.ascii.rvir]
def GetWithinMask(typemask):
    x=(particles[ehid_mask,mp.particles.x][uindex][typemask])-h_cx
    y=(particles[ehid_mask,mp.particles.y][uindex][typemask])-h_cy
    z=(particles[ehid_mask,mp.particles.z][uindex][typemask])-h_cz
    points=numpy.column_stack((x,y,z))
    within=numpy.linalg.norm(points,axis=1)*1000
    within_mask=(within<=h_rv)
    # print(within_mask)
    return within_mask

# print(sum(within_mask),"x",0.0248811,"=",sum(within_mask)*0.0248811,"\n")

# Check output of double unique fro single length of 1 to confirm
# uid,ucounts=numpy.unique(ids,return_counts=True)
# uucounts=numpy.unique(ucounts)
# print(uucounts)

ids0_within=particles[ehid_mask,mp.particles.particle_id][uindex][type0_mask][GetWithinMask(type0_mask)]
ids1_within=particles[ehid_mask,mp.particles.particle_id][uindex][type1_mask][GetWithinMask(type1_mask)]
ids2_within=particles[ehid_mask,mp.particles.particle_id][uindex][type2_mask][GetWithinMask(type2_mask)]
ids3_within=particles[ehid_mask,mp.particles.particle_id][uindex][type3_mask][GetWithinMask(type3_mask)]

#---------------------
op=mp.BaseDirectory("/home/ranitbehera/MyDrive/Data/MP-Gadget/L10N64/")
gad_ids0=op.PART(17).DarkMatter.ID.ReadValues()
gad_ids1=op.PART(17).Gas.ID.ReadValues()
gad_ids2=op.PART(17).Star.ID.ReadValues()
gad_ids3=op.PART(17).BlackHole.ID.ReadValues()

present0=numpy.in1d(gad_ids0,ids0_within)
present1=numpy.in1d(gad_ids1,ids1_within)
present2=numpy.in1d(gad_ids2,ids2_within)
present3=numpy.in1d(gad_ids3,ids3_within)

# u,c=numpy.unique(present0,return_counts=True)

gad_masses0=op.PART(17).DarkMatter.Mass.ReadValues()
gad_masses1=op.PART(17).Gas.Mass.ReadValues()
gad_masses2=op.PART(17).Star.Mass.ReadValues()
gad_masses3=op.PART(17).BlackHole.Mass.ReadValues()

filtered_mass0=gad_masses0[present0]
filtered_mass1=gad_masses1[present1]
filtered_mass2=gad_masses2[present2]
filtered_mass3=gad_masses3[present3]

dm_mass=(len(ids0_within)/len(filtered_mass0))*sum(filtered_mass0)
gas_mass=(len(ids1_within)/len(filtered_mass1))*sum(filtered_mass1)
star_mass=(len(ids2_within)/len(filtered_mass2))*sum(filtered_mass2)
bh_mass=(len(ids3_within)/len(filtered_mass3))*sum(filtered_mass3)
total_mass=dm_mass+gas_mass+star_mass+bh_mass

cell_width=16
print("Type".ljust(8),"Rockstar-UIDS".rjust(cell_width),"GADGET-IDS".rjust(cell_width),"Matched-IDS".rjust(cell_width),"Mass".rjust(cell_width))
print("----------------------------------------------------------------------------------------------")
print(str("DM").ljust(8),str(len(ids0_within)).rjust(cell_width),str(len(present0)).rjust(cell_width),str(len(filtered_mass0)).rjust(cell_width),str(round(dm_mass,3)).rjust(cell_width))
print(str("Gas").ljust(8),str(len(ids1_within)).rjust(cell_width),str(len(present1)).rjust(cell_width),str(len(filtered_mass1)).rjust(cell_width),str(round(gas_mass,3)).rjust(cell_width))
print(str("Star").ljust(8),str(len(ids2_within)).rjust(cell_width),str(len(present2)).rjust(cell_width),str(len(filtered_mass2)).rjust(cell_width),str(round(star_mass,3)).rjust(cell_width))
print(str("BH").ljust(8),str(len(ids3_within)).rjust(cell_width),str(len(present3)).rjust(cell_width),str(len(filtered_mass3)).rjust(cell_width),str(round(bh_mass,3)).rjust(cell_width))
print("---------------------------------------------------------------------------------------------")

print("Total Mass".ljust(20),":",round(total_mass,3))


#-----------------------------------------------------------------------
MASSTABLE               = op.PART(17).ReadAttribute().MassTable

N_DM    = len(ids0_within)
N_GAS   = len(ids1_within)
N_STAR  = len(ids2_within)
N_BH    = len(ids3_within)
N_TOTAL = N_DM + N_GAS + N_STAR + N_BH

M_DM    = N_DM * MASSTABLE[1]
M_GAS   = N_GAS * MASSTABLE[0]
M_STAR  = N_STAR * MASSTABLE[4]
M_BH    = N_BH * MASSTABLE[5]

M_TOTAL = M_DM + M_GAS + M_STAR + M_BH

print("-------------------------------------------------------")
print("Type".ljust(8)   ,":","Number".ljust(12)     ,"x","Mass Fraction".ljust(16)  ,"=","Type Mass")
print("-------------------------------------------------------")
print("DM".ljust(8)     ,":",str(N_DM).ljust(12)    ,"x",str(MASSTABLE[1]).ljust(16),"=",numpy.round(M_DM,3))
print("GAS".ljust(8)    ,":",str(N_GAS).ljust(12)   ,"x",str(MASSTABLE[0]).ljust(16),"=",numpy.round(M_GAS,3))
print("STAR".ljust(8)   ,":",str(N_STAR).ljust(12)  ,"x",str(MASSTABLE[4]).ljust(16),"=",numpy.round(M_STAR,3))
print("BH".ljust(8)     ,":",str(N_BH).ljust(12)    ,"x",str(MASSTABLE[5]).ljust(16),"=",numpy.round(M_BH,3))
print("-------------------------------------------------------")
print("Total".ljust(8)  ,":",str(N_TOTAL).ljust(12)," ","".ljust(16) ,"=",numpy.round(M_TOTAL,3),end="\n\n")




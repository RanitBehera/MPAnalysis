import sys, os, numpy

sys.path.append(os.getcwd())
import modules as mp

# --- CONFIG PARAMETERS
OUTPUTDIR           = "/home/ranitbehera/MyDrive/Work/RKSG_Benchmark_2/L50N640c/RKSG_036/"
HALO_FILENAME       = "halos_0.0.ascii"
PARTICLE_FILENAME   = "halos_0.0.particles"
LIST_LENGTH         = 10

# --- DERIVED PARAMETRS
HFILEPATH           = OUTPUTDIR + os.sep + HALO_FILENAME
PFILEPATH           = OUTPUTDIR + os.sep + PARTICLE_FILENAME
DEFAULT_PRINT_NEXT  = False
PRINT_NEXT          = DEFAULT_PRINT_NEXT

# --- DATA BANK
halos               = numpy.loadtxt(HFILEPATH)
particles         = numpy.loadtxt(PFILEPATH)

# --- FILTERS
def Filter(field,n,descending=True):
    fdata   = halos[:,field]
    idsort  = numpy.argsort(fdata)
    if descending: idsort=idsort[::-1]
    id      = halos[:,mp.ascii.id][idsort]
    print( list(numpy.int64(id[0:n])),end="\n\n")






# --- PRINTING

PRINT_NEXT = True
if PRINT_NEXT:
    print("Most massive Halos : ","mvir")
    Filter(mp.ascii.mvir,LIST_LENGTH)
    PRINT_NEXT = DEFAULT_PRINT_NEXT


# PRINT_NEXT = True
if PRINT_NEXT:
    print("Most populated Halos : ","num_p")
    Filter(mp.ascii.num_p,LIST_LENGTH)
    PRINT_NEXT = DEFAULT_PRINT_NEXT

# subhaloof=2088
# ehid=particles[:,mp.particles.external_haloid]
# ashid=particles[:,mp.particles.assigned_internal_haloid][ehid==subhaloof]
# u,c=numpy.unique(ashid,return_counts=True)
# sorted_id=numpy.argsort(c)[::-1]
# sorted_u=u[sorted_id]

# print(list(numpy.int64(sorted_u[:10])))



import sys, os, numpy

sys.path.append(os.getcwd())
import galspec as mp

# --- CONFIG PARAMETERS
OUTPUTDIR           = "/home/ranitbehera/MyDrive/Data/RKS_NEW/rks/output2/"
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
    id      = halos[:,mp.ascii0.id][idsort]
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




import sys, os, numpy

sys.path.append(os.getcwd())
import modules as mp

# --- CONFIG PARAMETERS
OUTPUTDIR   = "/home/ranitbehera/MyDrive/Data/RKS_NEW/rks/output2"
HALO_FILENAME       = "halos_0.0.ascii"
PARTICLE_FILENAME   = "halos_0.0.particles"


# --- DERIVED PARAMETRS
HALO_FILEPATH       = OUTPUTDIR + os.sep + HALO_FILENAME
PARTICLE_FILEPATH   = OUTPUTDIR + os.sep + PARTICLE_FILENAME

# --- DATA BANK
halos               = numpy.loadtxt(HALO_FILEPATH)
# particles   = numpy.loadtxt(PARTICLE_FILEPATH)

# --- LINK
mvir = halos[:,mp.ascii.mvir]
num_p= halos[:,mp.ascii.num_p]

# --- FILTERS
def Filter(data,fieldname,n=10,desending=True):
    id=halos[:,mp.ascii.id]
    sorted=numpy.unique(numpy.sort(data))
    if desending: sorted=sorted[::-1]
    print("Sorted by : " + fieldname, end="")
    if desending: print("(desending)")
    else: print("(acsending)")

    print("ID : ",end="")
    for i in range(n):
        print(int(id[numpy.where(data==sorted[i])][0]),end="")
        if not i==n-1:print(" - ",end="")

    print("")
    print("")


print("Most massive Halos")
Filter(mvir,"mvir",10)

print("Least massive Halos")
Filter(mvir,"mvir",10,False)

print("Most populated Halos")
Filter(num_p,"num_p",10)

print("Least populated Halos")
Filter(num_p,"num_p",10,False)
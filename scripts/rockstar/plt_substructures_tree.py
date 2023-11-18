import sys,os, numpy, open3d

sys.path.append(os.getcwd())
import modules as mp

# --- CONFIG PARAMETERS
OUTPUTDIR               = "/home/ranitbehera/MyDrive/Data/RKS_NEW/rks/output2"
HALO_FILENAME           = "halos_0.0.ascii"
PARTICLES_FILENAME      = "halos_0.0.particles"
FOCUS_EHID              = 2088  # most massive : 3972,2088,7444,6143,1250

# --- DERIVED PARAMETERS
HFILEPATH=OUTPUTDIR + os.sep + HALO_FILENAME
PFILEPATH=OUTPUTDIR + os.sep + PARTICLES_FILENAME

# --- DATA FILTERS
data=numpy.loadtxt(PFILEPATH)


# def GetAllSubsOfEHID()

ehid=numpy.int64(data[:,mp.particles.external_haloid])
ihid=numpy.int64(data[:,mp.particles.internal_haloid])
aihid=numpy.int64(data[:,mp.particles.assigned_internal_haloid])
types=numpy.int64(data[:,mp.particles.type])

# Filter by ehid
ids=numpy.arange(len(ehid))
filter1=(ehid==FOCUS_EHID)&(types==0)

f_aihid=aihid[filter1]
u,c=numpy.unique(f_aihid,return_counts=True)

print(u,c)


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

ehid=data[:,mp.particles.assigned_internal_haloid]
ehid=data[:,mp.particles.internal_haloid]
ehid=data[:,mp.particles.external_haloid]

# Filter by ehid
# Filter by part type
# find number of unique ihid with count and index and create numpy structures to fill
# Filter by ihid==aihid for particles which are not in substructures
# Filter by ihid!=aihid for particles which are in substructures
# Get all substractures particles which have common aihid
# Feed to open3d basic
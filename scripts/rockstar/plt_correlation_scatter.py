import os,sys,numpy
import matplotlib.pyplot as plt

sys.path.append(os.getcwd())
import galspec as mp

# --- CONFIG PARAMETRS
OUTPUTDIR           = "/home/ranitbehera/MyDrive/Data/RKS_NEW/rks/output2"
HALO_FILENAME       = "halos_0.0.ascii"
PARTICLE_FILENAME   = "halos_0.0.particles"
XCOLUMN             = mp.ascii.num_p
XLABLE              = "X"
YCOLUMN             = mp.ascii.mvir
YLABLE              = "Y"
LOGSCALE            = (1,1)
MARKERSIZE          = 4

# --- DERIVED PARAMETRS
HALO_FILEPATH       = OUTPUTDIR + os.sep + HALO_FILENAME
PARTICLE_FILEPATH   = OUTPUTDIR + os.sep + PARTICLE_FILENAME

# --- DATA BANK
halos       = numpy.loadtxt(HALO_FILEPATH)
# particles   = numpy.loadtxt(PARTICLE_FILEPATH)

# --- LINK
X   = halos[:,XCOLUMN]
Y   = halos[:,YCOLUMN]

# --- CORRELATION
R=numpy.corrcoef(numpy.row_stack((X,Y)))

# --- SCATTER PLOT
plt.plot(X,Y,'.k',ms=MARKERSIZE)
if LOGSCALE[0]:plt.xscale("log")
if LOGSCALE[1]:plt.yscale("log")
plt.title("Correlation Scatter Plot\nCorrelation : "+str(numpy.round(R[0,1],3)))
if not XLABLE=="":plt.xlabel(XLABLE)
if not YLABLE=="":plt.ylabel(YLABLE)
plt.show()
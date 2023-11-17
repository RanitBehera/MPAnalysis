import sys,os, numpy, open3d

sys.path.append(os.getcwd())
import modules as mp

# --- CONFIG PARAMETERS
OUTPUTDIR               = "/home/ranitbehera/MyDrive/Data/RKS_NEW/rks/output2"  # Output directory of rockstar where ".ascii" and ".particles" files are present.
HALO_FILENAME           = "halos_0.0.ascii"                                 # Name of ".ascii" files. Add ".ascii" extension.
PARTICLES_FILENAME      = "halos_0.0.particles"                                 # Name of ".particles" files. Add ".particles" extension.
FOCUSTO     = 2088  # most massive : 3972,2088,7444,6143,1250       # The "external_halo_id" to focus for child particles.
BGCOLOR     = [0,0,0]                                               # Render window background color 
DMCOLOR     = [1,0,1]                                               # Color of DM particle type
GASCOLOR    = [0,1,1]                                               # Color of Gas particle type
STARCOLOR   = [1,1,0]                                               # Color of Star particle type
BHCOLOR     = [1,0,0]                                               # Color of BH particle type


# --- DERIVED PARAMETERS
HFILEPATH=OUTPUTDIR + os.sep + HALO_FILENAME
PFILEPATH=OUTPUTDIR + os.sep + PARTICLES_FILENAME

# --- DATA FILTER
data=numpy.loadtxt(PFILEPATH)        
f_ehid=numpy.where(data[:,mp.particles.external_haloid]==FOCUSTO)               
def GetPositionOf(type):
    f_type=numpy.where(data[:,mp.particles.type][f_ehid]==type)              
    x=data[:,mp.particles.x][f_ehid][f_type]
    y=data[:,mp.particles.y][f_ehid][f_type]
    z=data[:,mp.particles.z][f_ehid][f_type]
    return numpy.column_stack((x,y,z))

datah=numpy.loadtxt(HFILEPATH)
halo_row=datah[FOCUSTO]
rvir=halo_row[mp.ascii.rvir]
x,y,z=halo_row[mp.ascii.x:mp.ascii.z+1]

h=0.697000
rvir/=1000*h


# --- OPEN3D :
win=mp.Open3DWindow()
win.SetBackgroundColor(BGCOLOR)
win.SetLookAt([x,y,z])

win.DarkMatter(GetPositionOf(0),[DMCOLOR])
win.Gas(GetPositionOf(1),[GASCOLOR])
win.Star(GetPositionOf(2),[STARCOLOR])
win.Blackhole(GetPositionOf(3),[BHCOLOR])

win.AddCircle([x,y,z],rvir)


win.Show()
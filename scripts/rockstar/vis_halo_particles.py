import sys,os, numpy

sys.path.append(os.getcwd())
import galspec as mp

# --- CONFIG PARAMETERS
OUTPUTDIR               = "/home/ranitbehera/MyDrive/Work/RKSG_Benchmark_2/L50N640c/RKSG_036/"
# OUTPUTDIR               = "/home/ranitbehera/MyDrive/Data/RKS_NEW/rks_640/RKS_036"
HALO_FILENAME           = "halos_0.0.ascii"
PARTICLES_FILENAME      = "halos_0.0.particles"
FOCUS_EHID              = 158292



# --- DERIVED PARAMETERS
HFILEPATH=OUTPUTDIR + os.sep + HALO_FILENAME
PFILEPATH=OUTPUTDIR + os.sep + PARTICLES_FILENAME

# --- DATA FILTER
data=numpy.loadtxt(PFILEPATH)        
ehid_mask=data[:,mp.particles.external_haloid]==FOCUS_EHID

def GetPositionOf(type):
    type_mask=data[:,mp.particles.type]==type
    mask=ehid_mask & type_mask              
    x=data[:,mp.particles.x][mask]
    y=data[:,mp.particles.y][mask]
    z=data[:,mp.particles.z][mask]
    return numpy.column_stack((x,y,z))

datah=numpy.loadtxt(HFILEPATH)
halo_row=datah[FOCUS_EHID]
rvir=halo_row[mp.ascii.rvir]
r200b=halo_row[mp.ascii.m200b]
x,y,z=halo_row[mp.ascii.x:mp.ascii.z+1]
J=halo_row[mp.ascii.Jx:mp.ascii.Jz+1]
J=numpy.array(J)
J=J/numpy.linalg.norm(J)
h=0.697000
rvir/=1000*h


# --- OPEN3D :
win=mp.Open3D.GADGET()
win.DarkMatter(GetPositionOf(0))
win.Gas(GetPositionOf(1))
win.Star(GetPositionOf(2))
win.Blackhole(GetPositionOf(3))

# win.AddLine((x,y,z),(x+2*rvir*J[0],y+2*rvir*J[1],z+2*rvir*J[2]))
# win.AddLine((x,y,z),(x-rvir*J[0],y-rvir*J[1],z-rvir*J[2]))
# win.SurroundSpehere(rvir,normal=J,location=[x,y,z],resolution=10)
# win.AddWireframeBox((0,0,0),(10,10,10))


win.Run()


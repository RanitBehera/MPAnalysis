import sys,os, numpy

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

# --- DATA FILTER
data=numpy.loadtxt(PFILEPATH)        
f_ehid=numpy.where(data[:,mp.particles.external_haloid]==FOCUS_EHID)               
def GetPositionOf(type):
    f_type=numpy.where(data[:,mp.particles.type][f_ehid]==type)              
    x=data[:,mp.particles.x][f_ehid][f_type]
    y=data[:,mp.particles.y][f_ehid][f_type]
    z=data[:,mp.particles.z][f_ehid][f_type]
    return numpy.column_stack((x,y,z))

datah=numpy.loadtxt(HFILEPATH)
halo_row=datah[FOCUS_EHID]
rvir=halo_row[mp.ascii.rvir]
r200b=halo_row[mp.ascii.m200b]
x,y,z=halo_row[mp.ascii.x:mp.ascii.z+1]
J=halo_row[mp.ascii.Jx:mp.ascii.Jz+1]
J=numpy.array(J)
# print(J)
J=J/numpy.linalg.norm(J)
# print(J)

# exit()


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
win.SurroundSpehere(rvir,normal=J,location=[x,y,z],resolution=10)
win.AddWireframeBox((0,0,0),(10,10,10))


win.Run()


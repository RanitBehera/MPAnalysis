import sys,os, numpy,colorsys

sys.path.append(os.getcwd())
import modules as mp

# --- CONFIG PARAMETERS
OUTPUTDIR               = "/home/ranitbehera/MyDrive/Data/RKS_NEW/rks/output2/"
# OUTPUTDIR               = "/home/ranitbehera/MyDrive/Data/RKS_NEW/rks_640/RKS_036/"
HALO_FILENAME           = "halos_0.0.ascii"
PARTICLES_FILENAME      = "halos_0.0.particles"
SHOW_BOX                = True
PART_TYPE               = 0
BOUND_TYPE              = 1 #-1:IGM, 0 : Both, 1: Not IGM (Halos)

# --- DERIVED PARAMETERS
HFILEPATH=OUTPUTDIR + os.sep + HALO_FILENAME
PFILEPATH=OUTPUTDIR + os.sep + PARTICLES_FILENAME
COLOR_IGM = [1,1,1]
COLOR_PART = [1,1,0]


# --- DATA FILTER
data=numpy.loadtxt(PFILEPATH)   
type_mask=(data[:,mp.particles.type]== PART_TYPE)
igm_mask=(data[:,mp.particles.external_haloid]== -1)

mask=[]
if BOUND_TYPE==-1:mask=type_mask & igm_mask
elif BOUND_TYPE==1:mask=type_mask & (~igm_mask)
else: mask=type_mask

x=data[mask,mp.particles.x]
y=data[mask,mp.particles.y]
z=data[mask,mp.particles.z]

# x=x[:int(len(x)/10)]
# y=y[:int(len(y)/10)]
# z=z[:int(len(z)/10)]

points=numpy.column_stack((x,y,z)) 
# --- Open3D
win=mp.Open3D.Basic()
win.SetBackgroundColor([0,0,0])
win.AddToPointCloudList("All",points,[1,1,1])

if SHOW_BOX:win.AddWireframeBox((0,0,0),(10,10,10))

win.Run()



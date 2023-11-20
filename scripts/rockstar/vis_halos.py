import sys,os, numpy,colorsys

sys.path.append(os.getcwd())
import modules as mp

# --- CONFIG PARAMETERS
OUTPUTDIR               = "/home/ranitbehera/MyDrive/Data/RKS_NEW/rks/output2"
HALO_FILENAME           = "halos_0.0.ascii"
PARTICLES_FILENAME      = "halos_0.0.particles"
WHICH_ID                = mp.particles.internal_haloid
# SHOW_HIDs              = [3972,2088,7444,6143,1250]  # most massive : 3972,2088,7444,6143,1250
SHOW_HIDs                = [8481]#,8577,7569,8504]
TYPE                    = 0
SHOW_BOX                = False


# --- DERIVED PARAMETERS
HFILEPATH=OUTPUTDIR + os.sep + HALO_FILENAME
PFILEPATH=OUTPUTDIR + os.sep + PARTICLES_FILENAME

COLORS=[]
for hue in numpy.linspace(0,1,len(SHOW_HIDs)+1):
    COLORS.append(colorsys.hsv_to_rgb(hue,1,1))



# --- DATA FILTER
data=numpy.loadtxt(PFILEPATH)   
type_mask=(data[:,mp.particles.type]==TYPE)
halo_mask=numpy.in1d(data[:,WHICH_ID],SHOW_HIDs)
mask=type_mask & halo_mask
fdata=data[mask]

print(mask)

def GetPoints(extHID):
    hids=fdata[:,WHICH_ID]
    hid_mask=(hids==extHID)
    x=fdata[hid_mask,mp.particles.x]
    y=fdata[hid_mask,mp.particles.y]
    z=fdata[hid_mask,mp.particles.z]
    return numpy.column_stack((x,y,z))


# --- Open3D
win=mp.Open3D.Basic()
win.SetBackgroundColor([0,0,0])

for i in range(len(SHOW_HIDs)):
    hid=SHOW_HIDs[i]
    points=GetPoints(hid)
    win.AddToPointCloudList("E"+str(hid),points,COLORS[i])

if SHOW_BOX:win.AddWireframeBox((0,0,0),(10,10,10))

win.Run()



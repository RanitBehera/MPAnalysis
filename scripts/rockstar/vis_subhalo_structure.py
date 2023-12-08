import sys,os, numpy,colorsys

sys.path.append(os.getcwd())
import galspec as mp

# --- CONFIG PARAMETERS
OUTPUTDIR               = "/home/ranitbehera/MyDrive/Data/RKS_NEW/rks/output2/"
# OUTPUTDIR               = "/home/ranitbehera/MyDrive/Data/RKS_NEW/rks_640/RKS_036"
HALO_FILENAME           = "halos_0.0.ascii"
PARTICLES_FILENAME      = "halos_0.0.particles"
WHICH_ID                = mp.particles.assigned_internal_haloid
SHOW_HIDs              = [7569,7762,7755,7631,7605,7251,6798,7622,6908,7770]
TYPE                    = 0
SHOW_BOX                = False


# --- DERIVED PARAMETERS
HFILEPATH=OUTPUTDIR + os.sep + HALO_FILENAME
PFILEPATH=OUTPUTDIR + os.sep + PARTICLES_FILENAME

COLORS=[]
for hue in numpy.linspace(0,1,len(SHOW_HIDs)+1): # Extra length as linspace includes both first and last element so that 0~360 in hue space which is issue
    COLORS.append(colorsys.hsv_to_rgb(hue,1,1))

COLORS[-2]=[0.5,0.5,0.5]

# COLORS =  [[1,1,1] for c in COLORS]


# --- DATA FILTER
data=numpy.loadtxt(PFILEPATH)   
type_mask=(data[:,mp.particles.type]==TYPE)
halo_mask=numpy.in1d(data[:,WHICH_ID],SHOW_HIDs)
mask=type_mask & halo_mask
fdata=data[mask]

# print(mask)

def GetPoints(HID):
    hids=fdata[:,WHICH_ID]
    hid_mask=(hids==HID)
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

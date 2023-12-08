import sys,os, numpy, open3d


sys.path.append(os.getcwd())
import galspec as mp

# --- CONFIG PARAMETERS
OUTPUTDIR               = "/home/ranitbehera/MyDrive/Data/RKS_NEW/rks/output2"
HALO_FILENAME           = "halos_0.0.ascii"
PARTICLES_FILENAME      = "halos_0.0.particles"
FOCUS_EHID     = 2088  # most massive : 3972,2088,7444,6143,1250       # The "external_halo_id" 
SNAPDIR     = "/home/ranitbehera/MyDrive/Data/MP-Gadget/L10N64/"


# --- DERIVED PARAMETERS
PARTICLE_FILEPATH = OUTPUTDIR + os.sep + PARTICLES_FILENAME

# --- DATA FILTER
data=numpy.loadtxt(PARTICLE_FILEPATH)        
f_ehid=numpy.where(data[:,mp.particles.external_haloid]==FOCUS_EHID)   

def GetPositionOf(type):
    f_type=numpy.where(data[:,mp.particles.type][f_ehid]==type)              
    x=data[:,mp.particles.x][f_ehid][f_type]
    y=data[:,mp.particles.y][f_ehid][f_type]
    z=data[:,mp.particles.z][f_ehid][f_type]
    return numpy.column_stack((x,y,z))

# --- GET TRACKS
track_type=2
f_type=numpy.where(data[:,mp.particles.type][f_ehid]==track_type)
f_ids=data[:,mp.particles.particle_id][f_ehid][f_type]


def GetTrack(track_id):
    # track_id=int(f_ids[0])
    track=[]
    op=mp.BaseDirectory(SNAPDIR)
    for snap in range(0,18):
        # starids=op.PART(snap).Star.ID.ReadValues()
        starids=op.PART(snap).BlackHole.ID.ReadValues()
        if len(starids)==0: continue

        if track_id in starids:
            id=numpy.where(starids==track_id)

            # pos=op.PART(snap).Star.Position.ReadValues()
            pos=op.PART(snap).BlackHole.Position.ReadValues()
            track.append(pos[id][0])
    track=numpy.array(track)
    track/=1000
    return track


# Not Relative to Galaxy
# Relative vs Absolute

# --- OPEN3d 
win=mp.Open3D.GADGET()
win.Star(GetPositionOf(2))
win.Blackhole(GetPositionOf(3))

for i in range(50):
    track_id=f_ids[i]
    track=GetTrack(track_id) 
    win.AddCurve(track,[1,0,0])

win.Run()





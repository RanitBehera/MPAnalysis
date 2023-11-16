import sys,os, numpy, open3d,colorsys

sys.path.append(os.getcwd())
import modules as mp

# --- CONFIG PARAMETERS
OUTPUTDIR           = "/home/ranitbehera/MyDrive/Data/RKS_NEW/rks/output2"  # Output directory of rockstar where ".ascii" and ".particles" files are present.
HALO_FILENAME       = "halos_0.0.ascii"                                     # Name of ".particles" files. Add ".particles" extension.
PARTICLE_FILENAME   = "halos_0.0.particles"                                 # Name of ".particles" files. Add ".particles" extension.
EHID,TYPE   = 12,9                                                  # Column number (0-based) of "external_halo_id", "type".
X,Y,Z       = 0,1,2                                                 # Column number (0-based) of "x", "y", "z".
VX,VY,VZ    = 3,4,5
MASS        = 6
FOCUSTO     = 1250  # most massive : 3972,2088,7444,6143,1250       # The "external_halo_id" to focus for child particles.
SHOWTYPE    = 1                                                     # Which particles types to render (dark-matter:0, gas:1, star:2, black-hole:3).
BGCOLOR     = [0,0,0]                                               # Render window background color 




# --- DERIVED PARAMETERS
HALO_FILEPATH=OUTPUTDIR + os.sep + HALO_FILENAME
PARTICLE_FILEPATH=OUTPUTDIR + os.sep + PARTICLE_FILENAME

# --- DATA BANK
halos=numpy.loadtxt(HALO_FILEPATH)
particles=numpy.loadtxt(PARTICLE_FILEPATH)

# --- DATA FILTER        
f_ehid=numpy.where(particles[:,EHID]==FOCUSTO)               
def GetPositionOf(type):
    f_type=numpy.where(particles[:,TYPE][f_ehid]==type)              
    x,y,z=particles[:,X][f_ehid][f_type],particles[:,Y][f_ehid][f_type],particles[:,Z][f_ehid][f_type]
    return numpy.column_stack((x,y,z))

# --- COLOR MATRIX
def GetColorMatrix(type):
    f_type=numpy.where(particles[:,TYPE][f_ehid]==type)              
    x,y,z=particles[:,X][f_ehid][f_type],particles[:,Y][f_ehid][f_type],particles[:,Z][f_ehid][f_type]
    vx,vy,vz=particles[:,VX][f_ehid][f_type],particles[:,VY][f_ehid][f_type],particles[:,VZ][f_ehid][f_type]
    mass=particles[:,MASS][f_ehid][f_type]

    L=numpy.zeros((len(mass),3))
    for i in range(len(mass)):
        r=[x[i],y[i],z[i]]
        v=[vx[i],vy[i],vz[i]]
        L[i]=mass[i]*numpy.cross(r,v)
        
    fto=numpy.where(halos[:,mp.ascii.id]==FOCUSTO)
    Jx=halos[:,mp.ascii.Jx][fto][0]
    Jy=halos[:,mp.ascii.Jy][fto][0]
    Jz=halos[:,mp.ascii.Jz][fto][0]

    J=numpy.asarray([Jx,Jy,Jz])

    def GetAngle(Ji,Li):
        # print(Ji)
        # print(Li)
        return numpy.dot(Ji,Li)/numpy.sqrt(numpy.dot(Ji,Ji)*numpy.dot(Li,Li))

    cost=numpy.zeros((len(mass),1))
    magf=numpy.zeros((len(mass),1))

    for i in range(len(mass)):
        cost[i]=GetAngle(J,L[i])
        magf[i]=numpy.sqrt(numpy.dot(L[i],L[i]))/numpy.sqrt(numpy.dot(J,J))
    
    angf=0.5*(cost+1)   # Normalised
    magf=magf/max(magf)


    colors=numpy.ones((len(mass),3))
    for i in range(len(mass)):
        # colors[i]=numpy.asarray([angf[i][0],0,1-angf[i][0]])
        rgb=numpy.asarray(colorsys.hsv_to_rgb(angf[i][0],magf[i][0],1))
        colors[i]=numpy.asarray(rgb)

    return colors

# --- OPEN3D : POINT CLOUD
vis = open3d.visualization.Visualizer()
vis.create_window()
vis.get_render_option().background_color = numpy.asarray(BGCOLOR)

def AddPointCloud(ptype):
    pcd = open3d.geometry.PointCloud()
    pcd.points = open3d.utility.Vector3dVector(GetPositionOf(ptype))
    # pcd.paint_uniform_color([1,1,1])
    # pcd.colors=open3d.utility.Vector3dVector(numpy.tile([1,1,1],(len(pos),1)))
    pcd.colors=open3d.utility.Vector3dVector(GetColorMatrix(ptype))
    GetColorMatrix(SHOWTYPE)
    vis.add_geometry(pcd)
    
AddPointCloud(SHOWTYPE)

vis.run()
vis.destroy_window()

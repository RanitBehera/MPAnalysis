import os, numpy, open3d

# --- CONFIG PARAMETERS
OUTPUTDIR   = "/home/ranitbehera/MyDrive/Data/RKS_NEW/rks/output2"  # Output directory of rockstar where ".ascii" and ".particles" files are present.
FILENAME    = "halos_0.0.particles"                                 # Name of ".particles" files. Add ".particles" extension.
EHID,TYPE   = 12,9                                                  # Column number (0-based) of "external_halo_id", "type".
X,Y,Z       = 0,1,2                                                 # Column number (0-based) of "x", "y", "z".
FOCUSTO     = 7444  # most massive : 3972,2088,7444,6143,1250       # The "external_halo_id" to focus for child particles.
SHOWTYPE    = (0,1,1,1)                                             # Whether to render the particles types (dark-matter, gas, star, black-hole).
BGCOLOR     = [0,0,0]                                               # Render window background color 
DMCOLOR     = [1,0,1]                                               # Color of DM particle type
GASCOLOR    = [0,1,1]                                               # Color of Gas particle type
STARCOLOR   = [1,1,0]                                               # Color of Star particle type
BHCOLOR     = [1,0,0]                                               # Color of BH particle type



# --- DERIVED PARAMETERS
FILEPATH=OUTPUTDIR + os.sep + FILENAME

# --- DATA FILTER
data=numpy.loadtxt(FILEPATH)        
f_ehid=numpy.where(data[:,EHID]==FOCUSTO)               
def GetPositionOf(type):
    f_type=numpy.where(data[:,TYPE][f_ehid]==type)              
    x,y,z=data[:,X][f_ehid][f_type],data[:,Y][f_ehid][f_type],data[:,Z][f_ehid][f_type]
    return numpy.column_stack((x,y,z))

# --- GET TRACKS



# --- OPEN3D
vis = open3d.visualization.Visualizer()
vis.create_window()
vis.get_render_option().background_color = numpy.asarray(BGCOLOR)

def AddPointCloud(ptype,pcolor):
    pcd = open3d.geometry.PointCloud()
    pcd.points = open3d.utility.Vector3dVector(GetPositionOf(ptype))
    # pcd.colors=o3d.utility.Vector3dVector(numpy.tile([1,1,1],(len(pos),1)))
    pcd.paint_uniform_color(pcolor)
    vis.add_geometry(pcd)
    
if SHOWTYPE[0]: AddPointCloud(0,DMCOLOR)
if SHOWTYPE[1]: AddPointCloud(1,GASCOLOR)
if SHOWTYPE[2]: AddPointCloud(2,STARCOLOR)
if SHOWTYPE[3]: AddPointCloud(3,BHCOLOR)




vis.run()
vis.destroy_window()

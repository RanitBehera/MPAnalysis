import numpy as np
import os
import open3d as o3d

bd="/home/ranitbehera/MyDrive/Data/RKS_NEW/rks/output2"
# fl="halos_PART_017.0.ascii"
fl="halos_0.0.particles"
file=bd+os.sep+fl

data=np.loadtxt(file)

gid=data[:,12]                                  
gp_fid=np.where(data[:,12]==3972)               # most massive : 3972,2088,7444,6143,1250 

def GetPos(type):
    x,y,z=data[:,0],data[:,1],data[:,2]
    type_fid=np.where(data[:,9][gp_fid]==type)              
    x=x[gp_fid][type_fid]
    y=y[gp_fid][type_fid]
    z=z[gp_fid][type_fid]
    return np.column_stack((x,y,z))



#-----------------------------------------------OPEN3D
vis = o3d.visualization.Visualizer()
vis.create_window()
vis.get_render_option().background_color = np.asarray([0, 0, 0])


def AddPointCloud(ptype,pcolor):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(GetPos(ptype))
    # pcd.colors=o3d.utility.Vector3dVector(np.tile([1,1,1],(len(pos),1)))
    pcd.paint_uniform_color(pcolor)
    vis.add_geometry(pcd)
    

# AddPointCloud(0,[1,0,1])
# AddPointCloud(1,[1,1,0])
AddPointCloud(2,[0,0,1])
AddPointCloud(3,[1,0,0])

# vis.get_view_control().set_lookat([6.222214,5.429032,1.932533])
# vis.get_view_control().set_zoom(10)
# vis.get_view_control().set_front(10)
# vis.get_view_control().set_up([0,1,0])

vis.run()
vis.destroy_window()

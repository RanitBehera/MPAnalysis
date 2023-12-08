import open3d as o3d
import numpy as np

import sys
sys.path.append("/home/ranitbehera/MyDrive/Repos/MPAnalysis/")
import galspec as mp





# op=mp.BaseDirectory("/home/ranitbehera/MyDrive/Data/Merger/L10N64/")
# op=mp.BaseDirectory("/home/ranitbehera/MyDrive/Data/MP-Gadget/L50N640/")
# pos=op.PIG(36).FOFGroups.MassCenterPosition.ReadValues()
# # pos=pos[0:int(len(pos)/100)]

# # point_cloud = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
# point_cloud = np.array(pos)


# pcd = o3d.geometry.PointCloud()
# pcd.points = o3d.utility.Vector3dVector(point_cloud)
# # pcd.color=
# pcd.paint_uniform_color([1,1,0])

# # o3d.visualization.draw_geometries([pcd])



# vis = o3d.visualization.Visualizer()
# # vis.create_window()
# vis.add_geometry(pcd)
# # vis.get_render_option().background_color = np.asarray([0, 0, 0])
# # vis.run()


# app=o3d.visualization.gui.Application.instance
# app

# app.create_window()
# app.add_window(vis)
# vis.run()


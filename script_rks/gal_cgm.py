import numpy as np
import os
import open3d as o3d

bd="/home/ranitbehera/MyDrive/Data/RKS_NEW/rks/output2"
# fl="halos_PART_017.0.ascii"
fl="halos_0.0.particles"
file=bd+os.sep+fl

data=np.loadtxt(file)

gid=data[:,12]                                  # Get associated halo
gp_fid=np.where(data[:,12]==3972)               # Filter for particles in halo 3972 (most massive)
stars_fid=np.where(data[:,9][gp_fid]==2)        # Filter for stars

x=data[:,0][gp_fid][stars_fid]
y=data[:,1][gp_fid][stars_fid]
z=data[:,2][gp_fid][stars_fid]






print(len(x))
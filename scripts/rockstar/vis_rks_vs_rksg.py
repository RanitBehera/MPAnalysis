import sys,os, numpy,colorsys

sys.path.append(os.getcwd())
import modules as mp



rks_path = "/home/ranitbehera/MyDrive/Work/RKSG_Benchmark_2/L50N640c/RKS_036/halos_0.0.particles"
rksg_path = "/home/ranitbehera/MyDrive/Work/RKSG_Benchmark_2/L50N640c/RKSG_036/halos_0.0.particles"

rks_data=numpy.loadtxt(rks_path)
rksg_data=numpy.loadtxt(rksg_path)

#filter1
mask=(rks_data[:,mp.particles0.internal_haloid]==rks_data[:,mp.particles0.assigned_internal_haloid])
x=rks_data[:,mp.particles0.x][mask]
y=rks_data[:,mp.particles0.y][mask]
z=rks_data[:,mp.particles0.z][mask]
points_rks=numpy.column_stack((x,y,z))

#filter2
mask=(rksg_data[:,mp.particles.internal_haloid]==rksg_data[:,mp.particles.assigned_internal_haloid])
type_mask=(rksg_data[:,mp.particles.type]==0)
mask=mask & type_mask
x=rksg_data[:,mp.particles.x][mask]
y=rksg_data[:,mp.particles.y][mask]
z=rksg_data[:,mp.particles.z][mask]
points_rksg=numpy.column_stack((x,y,z))







win=mp.Open3D.Basic()
win.SetBackgroundColor([0,0,0])

win.AddToPointCloudList("rks",points_rks,[0,1,0])
win.AddToPointCloudList("rksg",points_rksg,[1,0,0])

win.AddWireframeBox((0,0,0),(50,50,50))

win.Run()
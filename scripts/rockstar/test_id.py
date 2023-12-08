import sys,os, numpy,colorsys

sys.path.append(os.getcwd())
import galspec as mp



rks_path = "/home/ranitbehera/MyDrive/Work/RKSG_Benchmark_2/L50N640c/RKS_036/halos_0.0.particles"
rksg_path = "/home/ranitbehera/MyDrive/Work/RKSG_Benchmark_2/L50N640c/RKSG_036/halos_0.0.particles"
print("Loading data ...",end="")
rks_data=numpy.loadtxt(rks_path)
rksg_data=numpy.loadtxt(rksg_path)
print("Done")


gal_halo_mask=(rksg_data[:,mp.particles.external_haloid]==221133)
halo_part=rks_data[gal_halo_mask,mp.particles.particle_id]

print(list(halo_part))


print(list(halo_part))
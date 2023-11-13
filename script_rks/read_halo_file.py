import numpy as np
import os


bd="/home/ranitbehera/MyDrive/Data/RKS_NEW/rks/output2"
# fl="halos_PART_017.0.ascii"
fl="halos_0.0.ascii"
file=bd+os.sep+fl

data=np.loadtxt(file)

id = data[:,0]
num_p = data[:,1]
mvir = data[:,2]
# mbound_vir = data[:,3]
# rvir = data[:,4]
# vmax = data[:,5]
# rvmax = data[:,6]
# vrms = data[:,7]
# x = data[:,8]
# y = data[:,9]
# z = data[:,10]
# vx = data[:,11]
# vy = data[:,12]
# vz = data[:,13]
# Jx = data[:,14]
# Jy = data[:,15]
# Jz = data[:,16]
# E = data[:,17]
# Spin = data[:,18]
# PosUncertainty = data[:,19]
# VelUncertainty = data[:,20]
# bulk_vx = data[:,21]
# bulk_vy = data[:,22]
# bulk_vz = data[:,23]
# BulkVelUnc = data[:,24]
# n_core = data[:,25]
# m200b = data[:,26]
# m200c = data[:,27]
# m500c = data[:,28]
# m2500c = data[:,29]
# Xoff = data[:,30]
# Voff = data[:,31]
# spin_bullock = data[:,32]
# b_to_a = data[:,33]
# c_to_a = data[:,34]
# A[x] = data[:,35]
# A[y] = data[:,36]
# A[z] = data[:,37]
# b_to_a(500c) = data[:,38]
# c_to_a(500c) = data[:,39]
# A[x](500c) = data[:,40]
# A[y](500c) = data[:,41]
# A[z](500c) = data[:,42]
# Rs = data[:,43]
# Rs_Klypin = data[:,44]
# T/|U| = data[:,45]
# M_pe_Behroozi = data[:,46]
# M_pe_Diemer = data[:,47]
# Type = data[:,48]
# SM = data[:,49]
# Gas = data[:,50]
# BH = data[:,51]
# idx = data[:,52]
# i_so = data[:,53]
# i_ph = data[:,54]
# num_cp = data[:,55]
# mmetric = data[:,56]


# print(sum(num_p))
print(id[np.where(mvir==max(mvir))])
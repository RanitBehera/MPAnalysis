import matplotlib.pyplot as plt
import numpy

path="/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L10Mpc_N64c/txtfiles/sfr.txt"

sfr=numpy.loadtxt(path)

# print(sfr)

x=sfr[:,0]
y=sfr[:,1]

plt.plot(x,y,'.-',ms=1)
plt.yscale("log")
plt.savefig("/mnt/home/student/cranit/Work/RKSG_Benchmark/results/sfr/plot.png",dpi=200)
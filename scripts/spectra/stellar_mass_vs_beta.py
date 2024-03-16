import numpy
import matplotlib.pyplot as plt

data = numpy.loadtxt("/mnt/home/student/cranit/Repo/MPAnalysis/temp/UV_SLOPE/UV_slope_Av_00.txt")

beta=data[:,1]
sm=data[:,2]

plt.plot(sm,beta,'.')

plt.xscale('log')
plt.ylim(-4,1)
plt.xlim(1e6,1e12)

plt.show()
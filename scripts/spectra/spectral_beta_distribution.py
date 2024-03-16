import numpy
import matplotlib.pyplot as plt

file = "/mnt/home/student/cranit/Repo/MPAnalysis/temp/UV_SLOPE/UV_slope_Av_00.txt"

offset,beta = numpy.loadtxt(file).T

# beta=beta[:100]

plt.hist(beta,bins=30)
plt.xlim([-3,-2])
plt.xlabel("UV Slope $\\beta$")
plt.ylabel("Count")
plt.title("UV Slope Distribution")
plt.annotate("$A_V=0$\n$z=8$\n$N=$"+str(len(beta)),xy=(0,1),xycoords="axes fraction",va="top",ha="left",xytext=(5,-5),textcoords="offset pixels")

# plt.show()
plt.savefig("/mnt/home/student/cranit/Repo/MPAnalysis/temp/plots_mar9/UV_slope_dist.png",dpi=300)
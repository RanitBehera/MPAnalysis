import numpy
import matplotlib.pyplot as plt

offset,stellar_mass,sfr,beta,Luv = numpy.loadtxt("/mnt/home/student/cranit/Repo/MPAnalysis/temp/spectra/bagdata.txt").T


print(stellar_mass)
plt.plot(stellar_mass,beta,'.')


plt.ylim(-4,1)
plt.xlim(6,12)

plt.show()
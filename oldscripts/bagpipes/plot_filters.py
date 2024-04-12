import numpy
import matplotlib.pyplot as plt

PATH = "/mnt/home/student/cranit/Repo/MPAnalysis/oldscripts/bagpipes/filters/"

lists = ["f098m","f105w","f125w","f160w","f435w","f606w"]

for l in lists:
    x,y = numpy.loadtxt(PATH + l).T
    plt.plot(x,y)

plt.ylim([0,1])
plt.show()
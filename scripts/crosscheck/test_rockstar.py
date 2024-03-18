import numpy
import matplotlib.pyplot as plt
import galspec


rootpath = "/mnt/home/student/cranit/Work/RSGBench2"

rockstar = numpy.loadtxt("/mnt/home/student/cranit/Work/RSGBench2/rockstar_out/halos_PART_036.hdf5.0.ascii")
galaxy = numpy.loadtxt("/mnt/home/student/cranit/Work/RSGBench2/galaxy_out/halos_PART_036.hdf5.0.ascii")

galaxy_gad = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBench2/Check_Output/gadget_out")


mrockstar = rockstar[:,2]
mgalaxy = galaxy[:,2]
mgalaxygad = galaxy_gad.RSG(36).RKSGroups.VirialMass()


n,x,_=plt.hist(numpy.log10(mrockstar),bins=25,histtype='step',alpha=0.1)
bin_centers = 0.5*(x[1:]+x[:-1])
plt.plot(bin_centers,n,label="rockstar(hdf5)")
n,x,_=plt.hist(numpy.log10(mgalaxy),bins=25,histtype='step',alpha=0.1)
bin_centers = 0.5*(x[1:]+x[:-1])
plt.plot(bin_centers,n,label="galaxy(hdf5)")
n,x,_=plt.hist(numpy.log10(mgalaxygad),bins=25,histtype='step',alpha=0.1)
bin_centers = 0.5*(x[1:]+x[:-1])
plt.plot(bin_centers,n,label="galaxy(mp)")



plt.axvline(numpy.log10(32 * 0.00311013 * 1e10))

plt.legend()
plt.yscale('log')
plt.show()

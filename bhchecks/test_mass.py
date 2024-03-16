import numpy
import matplotlib.pyplot as plt
import galspec

box = galspec.NavigationRoot("/scratch/cranit/RSGBank/L50N640")
snap = box.RSG(50)
G_IHID = snap.RKSGroups.InternalHaloID()
G_MVIR = snap.RKSGroups.VirialMass()


tgid = 1


#particle
bh_ids = snap.BlackHole.ID()
bh_gids = snap.BlackHole.GroupID()
bh_pos = snap.BlackHole.Position() 
bh_mass = snap.BlackHole.BlackholeMass() 
mask = (bh_gids==tgid)
bh_pos = bh_pos[mask]
bh_mass = bh_mass[mask]*1e10


star_ids = snap.Star.ID()
star_gids = snap.Star.GroupID()
star_pos = snap.Star.Position() 
mask = (star_gids==tgid)
star_pos = star_pos[mask]

Gas_ids = snap.Gas.ID()
Gas_gids = snap.Gas.GroupID()
Gas_pos = snap.Gas.Position() 
mask = (Gas_gids==tgid)
Gas_pos = Gas_pos[mask]


si = numpy.int32(100*(bh_mass/numpy.max(bh_mass))**3)

print(len(si))

fig = plt.figure()
ax = fig.add_subplot(1,1,1,projection="3d")

X,Y,Z = bh_pos.T
print(si)
# plt.plot(X,Y,Z,'.b',ms=10)
ax.scatter(X,Y,Z,s=si)

X,Y,Z = star_pos.T
# plt.plot(X,Y,Z,'.y',alpha=0.3,ms=0.5)
ax.scatter(X,Y,Z,s=1,alpha=0.3,color="orange")

X,Y,Z = Gas_pos.T
# ax.scatter(X,Y,Z,s=0.1,alpha=0.3,color="y")

plt.show()


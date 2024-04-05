import numpy
import matplotlib.pyplot as plt

# MOCK POINTS
numpy.random.seed(0)
maj_rad=10
min_rad=2
# Wavy Torus skeleton
theta = numpy.random.random(1000)*2*numpy.pi
MX,MY = [maj_rad*numpy.cos(theta),maj_rad*numpy.sin(theta)]
MZ = 2 * numpy.sin(3*theta)
# Offset
mX,mY,mZ = min_rad*(numpy.random.normal(0,0.5,(1000,3)).T - 0.5)

X,Y,Z = [MX+mX,MY+mY,MZ+mZ]




fig=plt.figure()
ax = plt.axes(projection="3d")

ax.plot(X,Y,Z,'.',ms=2)
ax.set_xlim(-12,12)
ax.set_ylim(-12,12)
ax.set_zlim(-6,6)

plt.show()








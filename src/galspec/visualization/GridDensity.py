import numpy
import matplotlib.pyplot as plt
from typing import Literal



# def Grid3D(positions,X,Y,Z,dx,dy,dz):
#     Nx,Ny,Nz = numpy.int32(numpy.array([X,Y,Z])/numpy.array([dx,dy,dz]))
    


def GridDensity(ax:plt.Axes,width,height,boxsize,positions,sliceat,slicewidth):
    # grid = Grid3D(positions,boxsize,boxsize,boxsize,boxsize/width,boxsize/height,slicewidth)

    dx=boxsize/width
    dy=boxsize/height
    gx=numpy.int32(positions[:,0] / dx)
    gy=numpy.int32(positions[:,1] / dy)
    z = positions[:,2]/boxsize
    image = numpy.zeros((width,height))
    for n in range(len(positions)):
        zn=z[n]
        if not((sliceat-(slicewidth/2)<=zn) and (zn<=sliceat+(slicewidth/2))):continue
        i,j=gx[n],gy[n]
        image[i,j]+=1
    image = image/numpy.max(image)
    image = image**0.1
    ax.imshow(image)
    









# Debug
import galspec,os

BOX         = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640/")
PARTBOX     = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/L50N640/")


POS = BOX.RSG(36).DarkMatter.Position()


fig,ax = plt.subplots(1,1)

zs=numpy.linspace(0,1,100)
SAVE_PATH = "/mnt/home/student/cranit/Work/RSGBank/Results_2/frames"
for i,zc in enumerate(zs):
    GridDensity(ax,1000,1000,50,POS,zc,0.01)
    plt.savefig(SAVE_PATH + os.sep + "fr_"+str(i+1)+".png",dpi=300)
    print(i+1,"/",len(zs),"Done",flush=True)




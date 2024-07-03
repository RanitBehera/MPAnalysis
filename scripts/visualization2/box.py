import galspec
import matplotlib.pyplot as plt
from galspec.visualization.Matcube import PlotCube
import numpy
from scipy import spatial


BOX = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640")
LBOX = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/L50N640")

BOX = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L10N64")
LBOX = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/L10N64/output")
BOXSIZE = LBOX.PART(17).Attribute.BoxSize()

MODE = "2D"



# Relavant Position
fof_halos = LBOX.PIG(36).FOFGroups.MassCenterPosition()
rks_halos =  BOX.RSG(36).RKSGroups.Position() * 1000 # Mpc to Kpc


# Link
pos = rks_halos

# Plot
if MODE == "3D":
    fig = plt.figure(figsize=(8,8))
    ax = plt.axes(projection="3d")
    PlotCube(ax,pos,BOXSIZE,1,'k',0.1)
else:
    slice_at = 0.5
    slice_thickness = 0.02

    slice_at *= BOXSIZE
    slice_thickness /= 2
    slice_thickness *= BOXSIZE

    img_width = 1000
    img_heigh = 1000

    img = numpy.empty((img_width,img_heigh))

    dx = BOXSIZE/img_width
    dy = BOXSIZE/img_heigh



    h=slice_thickness
    def CubicSpline(q):
        sigma_2=10/(7*numpy.pi*(h**2))
        sigma_3 = 1 / (numpy.pi*(h**2))
        mask01 = (0<=q)&(q<=1)
        mask12 = (1<q)&(q<=2)
        mask2_ = (2<q)
        k01 = sigma_2 * (1-(1.5*(q**2)*(1-(q/2))))
        k12 = (sigma_2/4) * ((2-q)**3)
        k2_ = 0
        k=k01*mask01 + k12*mask12 #+ k2_ * mask2_
        return k

    kdt = spatial.cKDTree(pos)
    cx=0
    while cx<BOXSIZE:
        cy=0
        while cy<BOXSIZE:
            neighbours_index=kdt.query_ball_point([cx,cy,slice_at],2*h)
            neighbours = kdt.data[neighbours_index]
            n= neighbours
            q = numpy.sqrt(numpy.power(n[:,0]-cx,2)+numpy.power(n[:,1]-cy,2))/h
            density = numpy.sum(CubicSpline(q))
            img[int(cx/dx),int(cy/dy)]=density
            cy+=dy
        cx+=dx

    plt.imshow(img)
        


plt.show()






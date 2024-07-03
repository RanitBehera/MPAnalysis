import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

# --- PARTICLES
numpy.random.seed(10)
N=100
L=10
X = numpy.random.random(N)*L
Y = numpy.random.random(N)*L
Z = numpy.random.random(N)*L
C= numpy.array(list(zip(X,Y,Z)))


# --- FLAGS
h = 1 # smoothing length
STEP = 0.1

# --- AUTO-FLAGS
# Original Bounds
# OBX = [min(X),max(X)]
# OBY = [min(Y),max(Y)]
# OBZ = [min(Z),max(Z)]
OBX = [0,L]
OBY = [0,L]
OBZ = [0,L]
# Extended Bounds
EBX = OBX + 2*h * numpy.array([-1,1])
EBY = OBY + 2*h * numpy.array([-1,1])
EBZ = OBZ + 2*h * numpy.array([-1,1])
# Image Dimensions
DX = numpy.int32((EBX[1]-EBX[0])/STEP)
DY = numpy.int32((EBY[1]-EBY[0])/STEP)
DZ = numpy.int32((EBZ[1]-EBZ[0])/STEP)


# --- DESNITY MAP
density  = numpy.zeros((DX,DY))

# Kernel at orgin
def CubicSpline(q):
    sigma_2=10/(7*numpy.pi*(h**2))
    mask01 = (0<=q)&(q<=1)
    mask12 = (1<q)&(q<=2)
    mask2_ = (2<q)
    k01 = sigma_2 * (1-(1.5*(q**2)*(1-(q/2))))
    k12 = (sigma_2/4) * ((2-q)**3)
    k2_ = 0
    k=k01*mask01 + k12*mask12 #+ k2_ * mask2_
    return k


def FullKernelatOrgin(h):
    rx=numpy.arange(-2*h,2*h,STEP)
    ry=numpy.arange(-2*h,2*h,STEP)
    RX,RY = numpy.meshgrid(rx,ry)
    q = numpy.sqrt(numpy.power(RX,2)+numpy.power(RY,2))/h
    k = CubicSpline(q)
    return RX,RY,k

rx,ry,k=FullKernelatOrgin(h)



def XC_2_Index(xc):return numpy.int32(( (xc-EBX[0])/(EBX[1]-EBX[0]) ) * DX)
def YC_2_Index(yc):return numpy.int32(( (yc-EBX[0])/(EBX[1]-EBX[0]) ) * DX)

for ci in C:
    px = ci[0]+rx
    py = ci[1]+ry
    pi = XC_2_Index(px)
    pj = YC_2_Index(py)
    density[pi,pj] += k



# --- SIGHTLINE
# create points to stop and scan for particles
scan_from = [2,5]
scan_to = [8,8]
scan_N = 100
stop_X = numpy.linspace(scan_from[0],scan_to[0],scan_N)
stop_Y = numpy.linspace(scan_from[1],scan_to[1],scan_N)
stops = numpy.array(list(zip(stop_X,stop_Y)))

# --- Curved line
theta = numpy.linspace(0,4*numpy.pi,scan_N)
cstop_X = 5 + 0.2 * theta * numpy.cos(theta)
cstop_Y = 5 + 0.2 * theta * numpy.sin(theta)
cstops = numpy.array(list(zip(cstop_X,cstop_Y)))


# create kd tree to quickly look for nearest particles
from scipy import spatial
kdt = spatial.cKDTree(C[:,0:2])
def ProbeDensity(stops):
    density = numpy.zeros(len(stops))
    for i,stop in enumerate(stops):
        neighbours_index=kdt.query_ball_point(stop,2*h)
        neighbours = kdt.data[neighbours_index]
        n= neighbours
        q = numpy.sqrt(numpy.power(n[:,0]-stop[0],2)+numpy.power(n[:,1]-stop[1],2))/h
        density[i] = numpy.sum(CubicSpline(q))
    return density



def ShowDensity(stops,color,frc=scan_N):
    # mask for animation
    stops = stops[:frc]

    density = ProbeDensity(stops)
    ax[0].plot(stops[:,0],stops[:,1],'-',ms=2,lw=1,c=color)
    ax[0].plot(stops[0,0],stops[0,1],'xk',ms=5)
    # ax[0].plot(stops[-1,0],stops[-1,1],'',ms=5)
    ax[1].plot(density,c=color)


# ShowDensity(stops,'b')
# ShowDensity(cstops,'g')
# # --- BEAUTIFICATION
# ax[0].set_xlim(OBX[0],OBX[1]-STEP)
# ax[0].set_ylim(OBY[0],OBY[1]-STEP)
# # plt.show()


# Animation Frames
frc=0
while frc<=scan_N:
    print("Frame",frc,": ",end="",flush=True)

    fig,ax=plt.subplots(1,2,figsize=(16,8))

    ax[0].plot(X,Y,'.r',ms=2)

    im=ax[0].imshow(density.T,extent=numpy.array(numpy.array([EBX,EBY]).flatten())-STEP/2,origin="lower",cmap="Greys")
    divider = make_axes_locatable(ax[0])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    plt.colorbar(im,cax)



    frc+=1
    ShowDensity(stops,'b',frc)
    ShowDensity(cstops,'g',frc)
    # --- BEAUTIFICATION
    ax[0].set_xlim(OBX[0],OBX[1]-STEP)
    ax[0].set_ylim(OBY[0],OBY[1]-STEP)
    ax[1].set_ylim(0,numpy.max(density)*1.5)
    plt.savefig(f"/mnt/home/student/cranit/Repo/MPAnalysis/temp/anim/sph_dens_prob_2d/fr_{frc}.png",dpi=300)
    plt.close()
    print("Done",flush=True)


import galspec
import numpy
import matplotlib.pyplot as plt
from galspec.visualization.Matcube import PlotCube
from scipy import spatial

# --- SIMS
BOX         = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640")
PARTBOX     = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/L50N640")

# --- FLAGS : Set flags
SNAP_NUM    = 36
HALO_OFFSET = 1
WITHIN_RVIR  = True

# --- AUTO-FLAGS
COSMOLOGY   = BOX.GetCosmology("MassFunctionLitrature")
SNAP        = BOX.RSG(SNAP_NUM)
PSNAP       = PARTBOX.PART(SNAP_NUM)
REDSHIFT    = (1/SNAP.Attribute.Time())-1
BOX_SIZE    = SNAP.Attribute.BoxSize()/1000


# --- REORDER
ORDER       = numpy.argsort(SNAP.RKSGroups.VirialMass())[::-1]    # Reorders as decreasing mass

# TARGET HALO FEILDS
TIHID       = SNAP.RKSGroups.InternalHaloID()[ORDER][HALO_OFFSET]
TMVIR       = SNAP.RKSGroups.VirialMass()[ORDER][HALO_OFFSET]
TRVIR       = SNAP.RKSGroups.VirialRadius()[ORDER][HALO_OFFSET]*0.001
TPOS        = SNAP.RKSGroups.Position()[ORDER][HALO_OFFSET]

# TIHID       = SNAP.RKSGroups.InternalHaloID()[HALO_OFFSET]
# TMVIR       = SNAP.RKSGroups.VirialMass()[HALO_OFFSET]
# TRVIR       = SNAP.RKSGroups.VirialRadius()[HALO_OFFSET]*0.001
# TPOS        = SNAP.RKSGroups.Position()[HALO_OFFSET]


def GetParticlePos(PTYPE):
    P_IHIDS = PTYPE.InternalHaloID()                # Get all particle ihids
    P_POS   = PTYPE.Position()[P_IHIDS==TIHID]      # Filter for particles in target
    P_POS  -= TPOS                                  # Get positions relative to halo center
    P_DIST  = numpy.linalg.norm(P_POS,axis=1)       # Get distance of particles from center
    if WITHIN_RVIR:                                 # Virial radius Filter
        P_POS = P_POS[P_DIST<TRVIR]

    return P_POS

TDM_POS      = GetParticlePos(SNAP.DarkMatter)
TGAS_POS     = GetParticlePos(SNAP.Gas)
TSTAR_POS    = GetParticlePos(SNAP.Star)
TBH_POS      = GetParticlePos(SNAP.BlackHole)




# PLOT
fig = plt.figure("Particles",figsize=(6,6))
# ax = plt.axes(projection='3d')
ax = plt.axes()

fig1 = plt.figure("Dark Matter",figsize=(6,6))
ax1 = plt.axes(projection='3d')
fig2 = plt.figure("Gas",figsize=(6,6))
ax2 = plt.axes(projection='3d')
fig3 = plt.figure("Star",figsize=(6,6))
ax3 = plt.axes(projection='3d')
fig4 = plt.figure("BlackHole",figsize=(6,6))
ax4 = plt.axes(projection='3d')


#  For blackhole size scaling
# bh_mask = (BH_IHIDS==TIHID)
# bh_mass = SNAP.BlackHole.Mass()[bh_mask][R_TBH<TRVIR]
# print(numpy.log10(bh_mass))
# For offset_id=1 blackhole mass almost macth

# bhs = numpy.int32(100*(bh_mass/numpy.max(bh_mass))**3)


# OFFSET
BOUND       = 2*max(numpy.vstack([TDM_POS,TGAS_POS,TSTAR_POS,TBH_POS]).flatten())
TRANSLATE   = numpy.ones(3)*(BOUND/2) 
ZOOM_SCALE  = 3

PlotCube(ax1,(TDM_POS*ZOOM_SCALE) +TRANSLATE,BOUND,2,'m',alpha=0.5)
PlotCube(ax2,(TGAS_POS*ZOOM_SCALE) +TRANSLATE,BOUND,2,'c',alpha=0.5)
PlotCube(ax3,(TSTAR_POS*ZOOM_SCALE)+TRANSLATE,BOUND,2,'darkorange',alpha=0.5)
PlotCube(ax4,(TBH_POS*ZOOM_SCALE)  +TRANSLATE,BOUND,10,'k')


if True:
    BOUND = BOUND/2
    slice_at = 0.5
    slice_thickness = BOUND/10

    slice_at *= BOUND
    slice_thickness /= 2
    slice_thickness *= BOUND

    img_width = 1000
    img_heigh = 1000

    img = numpy.empty((img_width,img_heigh))

    dx = BOUND/img_width
    dy = BOUND/img_heigh



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

    kdt = spatial.cKDTree((TSTAR_POS) + numpy.ones(3)*BOUND/2)
    cx=0
    while cx<BOUND:
        cy=0
        while cy<BOUND:
            neighbours_index=kdt.query_ball_point([cx,cy,slice_at],2*h)
            neighbours = kdt.data[neighbours_index]
            n= neighbours
            q = numpy.sqrt(numpy.power(n[:,0]-cx,2)+numpy.power(n[:,1]-cy,2))/h
            density = numpy.sum(CubicSpline(q))
            img[int(cx/dx),int(cy/dy)]=density
            cy+=dy
        cx+=dx

    ax.imshow(img)




# --- SAVE
for ax in [ax1,ax2,ax3,ax4]:
    ax.set_xlim(0,BOUND)
    ax.set_ylim(0,BOUND)
    ax.set_zlim(0,BOUND)
    ax.set_box_aspect([1.0, 1.0, 1.0])

plt.tight_layout()
plt.show()

# plt.savefig(SAVE_PATH,dpi=300)
# plt.savefig("/mnt/home/student/cranit/Repo/MPAnalysis/temp/plots/part_sep.png",dpi=400)
import numpy, galspec
import matplotlib.pyplot as plt

from galspec.navigation.MPGADGET.Sim import _Sim


from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roboto']})
rc('text', usetex=True)






# --- FLAGS
SNAP_NUM    = 36
SAVE_PATH   = "/mnt/home/student/cranit/Work/RSGBank/Results_PMCAM/main_sequence_convergence.png" 
REDSHIFT    = 8


# --- SIMULATIONS
L50N640     = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640")
L140N700    = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L140N700")
L140N896    = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L140N896")
L140N1008   = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L140N1008")
L50N1008   = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N1008")

# --- LINKING BOX         
BOX_LIST    = [ [L50N640    ,"L50N640"   ,"r"   ,1.5e10],
                [L50N1008   ,"L50N1008"  ,"g"   ,9e9],
                # [L140N700   ,"L140N700"  ,"y"   ,5e10],
                # [L140N896   ,"L140N896"  ,"c"   ,5e10],
                [L140N1008  ,"L140N1008" ,"b"   ,5.5e10] ]

# --- MAIN SEQUENCE PLOT
fig, ax = plt.subplots(figsize=(10,8))
iax = ax.inset_axes([0.7,0.1,0.31,0.3])

star_mass_min = 0
star_mass_max = 0

def PlotMS(BOX:_Sim,mask_lim,**kwargs):

    # --- AUTO-FLAGS
    SNAP        = BOX.RSG(SNAP_NUM)
    MASS_UNIT   = 10**10
    MASS_TABLE  = SNAP.Attribute.MassTable() * MASS_UNIT

    # --- GET FIELDS
    MVIR        = SNAP.RKSGroups.VirialMass()
    LBT         = SNAP.RKSGroups.LengthByTypeInRvirWC()
    SFR         = SNAP.RKSGroups.StarFormationRate()

    # --- GET BUDGET
    STAR = SNAP.RKSGroups.MassByTypeInRvirWC()[:,4]
    MVIR  = SNAP.RKSGroups.VirialMass()

    # --- MASK AND PLOT

    mask1 = (MVIR>mask_lim)
    mask2 = (STAR>0)
    mask = mask1 & mask2

    ax.plot(STAR[mask],SFR[mask],'.',ms=2,**kwargs)
    iax.plot(numpy.log10(STAR[mask]),numpy.log10(SFR[mask]/STAR[mask]),'.',ms=1,**kwargs)

    # Update star mass for observation fitting
    box_star_mass_min = min(STAR[mask])
    box_star_mass_max = max(STAR[mask])

    global star_mass_min
    global star_mass_max

    if (star_mass_min==0) or (box_star_mass_min<star_mass_min):
        star_mass_min=box_star_mass_min
    
    if (star_mass_max==0) or (box_star_mass_max>star_mass_max):
        star_mass_max=box_star_mass_max
    
    



for BOX in BOX_LIST: PlotMS(BOX[0],BOX[3],label=BOX[1],color=BOX[2])




# --- OBSERVATION
# Calabro et al. (arXiv:2402.17829v1) 
# Table 1 (3rd row) and Fig 4
M_comp = numpy.array([star_mass_min,star_mass_max])
def GetObs(M,m,q,merr,qerr,**kwargs):
    # x = log M*/M0
    # y = log SFR/(M0/yr)
    # y = m*x + q
    x = numpy.log10(M)
    y = m*x + q

    # --- Fit plot
    fitSFR = numpy.power(10,y)
    ax.plot(M,fitSFR,'k-',**kwargs)
    # iax.plot(numpy.log10(M),numpy.log10((10**q)*numpy.power(M,m-1)),'k-',**kwargs)
    iax.plot(numpy.log10(M),numpy.log10(fitSFR/M),'k-',**kwargs)

    # --- Error plot
    xl = x[0] #left
    xr = x[-1] #right
    mp,mn=m+merr,m-merr #positive,negative
    qp,qn=q+qerr,q-qerr

    yl_max = max(mp*xl+qp, mp*xl+qn, mn*xl+qp, mn*xl+qn)
    yl_min = min(mp*xl+qp, mp*xl+qn, mn*xl+qp, mn*xl+qn)
    yr_max = max(mp*xr+qp, mp*xr+qn, mn*xr+qp, mn*xr+qn)
    yr_min = min(mp*xr+qp, mp*xr+qn, mn*xr+qp, mn*xr+qn)

    fitSFR_err_max = numpy.power(10,[yl_max,yr_max])
    fitSFR_err_min = numpy.power(10,[yl_min,yr_min])

    ax.fill_between(M,fitSFR_err_max,fitSFR_err_min,color='k',alpha=0.05,ec=None)
    iax.fill_between(numpy.log10(M),numpy.log10(fitSFR_err_max/M),numpy.log10(fitSFR_err_min/M),color='k',alpha=0.05,ec=None)


# GetObs(M_comp,0.55,-4.0,0.12,1,lw=1,label="Calabro et al. (2024)")
GetObs(M_comp,0.76,-6.0,0.07,0.6,lw=1,label="Calabro et al. (2024)")





# --- BEUTIFY
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel("Stellar Mass $(M_{*}/M_{\odot})$",fontsize=20)
ax.set_ylabel("Star Formation Rate $(M_{\odot} $yr$^{-1})$",fontsize=20)
ax.tick_params(axis='both', which='major', labelsize=16)
ax.tick_params(axis='both', which='minor', labelsize=12)

# iax.set_xscale('log')
# iax.set_yscale('log')
iax.set_xlabel("$\log(M_{*}/M_{\odot})$",fontsize=12,labelpad=0)
iax.set_ylabel("$\log$ sSFR $($yr$^{-1})$",fontsize=12,rotation=-90,labelpad=16)
iax.tick_params(axis='both', labelsize=6)
iax.yaxis.set_label_position("right")
iax.yaxis.tick_right()
iax.tick_params(axis='both', which='major', labelsize=8)
iax.tick_params(axis='both', which='minor', labelsize=8)

plt.legend(loc="upper left",fontsize=14,frameon=False,markerscale=4)
plt.annotate(f"$z={numpy.round(REDSHIFT,2)}$",xy=(0.5,1),xytext=(0,-10),xycoords="axes fraction",textcoords="offset pixels",ha="center",va='top',fontsize=20)
# plt.title(f"MAIN SEQUENCE (z={numpy.round(REDSHIFT,2)})")


# --- SAVE
plt.show()
# plt.savefig(SAVE_PATH,dpi=300)
# plt.savefig("temp/plots/main_seq.png",dpi=300)
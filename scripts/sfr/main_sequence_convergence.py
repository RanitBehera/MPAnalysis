import numpy, galspec
import matplotlib.pyplot as plt

from galspec.navigation.MPGADGET.Sim import _Sim

import matplotlib
matplotlib.use('Agg')


# --- FLAGS
SNAP_NUM    = 36
SAVE_PATH   = "/mnt/home/student/cranit/Work/RSGBank/Results/main_sequence_convergence.png" 
REDSHIFT    = 8


# --- SIMULATIONS
L50N640     = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640")
L140N700    = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L140N700")
L140N896    = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L140N896")
L140N1008   = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L140N1008")

# --- LINKING BOX         
BOX_LIST    = [ [L50N640    ,"L50N640"   ,"r"   ,1.5e10],
                # [L140N700   ,"L140N700"  ,"y"   ,5e10],
                # [L140N896   ,"L140N896"  ,"c"   ,5e10],
                [L140N1008  ,"L140N1008" ,"b"   ,5.5e10] ]

# --- MAIN SEQUENCE PLOT
fig, ax = plt.subplots()
iax = ax.inset_axes([0.7,0.1,0.31,0.3])

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
    GAS,DM,U1,U2,STAR,BH = numpy.transpose(LBT)
    GAS     *=  MASS_TABLE[0]
    DM      *=  MASS_TABLE[1]
    STAR    *=  MASS_TABLE[4]
    BH      *=  MASS_TABLE[5]
    MTOTAL  = GAS + DM + STAR + BH
    RATIO = MTOTAL/MVIR

    # --- MASK AND PLOT

    mask1 = (MVIR>mask_lim)
    mask2 = (STAR>0)
    mask = mask1 & mask2

    ax.plot(STAR[mask],SFR[mask],'.',ms=2,**kwargs)
    iax.plot(numpy.log10(STAR[mask]),numpy.log10(SFR[mask]/STAR[mask]),'.',ms=1,**kwargs)
    
    # iax.axhline(numpy.log10(3e-9),color='k',lw=1,ls='--')



for BOX in BOX_LIST: PlotMS(BOX[0],BOX[3],label=BOX[1],color=BOX[2])

# --- BEUTIFY
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel("Stellar Mass $(M_{*}/M_{\odot})$")
ax.set_ylabel("Star Formation Rate $(M_{\odot} yr^{-1})$")

# iax.set_xscale('log')
# iax.set_yscale('log')
iax.set_xlabel("$\log(M_{*}/M_{\odot})$",fontsize=6,labelpad=0)
iax.set_ylabel("sSFR $(yr^{-1})$",fontsize=6,rotation=-90,labelpad=10)
iax.tick_params(axis='both', labelsize=6)
iax.yaxis.set_label_position("right")
iax.yaxis.tick_right()

plt.legend()
plt.title(f"MAIN SEQUENCE CONVERGENCE\nz={numpy.round(REDSHIFT,2)}")

# --- SAVE
plt.savefig(SAVE_PATH,dpi=200)
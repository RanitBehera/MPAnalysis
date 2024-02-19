import numpy, galspec
import matplotlib.pyplot as plt

from galspec.utility.MassFunction import MassFunction, MassFunctionLitreture
from galspec.navigation.MPGADGET.Sim import _Sim


import matplotlib
matplotlib.use('Agg')


# --- SIMULATIONS
L50N640     = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640")
L140N700    = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L140N700")
L140N896    = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L140N896")
L140N1008   = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L140N1008")


# --- FLAGS
SNAP_NUM    = 36
BIN_SIZE    = 0.5
MASS_HR     = numpy.logspace(7,12,100) # High resolution mass for litrature mass function plot
SAVE_PATH   = "/mnt/home/student/cranit/Work/RSGBank/Results_PMCAM/p2_mf_conv.png"

INCLUDE_CONTRIBUTIONS = [1,1,1,0]   # [ DM, GAS, STAR, BH ]


# --- LINKING BOX           
BOX_LIST    = [ [L50N640    ,"L50N640"   ,"r"],
                [L140N700   ,"L140N700"  ,"y"],
                [L140N896   ,"L140N896"  ,"c"],
                [L140N1008  ,"L140N1008" ,"b"] ]

# --- AUTO-FLAGS
# Make sure cosmology in all simulations are same
COSMOLOGY   = L50N640.GetCosmology("MassFunctionLitrature")
SNAP        = L50N640.RSG(SNAP_NUM)
REDSHIFT    = (1/SNAP.Attribute.Time())-1 
HUBBLE      = SNAP.Attribute.HubbleParam()


# --- SIMULATION MASS FUNCTIONS
def PlotSMF(SIM:_Sim,**kwargs):
    SNAP = SIM.RSG(SNAP_NUM)
    BOX_SIZE = SNAP.Attribute.BoxSize()/1000
    MASS_UNIT = 10**10                          # <--- HARD CODE
    MASS_TABLE = SNAP.Attribute.MassTable() * MASS_UNIT

    conv_lim = 32 * MASS_TABLE[1]

    def PlotMF(mass,**kwargs):
        M, dn_dlogM = MassFunction(mass,BOX_SIZE,BIN_SIZE)
        mask1        = (dn_dlogM>1e-20)
        mask2        = (log_M>conv_lim)
        mask=mask1 #& mask2
        plt.plot(log_M[mask1],dn_dlogM[mask1],alpha=0.1)
        plt.plot(log_M[mask],dn_dlogM[mask],**kwargs)
    
    PlotMF(SNAP.RKSGroups.VirialMass(),**kwargs)
    plt.axvline(conv_lim,color=kwargs['color'],lw=0.5,ls='--',alpha=0.5)


    if True in INCLUDE_CONTRIBUTIONS:
        LBT = SNAP.RKSGroups.LengthByTypeInRvirWC()
        GAS,DM,U1,U2,STAR,BH = numpy.transpose(LBT)
        GAS     *=  MASS_TABLE[0]
        DM      *=  MASS_TABLE[1]
        STAR    *=  MASS_TABLE[4]
        BH      *=  MASS_TABLE[5]

        if INCLUDE_CONTRIBUTIONS[0]:PlotMF(DM,      color=kwargs['color'],lw=1,ls='--')
        if INCLUDE_CONTRIBUTIONS[1]:PlotMF(GAS,     color=kwargs['color'],lw=1,ls=':')
        if INCLUDE_CONTRIBUTIONS[2]:PlotMF(STAR,    color=kwargs['color'],lw=0.5,ls='-.')
        if INCLUDE_CONTRIBUTIONS[3]:PlotMF(BH,      color=kwargs['color'],lw=1,ls='-.')

        
for BOX in BOX_LIST:
    PlotSMF(BOX[0],label=BOX[1],color=BOX[2],lw=1)



# --- LITRARTURE MASS FUNCTIONS
if True:
    log_M, dn_dlogM = MassFunctionLitreture("Seith-Tormen",COSMOLOGY,REDSHIFT,MASS_HR,"dn/dlnM")
    plt.plot(log_M,dn_dlogM*HUBBLE,'k',lw=1,zorder=-1,alpha=0.1)

    log_M, dn_dlogM = MassFunctionLitreture("Press-Schechter",COSMOLOGY,REDSHIFT,MASS_HR,"dn/dlnM")
    plt.plot(log_M,dn_dlogM*HUBBLE,'k',lw=1,zorder=-1,alpha=0.1)


# --- BEUTIFY
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.xlabel("$M/M_{\odot}$")
plt.ylabel("$dn/d\log(M/M_{\odot})$")
plt.title(f"MASS FUNCTION CONVERGENCE\n z={numpy.round(REDSHIFT,2)}")

# --- SAVE
plt.savefig(SAVE_PATH,dpi=200)


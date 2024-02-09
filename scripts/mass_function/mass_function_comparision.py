import numpy, galspec
import matplotlib.pyplot as plt

from galspec.utility.MassFunction import MassFunction, MassFunctionLitreture,MASS_OPTIONS

import matplotlib
matplotlib.use('Agg')


# --- FLAGS
SNAP_NUM    = 36
BIN_SIZE    = 0.5
MASS_HR     = numpy.logspace(7,12,100) # High resolution mass for litrature mass function plot
SAVE_PATH   = "/mnt/home/student/cranit/Work/RSGBank/Results/mass_function_comparision.png" 

# --- SIMULATIONS
BOX         = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640")

# --- AUTO-FLAGS
# Make sure cosmology in all simulations are same
COSMOLOGY   = BOX.GetCosmology("MassFunctionLitrature")
SNAP        = BOX.RSG(SNAP_NUM)
REDSHIFT    = (1/SNAP.Attribute.Time())-1
BOX_SIZE    = SNAP.Attribute.BoxSize()/1000
BOX_TEXT    = BOX.path.split("_")[-1]       # Special Case Work Only
HUBBLE      = SNAP.Attribute.HubbleParam()
MASS_UNIT   = 10**10
MASS_TABLE  = SNAP.Attribute.MassTable() * MASS_UNIT

# --- GET FIELDS
MVIR        = BOX.RSG(SNAP_NUM).RKSGroups.VirialMass()
LBT         = BOX.RSG(SNAP_NUM).RKSGroups.LengthByTypeInRvirWC()

GAS,DM,U1,U2,STAR,BH = numpy.transpose(LBT)
DM      *=  MASS_TABLE[1]




# --- MASS FUNCTION PLOTS
log_M, dn_dlogM = MassFunction(MVIR,BOX_SIZE,BIN_SIZE)
plt.plot(log_M,dn_dlogM,color="k",label="Virial Mass",lw=2)

log_M, dn_dlogM = MassFunction(DM,BOX_SIZE,BIN_SIZE)
plt.plot(log_M,dn_dlogM,color="m",label="Dark Matter",lw=1,ls='--')

def PlotLMF(model:MASS_OPTIONS,**kwargs):
    log_M, dn_dlogM = MassFunctionLitreture(model,COSMOLOGY,REDSHIFT,MASS_HR,'dn/dlnM')
    plt.plot(log_M,dn_dlogM*HUBBLE,label=model,lw=1,**kwargs)

PlotLMF("Seith-Tormen")
PlotLMF("Press-Schechter")

# --- BEUTIFY
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.xlabel("$M/M_{\odot}$")
plt.ylabel("$dn/d\log(M/M_{\odot})$")
plt.title(f"MASS FUNCTION COMPARISION\n BOX : {BOX_TEXT} ; z={numpy.round(REDSHIFT,2)}")

# --- SAVE
plt.savefig(SAVE_PATH,dpi=200)
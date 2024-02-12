import numpy, galspec
import matplotlib.pyplot as plt

from galspec.utility.MassFunction import MassFunction, MassFunctionLitreture

import matplotlib
matplotlib.use('Agg')

# --- SIMULATIONS
BOX         = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640")

# --- FLAGS
SNAP_NUM    = 36
BIN_SIZE    = 0.5
MASS_HR     = numpy.logspace(6,12,100) # High resolution mass for litrature mass function plot
SAVE_PATH   = "/mnt/home/student/cranit/Work/RSGBank/Results/mass_function_contribution.png" 


# --- AUTO-FLAGS
# Make sure cosmology in all simulations are same
COSMOLOGY   = BOX.GetCosmology("MassFunctionLitrature")
SNAP        = BOX.RSG(SNAP_NUM)
REDSHIFT    = (1/SNAP.Attribute.Time())-1
BOX_SIZE    = SNAP.Attribute.BoxSize()/1000
MASS_UNIT   = 10**10
MASS_TABLE  = SNAP.Attribute.MassTable() * MASS_UNIT
BOX_TEXT    = BOX.path.split("_")[-1]       # Special Case Work Only
HUBBLE      = SNAP.Attribute.HubbleParam()

# --- GET FIELDS
MVIR        = BOX.RSG(SNAP_NUM).RKSGroups.VirialMass()
LBT         = BOX.RSG(SNAP_NUM).RKSGroups.LengthByTypeInRvirWC()

# --- GET BUDGET
GAS,DM,U1,U2,STAR,BH = numpy.transpose(LBT)
GAS     *=  MASS_TABLE[0]
DM      *=  MASS_TABLE[1]
STAR    *=  MASS_TABLE[4]
BH      *=  MASS_TABLE[5]
MTOTAL  = GAS + DM + STAR + BH
RATIO = MTOTAL/MVIR


# --- MASS FUNCTION PLOTS
def PlotMF(mass,**kwargs):
    log_M, dn_dlogM = MassFunction(mass,BOX_SIZE,BIN_SIZE)
    mask        = (dn_dlogM>1e-20)
    plt.plot(log_M[mask],dn_dlogM[mask],**kwargs)

PlotMF(MVIR,color="k",label="Virial Mass",lw=2)
PlotMF(DM,color="m",label="Dark Matter",ls='--',lw=1)
PlotMF(GAS,color="b",label="Gas",ls='--',lw=1)
PlotMF(STAR,color="y",label="Star",ls='--',lw=1)
PlotMF(BH,color="k",label="Blackhole",ls='--',lw=1)
PlotMF(MTOTAL,color="r",label="Total",ls='--',lw=1)

log_M, dn_dlogM = MassFunctionLitreture("Seith-Tormen",COSMOLOGY,REDSHIFT,MASS_HR,'dn/dlnM')
plt.plot(log_M,dn_dlogM*HUBBLE,label="Seith-Tormen",ls='-',color='k',lw=1)


# --- TEMP CHECK ASTRID
x = [7.015723270440252, 10.066037735849056, 10.41194968553459, 9.374213836477988, 7.361635220125786, 7.723270440251572, 8.084905660377359, 8.430817610062894, 8.69811320754717, 8.949685534591195, 9.185534591194969, 9.531446540880504, 9.79874213836478]
y = [-1.948717948717949, -6.794871794871795, -7.282051282051282, -5, -2.282051282051282, -2.6923076923076925, -3.1282051282051286, -3.5897435897435903, -4, -4.384615384615385, -4.717948717948718, -5.461538461538462, -6.128205128205128]

m = numpy.power(10,x)
dn = numpy.power(10,y)
sa = numpy.argsort(m)
m,dn=m[sa],dn[sa]
plt.plot(m,dn,'g',lw=1,label="Star (Astrid) **")

# LBT         = BOX.RSG(SNAP_NUM).RKSGroups.LengthByTypeWC()

BOX         = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/L50N640")
LBT         = BOX.PIG(SNAP_NUM).FOFGroups.LengthByType()
GAS,DM,U1,U2,STAR,BH = numpy.transpose(LBT)
STAR    = numpy.int64(STAR)
MASS_TABLE = numpy.int64(MASS_TABLE)
STAR    *=  MASS_TABLE[4]
PlotMF(STAR,color="y",label="Star FOF **",ls='-',lw=1)



# --- BEUTIFY
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.xlabel("$M/M_{\odot}$")
plt.ylabel("$dn/d\log(M/M_{\odot})$")
plt.title(f"MASS FUNCTION CONTRIBUTION\n BOX : {BOX_TEXT} ; z={numpy.round(REDSHIFT,2)}")

# --- SAVE
plt.savefig(SAVE_PATH,dpi=200)
import numpy, galspec
import matplotlib.pyplot as plt

from galspec.utility.MassFunction import MassFunction, MassFunctionLitreture,MASS_OPTIONS

# import matplotlib
# matplotlib.use('Agg')

# --- SIMULATIONS
BOX         = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640")
LINKED_BOX  = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/L50N640")

# --- FLAGS
SNAP_NUM    = 36
BIN_SIZE    = 0.5
MASS_HR     = numpy.logspace(7,12,100) # High resolution mass for litrature mass function plot
SAVE_PATH   = "/mnt/home/student/cranit/Work/RSGBank/Results_PMCAM/p1_mf_comp1.png" 
HALO_DEF    = 50    # Can be auto detected from rockstar.cfg

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
MIN_HALO_MASS = HALO_DEF * MASS_TABLE[1]

# --- MASS FUNCTION PLOTS
fig,ax = plt.subplots(2,1,figsize=(10,8),sharex=True,height_ratios=[3,1])

# Litrature
def PlotLMF(model:MASS_OPTIONS,label:str="",**kwargs):
    M, dn_dlogM = MassFunctionLitreture(model,COSMOLOGY,REDSHIFT,MASS_HR,'dn/dlnM')
    ax[0].plot(M,dn_dlogM*HUBBLE,label=model + label,lw=1,**kwargs)
    return M,dn_dlogM*HUBBLE
M_st,mfhr_st = PlotLMF("Seith-Tormen"," (FoF)",ls="-",c='k')
M_ps,mfhr_ps = PlotLMF("Press-Schechter"," (FoF)",ls="--",c='k')

def Extrapolated_MF(lit_m,lit_mf,mass):
    near_mf=numpy.empty(len(mass))
    for i,m in enumerate(mass):
        mass_diff_arr = lit_m-m
        min_mass_diff_ind = numpy.argmin(numpy.abs(mass_diff_arr))

        # Interpolate in log plot while values are in linear plot
        min_mass_diff = mass_diff_arr[min_mass_diff_ind]
        if min_mass_diff<0:slope_offset = 1
        else:slope_offset = -1

        delta_logy = numpy.log10(lit_mf[min_mass_diff_ind+slope_offset])-numpy.log10(lit_mf[min_mass_diff_ind])
        delta_logx = numpy.log10(lit_m[min_mass_diff_ind+slope_offset])-numpy.log10(lit_m[min_mass_diff_ind])
        slope = delta_logy/delta_logx
        d_logx = numpy.log10(m) - numpy.log10(lit_m[min_mass_diff_ind])
        d_logy = slope * d_logx
        near_mf[i] = 10**(numpy.log10(lit_mf[min_mass_diff_ind]) + d_logy)

    return near_mf


# FoF
if True:
    MFOF        = LINKED_BOX.PIG(SNAP_NUM).FOFGroups.MassByType()
    GAS,DM,U1,U2,STAR,BH = numpy.transpose(MFOF)
    DM         *=  MASS_UNIT
    M, dn_dlogM,error = MassFunction(DM,BOX_SIZE,BIN_SIZE)

    # Filter
    M,dn_dlogM,error = M[:-2],dn_dlogM[:-2],error[:-2]
    mass_mask = (M>MIN_HALO_MASS)
    num_mask = (dn_dlogM>1e-20)
    mask = mass_mask & num_mask
    M,dn_dlogM,error = M[mask],dn_dlogM[mask],error[mask]
    
    osmf = (dn_dlogM)                           # Observed simulation mass function (linear)
    eelmf = Extrapolated_MF(M_st,mfhr_st,M)     # Expected extrapolated litrarture mass function (linear)
    dev_by_fac =  osmf/eelmf
    dev_by_fac_p =  (osmf+0.7*error)/eelmf
    dev_by_fac_n =  (osmf-0.7*error)/eelmf
    
    #plot
    ax[0].plot(M,dn_dlogM,'b.-',label="Dark Matter (FoF)",lw=2)
    ax[1].plot(M,dev_by_fac,'b.-')
    ax[1].fill_between(M,dev_by_fac_p,dev_by_fac_n,alpha=0.2,color='b',edgecolor=None)




# Rockstar
if True:
    MVIR        = BOX.RSG(SNAP_NUM).RKSGroups.VirialMass()
    LBT         = BOX.RSG(SNAP_NUM).RKSGroups.LengthByTypeInRvirWC()
    GAS,DM,U1,U2,STAR,BH = numpy.transpose(LBT)
    DM         *=  MASS_TABLE[1]
    M, dn_dlogM,error = MassFunction(DM,BOX_SIZE,BIN_SIZE)
    
    # Filter
    # M,dn_dlogM,error = M[:-2],dn_dlogM[:-2],error[:-2]
    mass_mask = (M>MIN_HALO_MASS)
    num_mask = (dn_dlogM>1e-20)
    mask = mass_mask & num_mask
    M,dn_dlogM,error = M[mask],dn_dlogM[mask],error[mask]

    osmf = (dn_dlogM)                           # Observed simulation mass function (linear)
    eelmf = Extrapolated_MF(M_ps,mfhr_ps,M)     # Expected extrapolated litrarture mass function (linear)
    dev_by_fac =  osmf/eelmf
    dev_by_fac_p =  (osmf+0.7*error)/eelmf
    dev_by_fac_n =  (osmf-0.7*error)/eelmf
    
    #plot
    ax[0].plot(M,dn_dlogM,'c.-',label="Dark Matter (Virial)",lw=2)
    # ax[1].plot(M,dev_by_fac,'b.-')
    # ax[1].fill_between(M,dev_by_fac_p,dev_by_fac_n,alpha=0.2,color='m',edgecolor=None)


# log_M, dn_dlogM = MassFunction(MVIR,BOX_SIZE,BIN_SIZE)
# plt.plot(log_M,dn_dlogM,color="k",label="Virial Mass",lw=2)



# --- BEUTIFY
ax[0].set_xscale('log')
ax[0].set_yscale('log')
ax[0].legend()
ax[0].set_ylabel("$dn/d\log(M/M_{\odot})$")
ax[0].grid(alpha=0.3)

ax[1].set_xlabel("$M/M_{\odot}$")
# ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_ylabel("Deviation\nby Factor")
ax[1].set_xscale('log')
ax[1].axhline(1,ls='-',c='k')
ax[1].grid(alpha=0.3)

# ax[1].set_yscale('log')
ax[1].set_ylim(0.6,1.5)
# Direct yscale('log') has issue of hiding default labels and ticks 
# which is partly from ylim values also. 
# So as work around we make lin-log conversion


ticks= [0.8,1,1.25]
# ax[1].set_yticks([])
# ax[1].set_yticklabels([])
ax[1].set_yticks(ticks,minor=False)
ax[1].set_yticklabels([str(t) for t in ticks])





# plt.suptitle(f"MASS FUNCTION COMPARISION\n BOX : {BOX_TEXT} ; z={numpy.round(REDSHIFT,2)}")
plt.suptitle(f"HALO MASS FUNCTION COMPARISION\n BOX : {BOX_TEXT} ; z={numpy.round(REDSHIFT,2)}")
plt.subplots_adjust(hspace=0)

# --- SAVE
plt.savefig(SAVE_PATH,dpi=400)
# plt.show()
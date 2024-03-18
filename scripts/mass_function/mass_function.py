import numpy, galspec,os
import matplotlib.pyplot as plt

from galspec.utility.MassFunction import MassFunction, MassFunctionLiterature,LMF_OPTIONS


# --- SIMULATIONS
# Rockstar dump folders
# Make sure corresponding snapshorts are at same time

L50N640     = "/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640"
L50N1008     = "/mnt/home/student/cranit/Work/RSGBank/OUT_L50N1008"
L140N700    = "/mnt/home/student/cranit/Work/RSGBank/OUT_L140N700"
L140N896    = "/mnt/home/student/cranit/Work/RSGBank/OUT_L140N896"
L140N1008   = "/mnt/home/student/cranit/Work/RSGBank/OUT_L140N1008"

L50N640_z6     = "/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640_z6"

ONLY_PIG = False
if ONLY_PIG:
    L50N640     = "/mnt/home/student/cranit/Work/RSGBank/L50N640"
    L140N700    = "/mnt/home/student/cranit/Work/RSGBank/L140N700"
    L140N896    = "/mnt/home/student/cranit/Work/RSGBank/L140N896"
    L140N1008   = "/mnt/home/student/cranit/Work/RSGBank/L140N1008"
    L50N1008   =  "/mnt/home/student/cranit/Work/RSGBank/L50N1008"

    L50N1008   =  "/mnt/home/student/cranit/Work/RSGBank/L50N1008"
    L50N640_a100 = "/mnt/home/student/cranit/Work/RSGBank/L50N640" 
    L50N640_a200 = "/scratch/nkhandai/mp-gadget/50Mpc_640cube_alpha200" 
    L50N640_a400 = "/scratch/nkhandai/mp-gadget/50Mpc_640cube_alpha400" 



# --- FLAGS
FOF,ROCKSTAR    = 1,2       # Don't change this
DM,GAS,STAR,BH  = 1,2,4,8   # Don't change this
if ONLY_PIG:ROCKSTAR*=0

# Skip points structure [[fof-dm,fof-gas,fof-star],[vir-dm,vir-gas,vir-star]]
CURVE_LIST       = [ 
        [L50N640, 0*FOF + ROCKSTAR, (DM+GAS+STAR),[[1,2,4],[1,1,4]]],
        [L140N1008, 0*FOF + ROCKSTAR, (DM+GAS+STAR),[[0,0,0],[1,0,1]]],
        [L50N1008, 0*FOF + ROCKSTAR, (DM+GAS+STAR),[[1,2,4],[1,1,4]]],
        # [L140N700, 0*FOF + ROCKSTAR, 0*(DM+GAS+STAR)+BH,[[0,0,0],[0,0,0]]],
        # [L140N896, 0*FOF + ROCKSTAR, 0*(DM+GAS+STAR)+BH,[[0,0,0],[0,0,0]]],
        # [L140N1008, 0*FOF + ROCKSTAR, 0*(DM+GAS+STAR)+BH,[[0,0,0],[0,0,0]]],
        # [L50N640_a100, 0*FOF + ROCKSTAR, GAS+STAR+BH,[[1,2,4],[1,1,2]],"$\\alpha=100$"],
        # [L50N640_a200, FOF + 0*ROCKSTAR, GAS+STAR+BH,[[0,0,0],[0,0,0]],"$\\alpha=200$"],
        # [L50N640_a400, FOF + 0*ROCKSTAR, GAS+STAR+BH,[[0,0,0],[0,0,0]],"$\\alpha=400$"]
        # [L50N1008, FOF + 0*ROCKSTAR, GAS+STAR+BH,[[0,0,0],[0,0,0]],"$\\alpha$"]
    ]

COLORS_FOF  = ['cyan','blue','red','g']
COLORS_RKS  = ['lime','green','m','g']
COLORS_FOF  = ['tab:blue','tab:orange','tab:green','g']

SNAP_NUM    = 36
BIN_SIZE    = 0.5
MASS_HR     = numpy.logspace(7,12,100) # High resolution mass for literature mass function plot
SAVE_PATH   = "temp/plots/gal_bh_mf_avar.png" 
INCLUDE_DEVIATION = False
# INCLUDE_LMF = True          # Deviation axis and its plot also needs to be adapted. Not implemeted for now.

LEGEND_TITLE    = "Friends-of-Friends"
# LEGEND_TITLE    = "ROCKSTAR-Galaxies"


# --- COMMON AUTO-FLAGS
# Make sure following parameters are same in all simulations
REFBOX      = galspec.NavigationRoot(L50N640)
COSMOLOGY   = REFBOX.GetCosmology("MassFunctionLitrature")
if not ONLY_PIG : SNAP        = REFBOX.RSG(SNAP_NUM)
if ONLY_PIG: SNAP = REFBOX.PART(SNAP_NUM) 
REDSHIFT    = (1/SNAP.Attribute.Time())-1
HUBBLE      = SNAP.Attribute.HubbleParam()


# --- HELPER FUNCTION
def Get_Options_List(value):
    # 7  = 4 + 2 + 1
    # 13 = 8 + 4 + 1
    seq = []
    while value>0:
        p= 1
        while p*2 <= value:p *= 2
        seq.append(p)
        value -= p
    return seq

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


# --- PLOT HANDLES
if INCLUDE_DEVIATION:
    fig,ax = plt.subplots(2,1,figsize=(14,8),sharex=True,height_ratios=[3,1])
else:
    fig,ax = plt.subplots(1,1,figsize=(14,8))
    ax  =   [ax]    # to use ax[0] syntax

# --- PLOT HELPER FUNCTION
# Literature mass function
def PlotLMF(model:LMF_OPTIONS,label:str="",**kwargs):
    # HUBBLE=1
    M, dn_dlogM = MassFunctionLiterature(model,COSMOLOGY,REDSHIFT,MASS_HR,'dn/dlnM')
    ax[0].plot(M,dn_dlogM*HUBBLE,label=model + label,lw=1,**kwargs)
    return M,dn_dlogM*HUBBLE

M_st,mfhr_st = PlotLMF("Seith-Tormen","",ls="--",c='k')
M_ps,mfhr_ps = PlotLMF("Press-Schechter","",ls=":",c='k')
# M_ps,mfhr_ps = PlotLMF("Comparat(z=0)","",ls="-",c='k')

# Box mass function
def PlotBMF(M,dn_dlogM,error,min_mass,right_skip_count,include_deviation,color,leg,marker):
    # Filters
    if right_skip_count>0:
        M,dn_dlogM,error = M[:-right_skip_count],dn_dlogM[:-right_skip_count],error[:-right_skip_count]
    mass_mask = (M>min_mass)
    num_mask = (dn_dlogM>1e-20)
    mask = mass_mask & num_mask
    M,dn_dlogM,error = M[mask],dn_dlogM[mask],error[mask]
    #Deviation


    ax[0].plot(M,dn_dlogM,'-',label= BOX_TEXT + leg,lw=2,color=color,marker=marker)
    if include_deviation:
        osmf = (dn_dlogM)                           # Observed simulation mass function (linear)
        eelmf = Extrapolated_MF(M_st,mfhr_st,M)     # Expected extrapolated litrarture mass function (linear)
        dev_by_fac =  osmf/eelmf
        dev_by_fac_p =  (osmf+0.7*error)/eelmf
        dev_by_fac_n =  (osmf-0.7*error)/eelmf
        ax[1].plot(M,dev_by_fac,'-',color=color)
        ax[1].fill_between(M,dev_by_fac_p,dev_by_fac_n,alpha=0.2,color=color,edgecolor=None)



# --- PLOT ROUTINE



for i,PLOT in enumerate(CURVE_LIST):
    # --- AUTO-FLAGS
    SIM         = PLOT[0]
    PLT_HALO    = Get_Options_List(PLOT[1])
    PLT_TYPE    = Get_Options_List(PLOT[2])
    # ---
    if not ONLY_PIG:
        CFG         = galspec.RockstarCFG(SIM)
        BOX_TEXT    = os.path.basename(CFG.INBASE)
        BOX         = galspec.NavigationRoot(CFG.OUTBASE)
        LINKED_BOX  = galspec.NavigationRoot(CFG.INBASE)
        COSMOLOGY   = BOX.GetCosmology("MassFunctionLitrature")
    if ONLY_PIG : 
        LINKED_BOX  = galspec.NavigationRoot(SIM)
        BOX_TEXT    = PLOT[4]
        # dirty fix
        BOX_TEXT 
        COSMOLOGY   = LINKED_BOX.GetCosmology("MassFunctionLitrature")
    # ---
    if not ONLY_PIG: SNAP = BOX.RSG(SNAP_NUM)
    if ONLY_PIG : SNAP = LINKED_BOX.PART(SNAP_NUM)
    # ---
    REDSHIFT    = (1/SNAP.Attribute.Time())-1
    HUBBLE      = SNAP.Attribute.HubbleParam()
    BOX_SIZE    = (SNAP.Attribute.BoxSize()/1000)
    MASS_UNIT   = 10**10
    MASS_TABLE  = SNAP.Attribute.MassTable()
    if not ONLY_PIG:HALO_DEF    = CFG.MIN_HALO_PARTICLES
    if ONLY_PIG: HALO_DEF = 32
    # ---
    RIGHT_SKIP_FOF  = PLOT[3][0]
    RIGHT_SKIP_RKS  = PLOT[3][1]


    


    # --- MASS FUNCTION PLOTS
    if FOF in PLT_HALO:
        MBT_FOF        = LINKED_BOX.PIG(SNAP_NUM).FOFGroups.MassByType()
        M_GAS,M_DM,M_U1,M_U2,M_STAR,M_BH = numpy.transpose(MBT_FOF) * MASS_UNIT
        # M_BH = LINKED_BOX.PART(SNAP_NUM).BlackHole.BlackholeMass() * MASS_UNIT / HUBBLE
        if DM in PLT_TYPE:
            M, dn_dlogM,error = MassFunction(M_DM,BOX_SIZE,BIN_SIZE)
            PlotBMF(M,dn_dlogM,error,HALO_DEF * MASS_TABLE[1] * MASS_UNIT,RIGHT_SKIP_FOF[0],INCLUDE_DEVIATION,COLORS_FOF[i]," (DM)",marker=" ")
        if GAS in PLT_TYPE:
            M, dn_dlogM,error = MassFunction(M_GAS,BOX_SIZE,BIN_SIZE)
            PlotBMF(M,dn_dlogM,error,HALO_DEF * MASS_TABLE[0] * MASS_UNIT,RIGHT_SKIP_FOF[1],False,COLORS_FOF[i]," (Gas)",marker=".")
        if STAR in PLT_TYPE:
            M, dn_dlogM,error = MassFunction(M_STAR,BOX_SIZE,BIN_SIZE)
            PlotBMF(M,dn_dlogM,error,(HALO_DEF/16) * MASS_TABLE[4] * MASS_UNIT,RIGHT_SKIP_FOF[2],False,COLORS_FOF[i]," (Star)",marker="*")


    # Rockstar
    if ROCKSTAR in PLT_HALO:
        # MVIR        = BOX.RSG(SNAP_NUM).RKSGroups.VirialMass()
        MBT_VIR     = BOX.RSG(SNAP_NUM).RKSGroups.MassByTypeInRvirWC()
        M_GAS,M_DM,M_U1,M_U2,M_STAR,M_BH = numpy.transpose(MBT_VIR)
        if DM in PLT_TYPE:
            M, dn_dlogM,error = MassFunction(M_DM,BOX_SIZE,BIN_SIZE)
            PlotBMF(M,dn_dlogM,error,HALO_DEF * MASS_TABLE[1] * MASS_UNIT,RIGHT_SKIP_RKS[0],False,COLORS_RKS[i]," (DM)",marker=" ")
        if GAS in PLT_TYPE:
            M, dn_dlogM,error = MassFunction(M_GAS,BOX_SIZE,BIN_SIZE)
            PlotBMF(M,dn_dlogM,error,HALO_DEF * MASS_TABLE[0] * MASS_UNIT,RIGHT_SKIP_RKS[1],False,COLORS_RKS[i]," (Gas)",marker=".")
        if STAR in PLT_TYPE:
            M, dn_dlogM,error = MassFunction(M_STAR,BOX_SIZE,BIN_SIZE)
            PlotBMF(M,dn_dlogM,error,(HALO_DEF/8) * MASS_TABLE[4] * MASS_UNIT,RIGHT_SKIP_RKS[2],False,COLORS_RKS[i]," (Star)",marker="*")
        if BH in PLT_TYPE:
            M, dn_dlogM,error = MassFunction(M_BH,BOX_SIZE,BIN_SIZE)
            PlotBMF(M,dn_dlogM,error, 4e5,0,False,COLORS_FOF[i]," (BH)",marker="x")
    
        # log_M, dn_dlogM = MassFunction(MVIR,BOX_SIZE,BIN_SIZE)
        # plt.plot(log_M,dn_dlogM,color="k",label="Virial Mass",lw=2)



# --- BEUTIFY
ax[0].set_xscale('log')
ax[0].set_yscale('log')

ax[0].legend(loc="upper right",ncol=2,title="Dark Matter HMF",fontsize=10,title_fontsize=12,numpoints=2,frameon=False)
# for manual ordering
if False:
    handles, labels = ax[0].get_legend_handles_labels()
    # order = [0,2,1] # coulmn first
    # order = [0,2,1,3] # coulmn first
    # order = [0,2,3,4,1,5,6,7] # coulmn first
    order =[0,3,6,1,4,7,2,5,8]
    oh = [handles[idx] for idx in order]
    ol = [labels[idx] for idx in order]
    ax[0].legend(oh, ol,loc="upper right",ncol=3,title=LEGEND_TITLE,fontsize=10,title_fontsize=12,numpoints=2,frameon=False)

ax[0].set_ylabel("$dn/d\log(M/M_{\odot})$",fontsize=16)
ax[0].grid(alpha=0.3)
# ax[0].set_xlim(left=5*10**5,right=5*10**12)
# ax[0].set_xlim(left=5*10**8,right=5*10**12)

# ax[-1] = ax[0] when deviation not included else ax[1]
ax[-1].set_xlabel("$M/M_{\odot}$",fontsize=16)

if INCLUDE_DEVIATION:
    # ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_ylabel("FoF - ST\nDeviation\nby Factor",fontsize=10)
    ax[1].set_xscale('log')
    ax[1].axhline(1,ls='--',c='k',lw=1)
    ax[1].grid(alpha=0.3)
    # ax[1].set_yscale('log')
    ax[1].set_ylim(0.6,1.5)
    # Direct yscale('log') has issue of hiding default labels and ticks 
    # which is partly from ylim values also. 
    # So as work around we make lin-log conversion
    ticks= [0.8,1,1.25]
    ax[1].set_yticks(ticks,minor=False)
    ax[1].set_yticklabels(["$\\times$ " + str(t) for t in ticks])


# ax[0].set_title(f"HALO MASS FUNCTION (z={numpy.round(REDSHIFT,2)})",fontsize=18,pad=15)
ax[0].set_title(f"HALO MASS FUNCTION\nBOX:L50N640 ; z={numpy.round(REDSHIFT,2)}",fontsize=18,pad=15)
plt.subplots_adjust(hspace=0)

# --- SAVE
# plt.savefig(SAVE_PATH,dpi=300)
plt.show()
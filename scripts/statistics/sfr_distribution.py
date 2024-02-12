import numpy, galspec
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.gridspec import GridSpec


import matplotlib
matplotlib.use('Agg')

# --- SIMULATIONS
BOX         = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640")

# --- FLAGS
SNAP_NUM    = 36
SAVE_PATH   = "/mnt/home/student/cranit/Work/RSGBank/Results/sfr_distribution.png" 
MASS_BINS = numpy.arange(7,13,1)
SFR_BIN_START = -10
SFR_BIN_END = 10
SFR_BIN_NUM = 100

PART_NUM    = 640 # for annonation


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
SFR_BIN_STEP    = ( SFR_BIN_END-SFR_BIN_START ) / SFR_BIN_NUM
# PART_NUM    = SNAP.Attribute.

# --- GET FIELDS
MVIR        = BOX.RSG(SNAP_NUM).RKSGroups.VirialMass()
LBT         = BOX.RSG(SNAP_NUM).RKSGroups.LengthByTypeInRvirWC()
SM          = LBT[:,4]* MASS_TABLE[4]
SFR         = BOX.RSG(SNAP_NUM).RKSGroups.StarFormationRate()

# --- HELPER FUNCTION
def non_zero_sfr_in_halo_mass_range(start,end):
    log10_m = numpy.log10(MVIR)
    sm_mask = ((log10_m>=start) & (log10_m<end))    
    in_range_sfr    = SFR[sm_mask]
    if len(in_range_sfr)==0:return None, None
    in_range_nz_sfr = in_range_sfr[in_range_sfr!=0]
    if len(in_range_nz_sfr)==0:return None, None
    return in_range_nz_sfr,in_range_sfr

def GaussianFit(bin_repr,bin_density):
    def FitFun(x,A,x0,sig):
        A0=1/numpy.sqrt(2*numpy.pi*(sig**2))
        xss=(x-x0)/sig
        return A*A0*numpy.exp(-0.5*(xss**2))
    
    fit_para,fit_err = curve_fit(FitFun,bin_repr,bin_density,p0=[1,0,2])
    A_f=fit_para[0]
    x0_f=fit_para[1]
    sig_f=abs(fit_para[2])  # Complex number case ??

    # High resolution fit curve
    sfr_hr=numpy.linspace(SFR_BIN_START,SFR_BIN_END,SFR_BIN_NUM*10)
    den_hr=FitFun(sfr_hr,A_f,x0_f,sig_f)

    return sfr_hr,den_hr,A_f,x0_f,sig_f

# --- PLOT
def Histogram(ax:plt.Axes,mstart,mend,gaussianfit=True,annotate = True):



    in_range_nz_sfr,in_range_sfr = non_zero_sfr_in_halo_mass_range(mstart,mend)
    if in_range_nz_sfr is None : return

    log10_nz_sfr = numpy.log10(in_range_nz_sfr)

    # !!! Histogram post, pre, mid check
    my_bins = numpy.linspace(SFR_BIN_START,SFR_BIN_END,SFR_BIN_NUM+1)
    counts, bin_edges   = numpy.histogram(log10_nz_sfr,bins=my_bins)
    bin_density         = ( counts / sum(counts) ) / SFR_BIN_STEP
    bin_repr            = bin_edges[:-1]+(SFR_BIN_STEP/2)   # Bin representative
    
    bin_density /= max(bin_density) # Not standard
    

    # Gauusian curve fit - will not be good if too few sfr points or too less spread
    if (len(counts[counts!=0])<5):gaussianfit = False

    if gaussianfit:
        sfr_hr,den_hr,A_f,x0_f,sig_f=GaussianFit(bin_repr,bin_density)


    
    # -- sfr distribution histogram
    # ax.step(bin_edges[:-1],bin_density,lw=1,where='post',color='r',alpha=1)
    
    # --- sfr distribution curve
    # ax.plot(bin_repr,bin_density,'.-',lw=1,color='r')
    
    # --- sfr distribution histogram filled
    ax.fill_between(bin_edges[:-1],bin_density, step="post",color='r', alpha=0.2,zorder=200)

    # high resolution Gaussia fitted curve
    if gaussianfit:
        ax.plot(sfr_hr,den_hr,color='k',lw=1,alpha=1)
        # Mean line
        # ax.axvline(x0_f,color='r',lw=1,ls='--')
        ax.plot(x0_f*numpy.ones(2),[0,max(den_hr)],color='k',lw=1,ls='--',alpha=1)
        # 1-sigma fill
        # ax.fill_between([x0_f-sig_f,x0_f+sig_f],[2,2],color='k', alpha=0.1,ec=None)

    # ax.legend(frameon=False,fontsize=8,title="Halo Mass")

    # Annotate
    if annotate == False: return

    # Mass bin info
    text="$M_{\\text{halo}} \\text{ : } 10^{"+str(mstart) + " - " + str(mend) +"}M_{\odot}$"
    # text+="\n$M_{\\text{*}} \\text{     : } ?? $"
    ax.annotate(text,xy=(ax.get_xlim()[0],ax.get_ylim()[1]),textcoords='offset pixels',xytext=(20,-20),va='top',ha='left',fontsize=10,color='k')

    # fit info
    if gaussianfit:
        text="$\overline{\\text{SFR}}$ : ".ljust(8) + "$10^{" +str(round(x0_f,2)) +"} \\text{ } M_{\odot}/\\text{yr}$"
        text+="\n$\sigma_{\\text{SFR}}$ : ".ljust(8) + str(round(sig_f,2))
    else:
        text="$\overline{\\text{SFR}}$ : ".ljust(8) + "$10^{" +str(numpy.round(numpy.log10(numpy.average(in_range_nz_sfr)),2)) +"} \\text{ } M_{\odot}/\\text{yr}$"
    ax.annotate(text,xy=(ax.get_xlim()[0],ax.get_ylim()[1]),textcoords='offset pixels',xytext=(1000,-20),va='top',ha='left',fontsize=8,color='k')


    # # sfr filter info
    text="$N^{\\text{range}}=$" + str(len(in_range_sfr))
    text+=" (" + '{:.02f}'.format((round((len(in_range_sfr)/len(SFR))*100,2))) + "%" + ")"
    text+="\n$N^{\\text{range}}_{\\text{SFR}\\neq 0}=$" +str(str(len(in_range_nz_sfr)))
    text+=" : ( " + '{:.02f}'.format((round((len(in_range_nz_sfr)/len(in_range_sfr))*100,2))) + "%" + " )"
    ax.annotate(text,xy=(ax.get_xlim()[0],0.65),textcoords='offset pixels',xytext=(20,-20),va='top',ha='left',fontsize=8,color='k',alpha=0.3)


# --- PLOTS
fig = plt.figure(figsize=(8,6))
gs  = GridSpec(len(MASS_BINS)-1, 1, figure=fig,hspace=0.05,bottom=0.1,right=0.90)

ax_list=[]
for i in range(len(MASS_BINS)-1):
    ax = fig.add_subplot(gs[i,0])

    # Axis Costumise - before plot so that annontations get correct lim coordinates
    ax.set_xlim([-8,4])
    ax.set_ylim([0,1.2])
    ax.set_yticks([0,1])
    ax.grid(alpha=0.2)

    Histogram(ax,MASS_BINS[i],MASS_BINS[i+1])

    # Hide xticks except the bottom one
    if i != len(MASS_BINS)-2:
        # ax.set_xticks([]) # Comented as this also hides the grid lines
        ax.set_xticklabels([])
        for tick in ax.xaxis.get_major_ticks():
            tick.tick1line.set_visible(False)
            tick.tick2line.set_visible(False)
            # tick.label1.set_visible(False)    # done by set_xticklabels()
            # tick.label2.set_visible(False)

    ax_list.append(ax)

# --- BEAUTIFY
ax_list[0].set_title("SFR Distribution \n( L="+ str(BOX_SIZE) +"Mpc, N=$" + str(PART_NUM) + "^3, $ z="+str(numpy.round(REDSHIFT,2))+" )",pad=10)
ax_list[-1].set_xlabel("$log_{10}\left(\\frac{SFR}{\\text{??  }M_{\odot} yr^{-1} \\text{  ??}}\\right)$")
fig.text(0.05, 0.5, 'Relative Density', va='center', rotation='vertical',fontsize=12)
fig.text(0.14, 0.9, '$N^{\\text{Box}}_{\\text{halo}}$='+str(len(SFR)), va='center',fontsize=8,alpha=0.3)




# --- SAVE
plt.savefig(SAVE_PATH,dpi=200)

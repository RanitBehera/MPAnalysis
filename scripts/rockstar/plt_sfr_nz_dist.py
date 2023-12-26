import os,numpy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.gridspec import GridSpec,GridSpecFromSubplotSpec

# --- Config
DIR = "/mnt/home/student/cranit/Work/Merger_Tree_WSFR_Mod/RKSG_L50N640c"
REDSHIFT=12
MASS_BINS = numpy.arange(7,13,1)
SFR_BIN_START = -10
SFR_BIN_END = 10
SFR_BIN_NUM = 100
BOX_SIZE = 50 # Mpc
NUM_PART = 640

# --- Derived Config
SNAP_RED_DICT={"016":"12", "020":"11", "024":"10", "030":"9", "036":"8", "050":"6"}
RED_SNAP_DICT={"12":"016", "11":"020", "10":"024", "9":"030", "8":"036", "6":"050"}
SFR_BIN_STEP    = ( SFR_BIN_END-SFR_BIN_START ) / SFR_BIN_NUM

FF_SNAP_NUM = RED_SNAP_DICT[str(REDSHIFT)] # Fixed Format
FILE_NAME = "halos_PART_" + FF_SNAP_NUM + ".0.particles"
FILE_PATH = DIR + os.sep + FILE_NAME

# --- Date Acces
data = numpy.loadtxt(FILE_PATH)
sfr         =   data[:,5]                       # < ---- sfr column number may change in future
halo_mass   =   data[:,0]

def get_nz_sfr_for_mass_range(start,end):
    log10_mh = numpy.log10(halo_mass)
    mask_mass = ((log10_mh>=start) & (log10_mh<end))    
    
    bin_sfr    = sfr[mask_mass]        # length same as selected halos within mass range
    if len(bin_sfr)==0:return None, None

    bin_nz_sfr = bin_sfr[bin_sfr!=0]
    if len(bin_nz_sfr)==0:return None, None
    
        
    return bin_nz_sfr,bin_sfr


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


def PlotAndFit(ax:plt.Axes,mstart,mend,clr="r",fitclr="b",alf=1,annotate=True):
    bin_nz_sfr,bin_sfr=get_nz_sfr_for_mass_range(mstart,mend)
    if bin_nz_sfr is None : return
    log10_nz_sfr = numpy.log10(bin_nz_sfr)

    # !!! Histogram post, pre, mid check
    counts, bin_edges   = numpy.histogram(log10_nz_sfr,bins=numpy.linspace(SFR_BIN_START,SFR_BIN_END,SFR_BIN_NUM+1))
    bin_density         = ( counts / sum(counts) ) / SFR_BIN_STEP
    bin_repr            = bin_edges[:-1]+(SFR_BIN_STEP/2)   # Bin representative
    
    bin_density /= max(bin_density) # Not standard
    

    # Curve fit - will not be good if too few sfr points or too less spread
    # Hence validate
    if (len(counts[counts!=0])>5):
        sfr_hr,den_hr,A_f,x0_f,sig_f=GaussianFit(bin_repr,bin_density)
    else:
        sfr_hr,den_hr,A_f,x0_f,sig_f =[0,0],[0,0],0,0,0
    


    # ====== PLOTS ======
    # -- sfr distribution histogram
    # ax.step(bin_edges[:-1],bin_density,lw=1,color=clr,where='post',alpha=0.9*alf)
    
    # --- sfr distribution curve
    # ax.plot(bin_repr,bin_density,'.-',lw=1,color=clr)
    
    # --- sfr distribution histogram filled
    ax.fill_between(bin_edges[:-1],bin_density, step="post",color=clr, alpha=0.2*alf,zorder=200)

    # high resolution Gaussia fitted curve
    ax.plot(sfr_hr,den_hr,color=fitclr,lw=1,alpha=1*alf)

    # Gauusian Fit Mean line
    # ax.axvline(x0_f,color=fitlcr,lw=1,ls='--')
    ax.plot(x0_f*numpy.ones(2),[0,max(den_hr)],color=fitclr,lw=1,ls='--',alpha=1*alf)
    
    # 1-sigma fill
    # ax.fill_between([x0_f-sig_f,x0_f+sig_f],[1,1],color=fitclr, alpha=0.1*alf,ec=None)

    # ax.legend(frameon=False,fontsize=8,title="Halo Mass")

    # Annotate
    if annotate == False: return

    # Mass bin info
    text="$M_{\\text{halo}} \\text{ : } 10^{"+str(mstart) + " - " + str(mend) +"}M_{\odot}$"
    text+="\n$M_{\\text{*}} \\text{     : } ?? $"
    ax.annotate(text,xy=(ax.get_xlim()[0],ax.get_ylim()[1]),textcoords='offset pixels',xytext=(20,-20),va='top',ha='left',fontsize=8,color='k')

    # fit info
    # text="$\overline{\\text{SFR}}$ : ".ljust(8) + "$10^{" +str(round(x0_f,2)) +"}$"
    # text+="$\sigma_{\\text{SFR}}$ : ".ljust(8) + str(round(sig_f,2))
    # ax.annotate(text,xy=(ax.get_xlim()[0],ax.get_ylim()[1]),textcoords='offset pixels',xytext=(20,-20),va='top',ha='left',fontsize=8,color='k')

    # sfr filter info
    text="$N^{\\text{range}}=$" + str(len(bin_sfr))
    text+=" : ( " + '{:.02f}'.format((round((len(bin_sfr)/len(sfr))*100,2))) + "%" + " )"
    text+="\n$N^{\\text{range}}_{\\text{SFR}\\neq 0}=$" +str(str(len(bin_nz_sfr)))
    text+=" : ( " + '{:.02f}'.format((round((len(bin_nz_sfr)/len(bin_sfr))*100,2))) + "%" + " )"
    ax.annotate(text,xy=(ax.get_xlim()[1],0.75),textcoords='offset pixels',xytext=(20,-20),va='top',ha='left',fontsize=8,color='k')


# Presentation
fig = plt.figure(figsize=(8,6))
gs = GridSpec(len(MASS_BINS)-1, 1, figure=fig,hspace=0.05,bottom=0.1,right=0.75)
ax_list=[]
for i in range(len(MASS_BINS)-1):
    ax = fig.add_subplot(gs[i,0])

    # Axis Costumise - before plot so that annontations get correct lim coordinates
    ax.set_xlim([-6,3])
    ax.set_ylim([0,1.2])
    ax.set_yticks([0,1])
    ax.grid(alpha=0.2)

    PlotAndFit(ax,MASS_BINS[i],MASS_BINS[i+1])
    PlotAndFit(ax,MASS_BINS[0],MASS_BINS[-1],'k','k',0.2,False)

    if i != len(MASS_BINS)-2:
        # ax.set_xticks([])
        ax.set_xticklabels([])
        for tick in ax.xaxis.get_major_ticks():
            tick.tick1line.set_visible(False)
            tick.tick2line.set_visible(False)
            # tick.label1.set_visible(False)    # done by set_xticklabels()
            # tick.label2.set_visible(False)

    ax_list.append(ax)

ax_list[0].set_title("Mass binned non-zero SFR Distribution \n( L="+ str(BOX_SIZE) +"Mpc, N=$" + str(NUM_PART) + "^3, $ z="+str(REDSHIFT)+" )",pad=10)
ax_list[-1].set_xlabel("$log_{10}\left(\\frac{SFR}{\\text{??  }M_{\odot} yr^{-1} \\text{  ??}}\\right)$")
fig.text(0.05, 0.5, 'Relative Density', va='center', rotation='vertical',fontsize=12)
fig.text(0.81, 0.9, '$N^{\\text{Box}}$='+str(len(sfr)), va='center',fontsize=8)

plt.savefig("/mnt/home/student/cranit/Work/Merger_Tree_WSFR_Mod/Results/sfr_dist_z"+ str(REDSHIFT)+".png",dpi=200)
plt.savefig("/mnt/home/student/cranit/Work/Merger_Tree_WSFR_Mod/Results/sfr_dist_z"+ str(REDSHIFT) +".svg")
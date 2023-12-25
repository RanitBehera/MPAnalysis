import os,numpy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# --- Config
DIR = "/mnt/home/student/cranit/Work/Merger_Tree_WSFR_Mod/RKSG_L50N640c"
REDSHIFT=8
MASS_BINS = numpy.arange(7,13,1)
SFR_BIN_START = -10
SFR_BIN_END = 10
SFR_BIN_NUM = 100
COLORS = []


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
    
    selected_sfr    = sfr[mask_mass]        # length same as selected halos within mass range
    if len(selected_sfr)==0:return None, None

    selected_nz_sfr = selected_sfr[selected_sfr!=0]
    if len(selected_nz_sfr)==0:return None, None
    
    nz_sfr_fraction = len(selected_nz_sfr)/len(selected_sfr)    
    return selected_nz_sfr , nz_sfr_fraction

def PlotAndFit(ax:plt.Axes,mstart,mend):
    nz_sfr,nz_sfr_frac=get_nz_sfr_for_mass_range(mstart,mend)
    if nz_sfr is None : return
    log10_nz_sfr = numpy.log10(nz_sfr)


    # !!! Histogram post, pre, mid check
    counts, bin_edges   = numpy.histogram(log10_nz_sfr,bins=numpy.linspace(SFR_BIN_START,SFR_BIN_END,SFR_BIN_NUM+1))
    bin_density         = ( counts / sum(counts) ) / SFR_BIN_STEP
    bin_repr            = bin_edges[:-1]+(SFR_BIN_STEP/2)   # Bin representative
    

    # info texts
    non_zero_percentage_text='{:.02f}'.format((round(nz_sfr_frac*100,2))) + "%"
    label_text="z=" + str(REDSHIFT).rjust(2) + " ($SFR_{\\neq 0}:$" + non_zero_percentage_text + ")"

    # Plots
    # sfr distribution histogram
    ax.step(bin_edges[:-1],bin_density,lw=1,color='r',where='post',alpha=0.9)
    # sfr distribution histogram filled
    ax.fill_between(bin_edges[:-1],bin_density, step="post",color='r', alpha=0.2,label=label_text,zorder=200)
    # sfr distribution pointes conncted by lines instead of step as in histogram
    # ax.plot(bin_repr,bin_density,lw=1,label=label_text)





    # Curve fit - will not work if too few sfr points or too less spread
    # Hence validate
    if (len(counts[counts!=0])<5):
        return  # return a means and variance

    # Curve Fit Gaussian
    def FitFun(x,A,x0,sig):
        A0=1/numpy.sqrt(2*numpy.pi*(sig**2))
        xss=(x-x0)/sig
        return A*A0*numpy.exp(-0.5*(xss**2))
    
    fit_para,fit_err = curve_fit(FitFun,bin_repr,bin_density,p0=[1,0,2])
    A_f=fit_para[0]
    x0_f=fit_para[1]
    sig_f=abs(fit_para[2])

    # High resolution fit curve
    sfr_hr=numpy.linspace(SFR_BIN_START,SFR_BIN_END,SFR_BIN_NUM*10)
    den_hr=FitFun(sfr_hr,A_f,x0_f,sig_f)


    # Plots in order
    # high resolution fitted curve
    ax.plot(sfr_hr,den_hr,color='b',lw=1)
    # 1-sigma fill
    ax.fill_between([x0_f-sig_f,x0_f+sig_f],[1,1],color='b', alpha=0.1,ec=None)
    # Mean line
    ax.axvline(x0_f,color='b',lw=1,ls='--')
   

    # leg=ax.legend(frameon=False,fontsize=8)


# Presentation
fig,ax = plt.subplots()
for i in range(len(MASS_BINS)-1):
    PlotAndFit(ax,MASS_BINS[i],MASS_BINS[i+1])



ax.set_xlim([-6,3])


plt.savefig("/mnt/home/student/cranit/Work/Merger_Tree_WSFR_Mod/Results/sfr_dist.png",dpi=200)
plt.savefig("/mnt/home/student/cranit/Work/Merger_Tree_WSFR_Mod/Results/sfr_dist.svg")
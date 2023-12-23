import numpy,os
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec,GridSpecFromSubplotSpec
from matplotlib import axis
from scipy.optimize import curve_fit

import matplotlib
matplotlib.use('Agg')

DIR = "/mnt/home/student/cranit/Work/Merger_Tree_WSFR_Mod/RKSG_L50N640c"
SNAP_RED_DICT={"016":"12", "020":"11", "024":"10", "030":"9", "036":"8", "050":"6"}
BIN_START   = -10
BIN_STOP    = 10
BIN_NUM     = 100
BIN_STEP    = ( BIN_STOP-BIN_START ) / BIN_NUM
LEFT_XLIM        = [-5,0]


def PlotSFR(ax:plt.Axes,snap_num:int):
    fixed_format_snap_num='{:03}'.format(snap_num)
    FILE_NAME = "halos_PART_" + fixed_format_snap_num + ".0.particles"
    FILE_PATH = DIR + os.sep + FILE_NAME

    data = numpy.loadtxt(FILE_PATH)
    sfr=data[:,5]                       # < ---- sfr column number may change in future
    sfr_nz=sfr[sfr!=0]
    non_zero_fraction = len(sfr_nz)/len(sfr)
    log10_sfr_nz = numpy.log10(sfr_nz)

    # !!! Histogram post, pre, mid check
    counts, bin_edges   = numpy.histogram(log10_sfr_nz,bins=numpy.linspace(BIN_START,BIN_STOP,BIN_NUM+1))
    bin_density         = ( counts / sum(counts) ) / BIN_STEP
    bin_repr            = bin_edges[:-1]+(BIN_STEP/2)

    # Curve Fit Gaussian
    def FitFun(x,A,x0,sig):
        A0=1/numpy.sqrt(2*numpy.pi*(sig**2))
        xss=(x-x0)/sig
        return A*A0*numpy.exp(-0.5*(xss**2))

    fit_para,fit_err = curve_fit(FitFun,bin_repr,bin_density,p0=[0.5,-2.5,2])
    
    A_f=fit_para[0]
    x0_f=fit_para[1]
    sig_f=abs(fit_para[2])
    # High resolution fit curve
    sfr_hr=numpy.linspace(BIN_START,BIN_STOP,BIN_NUM*10)
    den_hr=FitFun(sfr_hr,A_f,x0_f,sig_f)


    # Plots in order
    non_zero_percentage_text='{:.02f}'.format((round(non_zero_fraction*100,2))) + "%"
    label_text="z=" + (SNAP_RED_DICT[fixed_format_snap_num]).rjust(2) + " ($SFR_{\\neq 0}:$" + non_zero_percentage_text + ")"

    ax.plot(sfr_hr,den_hr,color='b',lw=1)
    ax.fill_between([x0_f-sig_f,x0_f+sig_f],[1,1],color='b', alpha=0.1,ec=None)
    ax.axvline(x0_f,color='b',lw=1,ls='--')

    ax.step(bin_edges[:-1],bin_density,lw=1,color='r',where='post',alpha=0.9)
    ax.fill_between(bin_edges[:-1],bin_density, step="post",color='r', alpha=0.2,label=label_text,zorder=200)
    # ax.plot(bin_repr,bin_density,lw=1,label=label_text)

    leg=ax.legend(frameon=False,fontsize=8)

    ann_text=""
    ann_text += "$\overline{\\text{SFR}}$ : ".ljust(8) + "$10^{" +str(round(x0_f,2)) +"}$\n"
    ann_text += "$\sigma_{\\text{SFR}}$ : ".ljust(8) + str(round(sig_f,2))

    ax.annotate(ann_text,xy=(LEFT_XLIM[0],1),textcoords='offset pixels',xytext=(20,-20),va='top',ha='left',fontsize=8,color='b')

    return [float(SNAP_RED_DICT[fixed_format_snap_num]),x0_f,sig_f]


# --- Presentation

fig = plt.figure(figsize=(12,6))

gs_root = GridSpec(1, 2, figure=fig,left=0.06,right=0.95)
gs_sub  = GridSpecFromSubplotSpec(6,1,subplot_spec=gs_root[0],hspace=0.20)

ax_left =[]
for i in range(6):
    ax = fig.add_subplot(gs_sub[i,0])
    ax.set_xlim(LEFT_XLIM)
    ax.set_ylim([0,1])
    ax.set_xticks([])
    ax.set_yticks([0,1])
    ax_left.append(ax)
    
ax_left[0].set_title("Gaussian curve fit on SFR distribution")
ax_left[5].set_xticks(numpy.arange(-5,1,1))
ax_left[5].set_xlabel("$log_{10}\left(\\frac{SFR}{\\text{??  }M_{\odot} yr^{-1} \\text{  ??}}\\right)$")
fig.text(0.02, 0.5, 'Density', va='center', rotation='vertical',fontsize=12)


data=[]     # [redshift,mean_sfr,std_sfr] in order returned from PlotSFR()

data.append(PlotSFR(ax_left[0],16))
data.append(PlotSFR(ax_left[1],20))
data.append(PlotSFR(ax_left[2],24))
data.append(PlotSFR(ax_left[3],30))
data.append(PlotSFR(ax_left[4],36))
data.append(PlotSFR(ax_left[5],50))

z,mean_sfr,std_sfr = numpy.array(data).T

ax_right=fig.add_subplot(gs_root[0,1])
ax_right.plot(z,mean_sfr,'.-',color="b")
ax_right.fill_between(x=z,y1=mean_sfr+std_sfr,y2=mean_sfr-std_sfr,color="b",alpha=0.1,ec=None)
ax_right.invert_xaxis()

ax_right.set_xlabel("Redshift")
ax_right.set_ylabel("$log_{10}\left(\\frac{SFR}{\\text{??  }M_{\odot} yr^{-1} \\text{  ??}}\\right)$")
ax_right.set_title("SFR vs Redshift")

# plt.tight_layout()
plt.savefig("/mnt/home/student/cranit/Work/Merger_Tree_WSFR_Mod/Results/sfr_hist.png",dpi=200)
plt.savefig("/mnt/home/student/cranit/Work/Merger_Tree_WSFR_Mod/Results/sfr_hist.svg")





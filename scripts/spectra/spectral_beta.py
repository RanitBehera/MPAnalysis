import numpy,os
import matplotlib.pyplot as plt
import bagpipes as pipes
import galspec

SAVED_PATH = "/mnt/home/student/cranit/Work/RSGBank/TBSFR_Bank"

# PLOT
def PlotSpectra_and_GetSpectralBeta(offset):
    filepath = os.path.join(SAVED_PATH,"off_"+str(offset)+".txt")
    lbage,sfh = numpy.loadtxt(filepath).T
    with open(filepath) as f:
        header = f.readline()
    mass_fromed = float(header.split("*")[-1])

    # Validation
    if(mass_fromed==-numpy.inf):return offset,0
    if(len(sfh[sfh!=0]))==0:return offset,0

    # ===================== BAGPIPES
    goodss_filt_list = numpy.loadtxt("/mnt/home/student/cranit/Repo/MPAnalysis/oldscripts/bagpipes/filters/myfilters.txt", dtype="str")

    dust = {"type":"Calzetti","Av":0.0,"eta":3.}                         
    nebular = {"logU":-3}                             

    custom = {}
    custom["history"] = numpy.column_stack((lbage,sfh))
    custom["massformed"] =  mass_fromed  # Log_10 total stellar mass formed: M_Solar.
    custom["metallicity"] = 0.1

    model_components = {}                   
    model_components["redshift"] = 8
    # model_components["t_bc"] = 0.01         
    # model_components["veldisp"] = 200. 
    model_components["custom"] = custom
    model_components["dust"] = dust
    model_components["nebular"] = nebular

    # spectral index
    ref_start = 1300*(1+8)
    ref_end = 2000*(1+8)
    log_ref_start = numpy.log10(ref_start)
    log_ref_end = numpy.log10(ref_end)
    # model = pipes.model_galaxy(model_components, filt_list=goodss_filt_list,spec_wavs=numpy.logspace(4,4.2,10000))
    model = pipes.model_galaxy(model_components, filt_list=goodss_filt_list,spec_wavs=numpy.logspace(log_ref_start,log_ref_end,100000))
    # model = pipes.model_galaxy(model_components,spec_wavs=numpy.logspace(4,4.2,10000))

    # --- SFH
    # --- SPEC
    wv = 1450 *(1+8)

    fig,axes,yscale = model.plot(show=False)
    # fig,axes,yscale = model.plot_full_spectrum()
    # exit()

    # print(axes[1].collections[0].get_offsets())
    axes[1].axvline(log_ref_start,lw=1,ls='--',color='k')
    axes[1].axvline(log_ref_end,lw=1,ls='--',color='k')
    axes[1].fill_between([log_ref_start,log_ref_end],axes[1].get_ylim()[0]*numpy.ones(2),axes[1].get_ylim()[1]*numpy.ones(2),color='k',alpha=0.08,ec=None)
    axes[1].lines[0].set_color('b')


    # --- Luminosity
    waves = axes[0].lines[0].get_xdata()
    f_lam  = axes[0].lines[0].get_ydata()

    axes[0].set_xscale('log')

    Y= numpy.log10(f_lam*(10**yscale))
    X= numpy.log10(waves*1e-10)
    slope=(Y[-1]-Y[0])/(X[-1]-X[0])
    # print(slope)

    axes[0].plot([waves[0],waves[-1]],[f_lam[0],f_lam[-1]],'k--',zorder = 10,lw=1,label = "UV slope $\\beta=$"+str(round(slope,2)))
    axes[0].legend(loc='lower center',fontsize=12)


    plt.suptitle("UV slope using rest-frame wavelength [1300,2000] redshifted by 8")


    # plt.show()
    # plt.savefig(SAVE_PATH,dpi=200)
    # plt.savefig("/mnt/home/student/cranit/Repo/MPAnalysis/temp/plots_mar9/UV_slope_Av_01.png",dpi=300)
    plt.close()
    return offset, slope

# --- Single Halo
# a,b=PlotSpectra_and_GetSpectralBeta(68)

# plt.savefig(SAVED_PATH + "/test5.png",dpi=300)

# --- Multiple Halo Single Core
if True:
    N=1000
    table=numpy.zeros((N,3))
    for offset in range(N):
        print(offset+1,"/",N,end='',flush=True)
        halo_offset,beta = PlotSpectra_and_GetSpectralBeta(offset)
        table[offset,0]=halo_offset
        table[offset,1]=beta
        print(" : Done",flush=True)
    
    # top N halos stellar mass
    box = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640")
    mvir_sort = numpy.argsort(box.RSG(36).RKSGroups.VirialMass())[::-1]    
    mbt = box.RSG(36).RKSGroups.MassByTypeInRvirWC()[mvir_sort]
    stellar_mass = mbt[:N,4]
    table[:,2]=stellar_mass

    mask = (table[:,1]==0)
    out_list = table[~mask]


    OUT_DIR = os.path.join("/mnt/home/student/cranit/Repo/MPAnalysis/temp/UV_SLOPE","UV_slope_Av_00.txt")

    numpy.savetxt(OUT_DIR,out_list,header="Halo_offset UV_Slope (beta) Stellar_Mass(M0)",fmt="%d %f %e")
    print("Saved :",OUT_DIR,flush=True)










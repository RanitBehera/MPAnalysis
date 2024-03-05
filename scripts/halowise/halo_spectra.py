import numpy,os
import matplotlib.pyplot as plt
import bagpipes as pipes


SAVED_PATH = "/mnt/home/student/cranit/Work/RSGBank/TBSFR_Bank"

# PLOT
def PlotSpectra_and_GetLuminosity(offset):
    filepath = os.path.join(SAVED_PATH,"off_"+str(offset)+".txt")
    lbage,sfh = numpy.loadtxt(filepath).T
    with open(filepath) as f:
        header = f.readline()
    mass_fromed = float(header.split("*")[-1])

    # Validation
    if(mass_fromed==-numpy.inf):return offset,0, sfh[0]
    if(len(sfh[sfh!=0]))==0:return offset,0, sfh[0]

    # age_width = [(lbage[i+1] - lbage[i]) for i in range(len(lbage)-1)]
    # mass_fromed_2 =  numpy.log10(numpy.sum(age_width*sfh[1:]))

    # print(mass_fromed,mass_fromed_2)

    # ===================== BAGPIPES
    goodss_filt_list = numpy.loadtxt("/mnt/home/student/cranit/Repo/MPAnalysis/oldscripts/bagpipes/filters/myfilters.txt", dtype="str")

    dust = {"type":"Calzetti","Av":0.2,"eta":3.}                         
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

    model = pipes.model_galaxy(model_components, filt_list=goodss_filt_list,spec_wavs=numpy.logspace(4,4.2,10000))
    # model = pipes.model_galaxy(model_components,spec_wavs=numpy.logspace(4,4.2,10000))

    # --- SFH
    # sfh_fig,sfh_ax = model.sfh.plot()
    # xdata=sfh_ax.lines[0].get_xdata()
    # ydata=sfh_ax.lines[0].get_ydata()
    # print("Max Input :",numpy.max(sfh))
    # print("Max (Bagpipes) :",numpy.max(ydata))
    # plt.savefig(SAVE_PATH,dpi=200)

    # --- SPEC
    wv = 1450 *(1+8)

    fig,axes,yscale = model.plot(show=False)
    # fig,axes,yscale = model.plot_full_spectrum()
    # exit()

    # print(axes[1].collections[0].get_offsets())

    axes[1].fill_between([4,4.2],axes[1].get_ylim()[0]*numpy.ones(2),axes[1].get_ylim()[1]*numpy.ones(2),color='k',alpha=0.08,ec=None)
    axes[1].lines[0].set_color('b')
    axes[1].axvline(numpy.log10(wv),color='k',lw=1)
    axes[0].axvline(wv,color='k',lw=1)

    # --- Luminosity
    waves = axes[0].lines[0].get_xdata()
    lums  = axes[0].lines[0].get_ydata()

    lum   = lums[numpy.argmin(numpy.abs(waves-wv))]
    axes[0].axhline(lum,color='k',ls='--',lw=1)
    axes[0].annotate(str(numpy.round(lum,2)),xy=(axes[0].get_xlim()[0],lum),xycoords='data',xytext=(5,5),textcoords='offset points',fontsize=10,c='k')

    plt.show()
    # plt.savefig(SAVE_PATH,dpi=200)
    plt.close()
    return offset, lum * 10**yscale,sfh[0]  #erg s-1 cm-2 A-1,M0 yr-1

# --- Single Halo
PlotSpectra_and_GetLuminosity(0)
# plt.savefig(SAVED_PATH + "/test5.png",dpi=300)

# --- Multiple Halo Single Core
if False:
    table=numpy.zeros((1000,3))
    for offset in range(1000):
        print(offset+1,"/",1000,end='',flush=True)
        off,lum,sfr = PlotSpectra_and_GetLuminosity(offset)
        table[offset,0]=off
        table[offset,1]=lum
        table[offset,2]=sfr
        print(" : Done",flush=True)
    
    mask = (table[:,1]==0)
    out_list = table[~mask]

    OUT_DIR = os.path.join(SAVED_PATH,"luminosities.txt")
    numpy.savetxt(OUT_DIR,out_list,header="Luminosity(erg s-1 cm-2 ang-1) SFR(M0 yr-1)")
    print("Saved :",OUT_DIR,flush=True)


# --- Multiple Halo Multiple Core Core
# print("Starting")
# from multiprocessing import Pool
# if False:
#     def Compute(Offset):
#             return PlotSpectra_and_GetLuminosity(Offset)
    
#     if __name__ == '__main__':
#         with Pool(20) as p:
#             offsets = numpy.arange(0,1000,1)
#             lum_list=p.map(Compute,offsets)
#         OUT_DIR = os.path.join(SAVED_PATH,"luminosities.txt")
#         numpy.savetxt(OUT_DIR,numpy.row_stack((lum_list)),header="Unit : erg s-1 cm-2 ng-1")
#         print("Saved :",OUT_DIR,flush=True)








import numpy,os
import matplotlib.pyplot as plt
import galspec
import bagpipes as pipes
from bagpipes.plotting.general import add_z_axis
from scipy.optimize import curve_fit

# --- FLAGS
TBSFR_DIR = "/mnt/home/student/cranit/Work/RSGBank/TBSFR_Bank"
SHOW_SFH_FIGURE     = False
SHOW_SPECTRA_FIGURE = True
REDSHIFT = 8
WAVELENGTH_RANGE = numpy.logspace(4,4.5,10000) # In observed frame
REST_FRAME = True # Shift to rest frame
FLUX_UNIT = 1e-20 # In ergs s-1 cm-2 A-1 # Keep the exponent integer
UV_START        = 1350 # In Angstorm (Rest Frame)
UV_STOP         = 2800 # In Angstorm (Rest Frame)
UV_REPRESENT    = 1500 # In Angstorm (Rest Frame)
DATA_SAVE_PATH  = "/mnt/home/student/cranit/Repo/MPAnalysis/temp/spectra/bagdata.txt"

# --- Automate
if not REST_FRAME:
    UV_START        *= (1+REDSHIFT)
    UV_STOP         *= (1+REDSHIFT)
    UV_REPRESENT    *= (1+REDSHIFT)


def GetBagpipes(offset,ShowPlot=True):
    # Read star formation history
    sfhfilepath = os.path.join(TBSFR_DIR,"off_"+str(offset)+".txt")
    lbage,sfh = numpy.loadtxt(sfhfilepath).T

    # Get mass formed from header
    # Bagpipes wants Log_10 total stellar mass formed in M_Solar
    with open(sfhfilepath) as f:
        header = f.readline()
    mass_formed = float(header.split("*")[-1])

    # Validate for invalid sfh
    invalid_return = [-1, mass_formed, sfh[0], 0, 0]
    if (mass_formed==-numpy.inf): return invalid_return
    if(len(sfh[sfh!=0]))==0:return invalid_return

    # --- Bagpipes : Mandatory
    custom = {"massformed":mass_formed,"metallicity":0.1}
    custom["history"] = numpy.column_stack((lbage,sfh))
    
    # --- Bagpipes : Create Model
    model_components = {}                   
    model_components["redshift"] = REDSHIFT
    model_components["custom"] = custom

    # --- Bagpipes : Extra
    # model_components["t_bc"] = 0.01         
    # model_components["veldisp"] = 200. 
    # dust = {"type":"Calzetti","Av":0.2,"eta":3.}                         
    # model_components["dust"] = dust
    # nebular = {"logU":-3}
    # model_components["nebular"] = nebular

    # --- Bagpipes : Generate Spectra
    model = pipes.model_galaxy(model_components,spec_wavs=WAVELENGTH_RANGE)

    # Get Bagpipes internal quanties which it plots from codes
    # For SFH : model.sfh.plot()
    _sfh = model.sfh
    lookback_age = (_sfh.age_of_universe - _sfh.ages)*10**-9
    lookback_sfh = _sfh.sfh
    # for FLUX : model.plot()
    _spectrum = model.spectrum
    wave = _spectrum[:, 0]
    flux = _spectrum[:, 1]/FLUX_UNIT    # observed (spectral) flux (density) 
    if REST_FRAME:
        wave /= (1+REDSHIFT)



    # Plots
    if SHOW_SFH_FIGURE:
        fig = plt.figure(figsize=(12, 4))
        ax = plt.subplot()
        ax.plot(lookback_age,lookback_sfh)
        ax.set_xlim(_sfh.age_of_universe*10**-9, 0.)
        ax.set_ylim(bottom=0.)
        ax.set_xlabel("$\\mathrm{Age\\ of\\ Universe\\ /\\ Gyr}$")
        ax.set_ylabel("$\\mathrm{SFR\\ /\\ M_\\odot\\ \\mathrm{yr}^{-1}}$")
        add_z_axis(ax,zvals=[0, 0.5, 1, 2, 4, 10])
    
    if SHOW_SPECTRA_FIGURE:
        fig = plt.figure(figsize=(12, 4))
        ax = plt.subplot()
        ax.plot(wave,flux)
        ax.set_ylim(bottom=0.)
        ax.set_ylabel("$f_{\lambda}/ 10^{"+ str(int(numpy.log10(FLUX_UNIT))) +"}\\text{erg s}^{-1} \\text{cm}^{-2} \\AA^{-1} $")
        if REST_FRAME:ax.set_xlabel("Rest Frame $\lambda / \\AA$")
        else:ax.set_xlabel("Observed Frame $\lambda / \\AA$")
        
        if True: # Shading
            # Shade UV range considered for UV slope
            # ax.axvline(UV_START,color='k',ls='--')
            # ax.axvline(UV_STOP,color='k',ls='--')
            ax.fill_between([UV_START,UV_STOP],ax.get_ylim()[0]*numpy.ones(2),ax.get_ylim()[1]*numpy.ones(2),color='k',alpha=0.08,ec=None)
            # Highlight UV representative
            ax.axvline(UV_REPRESENT,color='k',ls='--',lw=1)

        if True: # Fitting
            # f = f0(lam/lam0)**beta

            # take a representative point for over all normalisation initialisation
            lam_ref=UV_REPRESENT
            ind_ref = numpy.argmin(numpy.abs(wave-lam_ref))
            f_ref = numpy.average(flux[ind_ref-10:ind_ref+10])
            # plt.plot(lam_ref,f_ref,'.k',ms=10)

            #  give only the uv range data for fitting
            ind_uv_start = numpy.argmin(numpy.abs(wave-UV_START))
            ind_uv_end = numpy.argmin(numpy.abs(wave-UV_STOP))
            wave_uv = wave[ind_uv_start:ind_uv_end]
            flux_uv = flux[ind_uv_start:ind_uv_end]

            def fitfun(wave,beta,f0):
                return f0*numpy.power(wave/lam_ref,beta)
            pvar,pcov = curve_fit(fitfun,wave_uv,flux_uv,[-2,f_ref])

            fitted_flux_uv = fitfun(wave_uv,pvar[0],pvar[1])
            plt.plot(wave_uv,fitted_flux_uv,'-r',lw=2)

            beta_uv= pvar[0]
            f_uv = fitted_flux_uv[numpy.argmin(numpy.abs(wave_uv-UV_REPRESENT))]

            plt.plot(UV_REPRESENT,f_uv,'.r',ms=10)
            plt.plot([plt.xlim()[0],UV_REPRESENT],f_uv*numpy.ones(2),'--r',lw=1)

        if True:
            plt.annotate("$\\beta_{\\text{UV}}$="+str(numpy.round(beta_uv,2)),
                         xy=(1,1),xytext=(-10,-10),xycoords="axes fraction",textcoords="offset pixels",fontsize=12,
                         ha="right",va="top")
            
            plt.annotate("$f_{\lambda,\\text{UV}}$="+str(numpy.round(f_uv,2)),
                         xy=(1,1),xytext=(-10,-32),xycoords="axes fraction",textcoords="offset pixels",fontsize=12,
                         ha="right",va="top")
            

    plt.margins(x=0,y=0)
    if ShowPlot:plt.show()
    plt.close()
    
    return offset, mass_formed, sfh[0], beta_uv, f_uv*FLUX_UNIT

# Single Call
# GetBagpipes(10)

# Dump Data for all
N=1000
table = numpy.zeros([N,5])
for offset in range(N):
    print(offset+1,"/",N,end='',flush=True)
    table[offset,:] = GetBagpipes(offset,False)
    print(" : Done",flush=True)

table = table[table[:,0]>0]

header = "Redshift ="+str(REDSHIFT)
header += "\nUV Start = " + str(UV_START)
header += "\nUV Stop = " + str(UV_STOP)
header += "\nUV Represent = " + str(UV_REPRESENT)
header += "\n(0)Halo Offset with virial mass sort"
header += "\n(1)Stellar mass formed : Log10(M/M_solar)"
header += "\n(2)Star formation rate : (M/M_solar)/yr"
header += "\n(3)Beta UV Slope"
header += "\n(4)Observed UV Luminosity : erg s-1 cm-2 AA-1"


numpy.savetxt(DATA_SAVE_PATH,table,header=header,fmt="%d %f %e %f %e")
print("Saved :",DATA_SAVE_PATH,flush=True)
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
WAVELENGTH_RANGE = numpy.logspace(3,4.5,100000) # In observed frame
REST_FRAME = True # Shift to rest frame
FLUX_UNIT = 1e-20 # In ergs s-1 cm-2 A-1 # Keep the exponent integer
UV_START        = 1350 # In Angstorm (Rest Frame)
UV_STOP         = 2800 # In Angstorm (Rest Frame)
UV_REPRESENT    = 1500 # In Angstorm (Rest Frame)
DATA_SAVE_PATH  = "/mnt/home/student/cranit/Repo/MPAnalysis/temp/spectra/bagdata_Av_M.txt"

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
    mass_formed = float(header.split("*")[-1])  # this is in log

    # Validate for invalid sfh
    invalid_return = [-1, mass_formed, sfh[0], 0, 0,0]
    if (mass_formed==-numpy.inf): return invalid_return
    if(len(sfh[sfh!=0]))==0:return invalid_return

    # --- Bagpipes : Mandatory
    custom = {"massformed":mass_formed,"metallicity":(numpy.random.random()*0.9)+0.1}
    custom["history"] = numpy.column_stack((lbage,sfh))
    
    # --- Bagpipes : Create Model
    model_components = {}                   
    model_components["redshift"] = REDSHIFT
    model_components["custom"] = custom

    if True:
        pass
        # burst = {"massformed":4,"metallicity":0.1}
        # burst["age"] = 0.4
        # model_components["burst"] = burst

        # constant = {"massformed":10,"metallicity":0.1}
        # constant["age_max"] = 0.6
        # constant["age_min"] = 0.0
        # model_components["constant"] = constant

        # exponential = {"massformed":10,"metallicity":0.1}
        # exponential["age"] = 0.5
        # exponential["tau"] = 0.1
        # model_components["exponential"] = exponential

        # delayed = {"massformed":10,"metallicity":0.1}
        # delayed["age"] = 0.6
        # delayed["tau"] = 0.1
        # model_components["delayed"] = delayed

    def get_Av(mass):   # currently mass is in log
        Av=0.01*((mass-6)**4)
        return Av

    # --- Bagpipes : Extra
    # model_components["t_bc"] = 0.01         
    # model_components["veldisp"] = 200. 
    Av = get_Av(mass_formed)
    dust = {"type":"Calzetti","Av":Av,"eta":3.}                         
    model_components["dust"] = dust
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
        
        def ShadeUVRegion(): # Shading
            # Shade UV range considered for UV slope
            # ax.axvline(UV_START,color='k',ls='--')
            # ax.axvline(UV_STOP,color='k',ls='--')
            ax.fill_between([UV_START,UV_STOP],ax.get_ylim()[0]*numpy.ones(2),ax.get_ylim()[1]*numpy.ones(2),color='k',alpha=0.08,ec=None)
            # Highlight UV representative
            ax.axvline(UV_REPRESENT,color='k',ls='--',lw=1)

        if True: # Fitting
            # take a representative point for over all normalisation
            wave_lower=UV_START
            wave_upper=UV_STOP
            wave_refer=UV_REPRESENT

            index_refer = numpy.argmin(numpy.abs(wave-wave_refer))
            flux_refer = numpy.average(flux[index_refer-10:index_refer+10])
            # plt.plot(lam_ref,f_ref,'.k',ms=10)

            # Find Continuum
            def get_continuum(wave_data,flux_data):
                span = 100
                flux_cont = []
                wave_cont = []
                for i in range(span,len(wave_data)-span):
                    # if wave[i]<1250 or wave[i]>1900 : continue
                    if False:
                        if (wave[i]>1520 and wave[i]<1570) :continue

                    chunk=flux_data[i-span:i+span+1]
                    chunk_avg=numpy.average(chunk)
                    rel_offset = chunk-chunk_avg

                    # sumy = numpy.sum(chunk*numpy.exp(-rel_offset**2/0.0001))
                    # sumy/= numpy.sum(numpy.exp(-rel_offset**2/0.0001))

                    sumy = numpy.sum(chunk*numpy.exp(rel_offset/0.01))
                    sumy/= numpy.sum(numpy.exp(rel_offset/0.01))


                    flux_cont.append(sumy)
                    wave_cont.append(wave[i])
                

                wave_cont = numpy.array(wave_cont)
                flux_cont = numpy.array(flux_cont)
                return wave_cont,flux_cont
            
            wave, flux = get_continuum(wave,flux)
            plt.plot(wave,flux)
   
            #  give only the uv range data for fitting
            ind_uv_start = numpy.argmin(numpy.abs(wave-wave_lower))
            ind_uv_end = numpy.argmin(numpy.abs(wave-wave_upper))
            wave_uv = wave[ind_uv_start:ind_uv_end]
            flux_uv = flux[ind_uv_start:ind_uv_end]

            wave_uv_hr = numpy.linspace(wave_lower,wave_upper,1000)

            if False : # Linear
                # f = f0*(lam/lam0)^beta
                def fitfun(wave,beta,f0):
                    return f0*numpy.power(wave/wave_refer,beta)
                pvar,pcov = curve_fit(fitfun,wave_uv,flux_uv,[-2.5,flux_refer])
                fitted_flux_uv_hr = fitfun(wave_uv_hr,pvar[0],pvar[1])

            else : # Logarithimic
                # log f = beta * log(lam/lam0) + log(f0)
                # y = beta * log (x/x0) + y0 
                def fitfun(wave,beta,y0):
                    return beta * numpy.log10(wave/wave_refer) + y0 
                pvar,pcov = curve_fit(fitfun,wave_uv,numpy.log10(flux_uv),[-2.5,numpy.log10(flux_refer)])
                log_fitted_flux_uv_hr = fitfun(wave_uv_hr,pvar[0],pvar[1])
                fitted_flux_uv_hr = 10**log_fitted_flux_uv_hr
                

            
            plt.plot(wave_uv_hr,fitted_flux_uv_hr,'-r',lw=2)

            beta_uv= pvar[0]
            f_uv = fitted_flux_uv_hr[numpy.argmin(numpy.abs(wave_uv_hr-wave_refer))]

            plt.plot(wave_refer,f_uv,'.r',ms=10)
            plt.plot([plt.xlim()[0],wave_refer],f_uv*numpy.ones(2),'--r',lw=1)





        if True:
            plt.annotate("$\\beta_{\\text{UV}}$="+str(numpy.round(beta_uv,2)),
                         xy=(1,1),xytext=(-10,-10),xycoords="axes fraction",textcoords="offset pixels",fontsize=12,
                         ha="right",va="top")
            
            plt.annotate("$f_{\lambda,\\text{UV}}$="+str(numpy.round(f_uv,2)),
                         xy=(1,1),xytext=(-10,-32),xycoords="axes fraction",textcoords="offset pixels",fontsize=12,
                         ha="right",va="top")
            

    plt.margins(x=0,y=0)
    plt.yscale('log')
    # plt.ylim(1e-25,1e2)
    # plt.ylim(1e-1,2e1)
    plt.ylim(max(flux)/10,max(flux)*2)
    plt.xscale('log')
    plt.xlim(8e2,3e3)
    # plt.axvline(912,c='k',ls='--')
    # plt.axvline(1215,c='k',ls='--')
    
    if SHOW_SPECTRA_FIGURE:ShadeUVRegion()

    if ShowPlot:plt.show()
    # plt.savefig("/mnt/home/student/cranit/Repo/MPAnalysis/temp/plots/spectra.svg")
    plt.close()
    
    # Dont forget to update invalid_return
    # return wave , flux * FLUX_UNIT
    return [offset, mass_formed, sfh[0], beta_uv, f_uv*FLUX_UNIT,Av]

# Single Call
# GetBagpipes(0)

# Dump Data for all
if False:
    N=10
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


#  Dump Parallel Version
from multiprocessing import Pool
import tqdm
if True:
    def GetBagpipesPool(offset):
        # print(offset,"Done")
        return GetBagpipes(offset,False)

    if __name__ == '__main__':
        N=100
        offsets = numpy.arange(N)
        with Pool(25) as p:
            # table=p.map(GetBagpipesPool, offsets)
            table=list(tqdm.tqdm(p.imap(GetBagpipesPool, offsets),total=N))

        table = numpy.array(table)
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


        numpy.savetxt(DATA_SAVE_PATH,table,header=header,fmt="%d %f %e %f %e %f")
        print("Saved :",DATA_SAVE_PATH,flush=True)

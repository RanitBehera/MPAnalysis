import bagpipes as pipes
import numpy as np
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')

# --- Model
exp = {}                          # Tau model star formation history component
exp["age"] = 3.                   # Gyr
exp["tau"] = 0.75                 # Gyr
exp["massformed"] = 9.            # log_10(M*/M_solar)
exp["metallicity"] = 0.5          # Z/Z_oldsolar

dust = {}                         # Dust component
dust["type"] = "Calzetti"         # Define the shape of the attenuation curve
dust["Av"] = 0.2                  # magnitudes

model_components = {}                   # The model components dictionary
model_components["redshift"] = 1.0      # Observed redshift  
model_components["exponential"] = exp   
model_components["dust"] = dust


# --- Filters
goodss_filt_list = np.loadtxt("/mnt/home/student/cranit/Repo/MPAnalysis/scripts/bagpipes/filters/myfilters.txt", dtype="str")

# --- Spectrum
# model = pipes.model_galaxy(model_components, filt_list=goodss_filt_list)

# gives spec at specified array of wavelengths
ws=500
we=1500
model = pipes.model_galaxy(model_components, filt_list=goodss_filt_list, spec_wavs=np.arange(ws, we, 5)) 



# --- Save
model.plot(False)

# model.sfh.plot(False)

plt.axvline(np.log10(ws),color='k',lw=1,ls='--')
plt.axvline(np.log10(we),color='k',lw=1,ls='--')
plt.savefig("/mnt/home/student/cranit/Work/Spectra/test.png", dpi=200)
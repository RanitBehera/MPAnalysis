import bagpipes
import numpy as np
import matplotlib.pyplot as plt



sfh = np.loadtxt("/mnt/home/student/cranit/Repo/MPAnalysis/sfh.txt")
# print(sfh)


# --- Model
custom = {}
custom["history"]     = sfh
custom["massformed"] = 9.22            # log_10(M*/M_solar)
custom["metallicity"] = 1          # Z/Z_oldsolar

# dust = {}                         # Dust component
# dust["type"] = "Calzetti"         # Define the shape of the attenuation curve
# dust["Av"] = 0.2                  # magnitudes

model_components = {}                   # The model components dictionary
model_components["redshift"] = 8.0      # Observed redshift  
model_components["custom"] = custom   
# model_components["dust"] = dust


# --- Filters
goodss_filt_list = np.loadtxt("/mnt/home/student/cranit/Repo/MPAnalysis/oldscripts/bagpipes/filters/myfilters.txt", dtype="str")

# --- Spectrum
# model = bagpipes.model_galaxy(model_components, filt_list=goodss_filt_list)

# gives spec at specified array of wavelengths
ws=500
we=1500
lams = np.logspace(3.6,4.8,10000)
model = bagpipes.model_galaxy(model_components, filt_list=goodss_filt_list)#, spec_wavs=lams)#np.arange(ws, we, 5)) 

# --- Save
# model.plot(False)
model.sfh.plot(False)


# plt.subplots()
# plt.plot(np.log10(model.spectrum[:,0]),model.spectrum[:,1])
# plt.xscale("log")

# plt.axvline(np.log10(ws),color='k',lw=1,ls='--')
# plt.axvline(np.log10(we),color='k',lw=1,ls='--')

# SAVE_PATH   = "/mnt/home/student/cranit/Work/RSGBank/Results/test_sepc.png" 
# plt.savefig(SAVE_PATH, dpi=200)
plt.show()
import numpy as np
import bagpipes as pipes

lbage_hr,sfr_hr = np.loadtxt("temp/sfh_hr.txt").T



# === BAGPIPES
goodss_filt_list = np.loadtxt("/mnt/home/student/cranit/Repo/MPAnalysis/oldscripts/bagpipes/filters/myfilters.txt", dtype="str")

dust = {"type":"Calzetti","Av":0.2,"eta":3.0}                         
nebular = {"logU":-3.}                      
sfh = np.column_stack((lbage_hr[::-1],sfr_hr[::-1]))
sfh = sfh[::200]
custom = {"history":sfh,"metallicity":0.1,"massformed":9.224393257882129}

model_components = {"redshift":8,"custom":custom,"dust":dust,"nebular":nebular}                   
# model_components["t_bc"] = 0.01         
# model_components["veldisp"] = 200. 

model = pipes.model_galaxy(model_components, filt_list=goodss_filt_list,spec_wavs=np.logspace(3.5,4.5,10000))

sfh_fig,sfh_ax = model.sfh.plot()

xdata=sfh_ax.lines[0].get_xdata()
ydata=sfh_ax.lines[0].get_ydata()

print("Max Input :",np.max(sfh[:,1]))
print("Max (Bagpipes) :",np.max(ydata))

# Bagpipes desired_mass/mass_norm scaling
# /mnt/home/student/cranit/Repo/MPAnalysis/gsconda/lib/python3.11/site-packages/bagpipes/models/star_formation_history.py:102

# Does-not effect much here because of smooth exponential curve of interpolation
# Original sfr is not smooth and hence scaling is more noticeable
# Should be improved with more data points 
import bagpipes as pipes
import numpy as np
import matplotlib.pyplot as plt

goodss_filt_list = np.loadtxt("/mnt/home/student/cranit/Repo/MPAnalysis/oldscripts/bagpipes/filters/myfilters.txt", dtype="str")



dust = {}                         
dust["type"] = "Calzetti"         
dust["Av"] = 0.2                  
dust["eta"] = 3.                  

nebular = {}                      
nebular["logU"] = -3.             

sfh = np.zeros((5, 2))

ex_data = np.loadtxt("/mnt/home/student/cranit/Repo/MPAnalysis/sfh.txt")

# sfh[:, 0] = np.arange(0., 10., 2.5)*10**8
# sfh[:, 1] = np.abs(np.random.randn(4))
# print(sfh)

# sfh =np.array([[1e8,2],[2e8,1],[3e8,3]])

sfh[:,0] = ex_data[:,0]
sfh[:,1] = ex_data[:,1]
print(sfh)



custom = {}
custom["history"] = sfh
# custom["massformed"] =  9.224393257882129  # Log_10 total stellar mass formed: M_Solar.
# custom["massformed"] =  9.26087315  # Log_10 total stellar mass formed: M_Solar.
custom["metallicity"] = 1.

model_components = {}                   
model_components["redshift"] = 8
# model_components["t_bc"] = 0.01         
# model_components["veldisp"] = 200. 
model_components["custom"] = custom
model_components["dust"] = dust
model_components["nebular"] = nebular

model = pipes.model_galaxy(model_components, filt_list=goodss_filt_list,spec_wavs=np.logspace(3.5,4.5,10000))

# SAVE_PATH   = "/mnt/home/student/cranit/Work/RSGBank/Results/bg_sfh.png" 
sfh_fig,sfh_ax = model.sfh.plot()

# print(sfh_ax.lines[0].get_xdata())
# print(sfh_ax.lines[0].get_ydata())

# plt.savefig(SAVE_PATH,dpi=200)

# SAVE_PATH   = "/mnt/home/student/cranit/Work/RSGBank/Results/bg_spec.png" 
# fig = model.plot()
# plt.savefig(SAVE_PATH,dpi=200)

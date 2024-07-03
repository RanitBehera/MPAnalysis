import matplotlib.pyplot as plt
import numpy as np

from cue.line import predict as line_predict
from cue.continuum import predict as cont_predict
from cue.utils import *


par = [[21.5, 14.85, 6.45, 3.15, 4.55, 0.7, 0.85, 49.58, 10**2.5, -0.85, -0.134, -0.134]]
lines = line_predict(theta=par).nn_predict()
cont = cont_predict(theta=par).nn_predict()





low_cont, med_cont, up_cont = np.quantile(np.array(cont), [0.16, 0.5, 0.84], axis=0)











# plot nebular continuum prediction
plt.figure(figsize=(7,3.5), dpi=120)
plt.plot(cont_lam[cont_lam>912],
         np.log10(med_cont*c/cont_lam[cont_lam>912]**2),
         color='C1', lw=2, alpha=0.7, label='nebular continuum')
plt.fill_between(cont_lam[cont_lam>912], 
                 y1=np.log10(low_cont*c/cont_lam[cont_lam>912]**2),
                 y2=np.log10(up_cont*c/cont_lam[cont_lam>912]**2),
                 facecolor='C1', edgecolor=None, alpha=0.4)
plt.xscale('log')
plt.legend(framealpha=0., handlelength=1.2)
plt.xlabel(r'$\mathrm{\lambda}$ ($\mathrm{\AA}$)', size=12)
plt.ylabel(r'log $\mathrm{F}_\lambda$ (erg s$^{-1}$ $\mathrm{\AA}^{-1}$)', size=12)


plt.show()
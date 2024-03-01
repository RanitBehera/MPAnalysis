import numpy
import galspec
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

reported_mass = 9.224393257882129   # log10(M*)

lbage = numpy.array([0.000000, 95173230.898091, 169242716.362828, 228219461.540078, 276079724.151465])
sfr = numpy.array([16.386204, 10.785671, 2.003063, 0.710654, 0.277032])
age = max(lbage) - lbage
plt.plot(age/1e6,sfr,'xr',ms=8,label="Sampled",mew=2)


# Exponential Interpolate
N_hr = 1000
age_hr = numpy.linspace(min(age),max(age),N_hr)
sfr_hr = numpy.zeros(len(age_hr))
lbage_hr = max(age_hr)-age_hr

def fit_fun(t,off,amp,tau):
    return off + amp * numpy.exp(t/tau)

par, err = curve_fit(fit_fun,age,sfr,[min(sfr),max(sfr)-min(sfr),numpy.mean(age)])
sfr_hr = fit_fun(age_hr, par[0],par[1],par[2])
plt.plot(age_hr/1e6,sfr_hr,'r',label="Interpolated")


# Dump for bagpipes grid dependence check
# numpy.savetxt("temp/sfr_hr.txt",numpy.column_stack((lbage_hr,sfr_hr)))


# Integrate - Simple
dM_star = numpy.zeros(N_hr-1)
for i in range(N_hr-1):
    dt = age_hr[i+1]-age_hr[i]
    sfr_t = sfr_hr[i]
    dm = sfr_t * dt
    dM_star[i] = dm

total_M_star = numpy.sum(dM_star)
integrated_mass = numpy.log10(total_M_star)



# Integrated - with IMF (Chabrier) effect
# from scipy.integrate import quad
# def Chabrier1(log10M):
#     if log10M<=1:
#         logme=numpy.log10(0.079)
#         return 0.158*numpy.exp(-((log10M-logme)**2/(2*(0.69**2))))
#     else:
#         m=10**log10M
#         return 0.0443*(m**-1.3)
    
# def Chabrier(log10M):
#     if log10M<=0.7:
#         logme=numpy.log10(0.22)
#         return (3.6*10**-4)*numpy.exp(-((log10M-logme)**2/(2*(0.33**2))))
#     else:
#         m=10**log10M
#         return (7.1*10**-5)*(m**-1.3)
    
# total_Area, err = quad(Chabrier,-numpy.inf,3)

# def M_upper_limit(lbage):
#     return (10**10/lbage)**0.4

# M_ul = M_upper_limit(lbage_hr[:-1])

# chab_area = numpy.empty(len(M_ul))
# for i,M in enumerate(M_ul):
#     l10m=numpy.log10(M)
#     chab_area[i]=quad(Chabrier,-numpy.inf,l10m)[0]

# chab_frac = chab_area / total_Area


# ic_dM_star =dM_star * chab_frac     # ic : imf corrected

# ic_total_M_star = numpy.sum(ic_dM_star)
# ic_integrated_mass = numpy.log10(ic_total_M_star)
    



# Plot beautification
plt.xlabel("Time since birth (Myr)")
plt.ylabel("SFR")
title = "Reported Mass".rjust(20)    + (" = $10^{" + str(numpy.round(reported_mass,8)) + "}M_\odot$").ljust(20) + "\n"
title += "Integrated Mass".rjust(20) + (" = $10^{" + str(numpy.round(integrated_mass,8)) + "}M_\odot$").ljust(20) #+ "\n"
# title += "Integrated Mass (C)".rjust(20) + (" = $10^{" + str(numpy.round(ic_integrated_mass,4)) + "}M_\odot$").ljust(20)

plt.title(title)
plt.legend()

plt.show()








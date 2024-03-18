import numpy, os
import matplotlib.pyplot as plt
from astropy.cosmology import FlatLambdaCDM


# Set for luminosity distance
HUBBLE = 69.7
OMEGA_M = 0.2814
CMBT = 2.7255
REDSHIFT = 8
lcdm = FlatLambdaCDM(H0=HUBBLE, Om0=OMEGA_M, Tcmb0=CMBT)
DL=lcdm.luminosity_distance(REDSHIFT).value #In Mpc
DL *= 3.086e24   # Mpc to cm
Area = 4*numpy.pi*(DL**2)


# Simulation flux
DIR = "/mnt/home/student/cranit/Repo/MPAnalysis/temp/UV_LUM/Av"
DIR = "/mnt/home/student/cranit/Repo/MPAnalysis/temp/spectra/"

def GetLuminosity(filename):
    file = os.path.join(DIR,filename)    
    # halo_offset,flux,sfr=numpy.loadtxt(file).T
    halo_offset,smass,sfr,beta,flux=numpy.loadtxt(file).T
    luminosity = flux*Area*(1+REDSHIFT) 
    return sfr,luminosity

min_sfr,max_sfr = None,None
def Plot(filename,**kwargs):
    sfr,luminosity = GetLuminosity(filename)
    
    # Update sfr range for observation overlay
    global min_sfr
    global max_sfr

    cur_min_sfr=numpy.min(sfr)
    cur_max_sfr=numpy.max(sfr)

    if min_sfr==None:min_sfr=cur_min_sfr
    elif cur_min_sfr < min_sfr: min_sfr = cur_min_sfr

    if max_sfr==None:max_sfr=cur_max_sfr
    elif cur_max_sfr > max_sfr: max_sfr = cur_max_sfr

    plt.plot(sfr,luminosity,ls='',label = kwargs["label"],ms=kwargs["ms"],marker=kwargs["marker"],color=kwargs["c"],zorder=kwargs["zorder"],alpha=kwargs["alpha"])


def PlotObserved():
    # Obsetrved flux
    # Eq 12 of Harikane Et al.(2023) : https://iopscience.iop.org/article/10.3847/1538-4365/acaaa9
    # SFR (M0 yr-1) = (K_UV) * L_UV(ergs s-1 Hz-1)
    # K_UV = 1.15e-28 ( M0 yr-1 / ergs s-1 Hz-1) : UV = 1500A
    lam = 1500e-8
    c = 3e10*1e-8
    nu = c/lam
    K_UV = 1.15e-28
    K_UV /= (nu**2/c)

    X = numpy.array([min_sfr,max_sfr])
    Y = X/K_UV
    plt.plot(X,Y,label="Harikane et al. (2023)",c='k')


plt.figure(figsize=(10,8))

Plot("bagdata.txt",label="$A_V=0.0$",marker=".",c='k',zorder=3,ms="5",alpha=1)
# Plot("lum_Av_00.txt",label="$A_V=0.0$",marker=".",c='k',zorder=3,ms="5",alpha=0.2)
# Plot("lum_Av_01.txt",label="$A_V=0.1$",marker="+",c='k',zorder=2,ms="5",alpha=0.2)
# Plot("lum_Av_02.txt",label="$A_V=0.2$",marker="x",c='r',zorder=1,ms="5",alpha=1.0)

PlotObserved()

# Beautify
plt.title("$\dot{\mathcal{M}}_{*} - \mathcal{L}_{UV}$ relation",fontsize=16)
plt.xlabel("SFR $\dot{\mathcal{M}}_{*} \\text{ } (M_\odot \\text{yr}^{-1})$",fontsize=12)
plt.ylabel("$\mathcal{L}_{UV} \\text{ }(\\text{erg } \\text{s }^{-1} \\text{Hz}^{-1})$",fontsize=12)
plt.xscale('log')
plt.yscale('log')
plt.legend()

plt.annotate("$\mathcal{K}_{\\text{UV}}=1.15\\times10^{-28} \\text{erg } \\text{s }^{-1} \\text{Hz}^{-1}/ M_\odot \\text{yr}^{-1}$",xy=(1,0),xycoords="axes fraction",ha="right",va="bottom")

plt.show()
# plt.savefig("temp/UV_LUM/Av/sfr_LUV_Av_02.png",dpi=300)
import numpy
import matplotlib.pyplot as plt
from astropy.cosmology import FlatLambdaCDM


# LUM_PATH = "/mnt/home/student/cranit/Work/RSGBank/TBSFR_Bank/luminosities.txt"
LUM_PATH = "/mnt/home/student/cranit/Repo/MPAnalysis/temp/UV_LUM/Av/lum_Av_00.txt"
off,ed,sfr = numpy.loadtxt(LUM_PATH).T # erg s-1 cm-2 A-1




# # Ed to lum by multipkying luminosisty disnatce
HUBBLE = 69.7
OMEGA_M = 0.2814
CMBT = 2.7255
REDSHIFT = 8
cosmo = FlatLambdaCDM(H0=HUBBLE, Om0=OMEGA_M, Tcmb0=CMBT)

DL=cosmo.luminosity_distance(REDSHIFT).value #In Mpc
cm_per_Mpc = 3.086e24
DL *= cm_per_Mpc
Area = 4*numpy.pi*(DL**2)

lum_flam = ed * Area*(1+REDSHIFT)/(4*numpy.pi*((3.086e+19)**2))


# === conversion
if True:
    lam = 1450
    f_lam = lum_flam
    f_nu_b_jy = (3.34e4)*(lam**2)*f_lam

    m_AB = -2.5*numpy.log10(f_nu_b_jy/3631)
    # m_AB to M_AB done while scaling flux



# === Binning
# print(m_AB)

Vol = (50)**3

LogBinStep = 1
LogBinStart = (int(min(m_AB)/LogBinStep)-1)*LogBinStep
LogBinEnd   = (int(max(m_AB)/LogBinStep)+1)*LogBinStep
MagBinCount = numpy.zeros(int((LogBinEnd-LogBinStart)/LogBinStep))

for M in m_AB:
    i = int((M-LogBinStart)/LogBinStep)
    MagBinCount[i] +=1

err = numpy.sqrt(MagBinCount)

# Normalise
MagBinCount /= (Vol*LogBinStep)
err /= (Vol*LogBinStep)

#  offset to center of bin
M_UV = numpy.arange(LogBinStart,LogBinEnd,LogBinStep) + (LogBinStep/2)

# Filter our zero bin count
mask = (MagBinCount!=0)
M_UV = M_UV[mask]
MagBinCount = MagBinCount[mask]
err = err[mask]



plt.plot(M_UV,MagBinCount)
plt.fill_between(M_UV,MagBinCount+(0.8*err/2),MagBinCount-(0.8*err/2),alpha=0.1)


# Load Obs
def PlotObsMUVCount(study,redshift,xerr=False,**args):
    # Load Study
    data=numpy.asarray(numpy.loadtxt(r"/mnt/home/student/cranit/Repo/MPAnalysis/temp/OBSLF//"+study+".csv",delimiter=","))[:]

    # Obtain Redshift
    obs_redshift=data[:,0]          # Column 1

    # Filter Redshift
    ids=numpy.where(obs_redshift==redshift)
    data=data[ids,:][0]
  
    # Extract Columns
    M_UV=data[:,1]                          # Column 2
    base10_exp=data[:,5]                    # Column 6
    Phi=data[:,2]*(10**base10_exp)          # Column 3
    yerr_p=data[:,3]*(10**base10_exp)       # Column 4
    yerr_n=data[:,4]*(10**base10_exp)       # Column 5
    if xerr : xerr=data[:,6]                # Column 7

    plt.errorbar(M_UV,Phi,[yerr_n,yerr_p],xerr,**args)

PlotObsMUVCount("donnan",8,True,ms=5,capsize=3,label="Donnan+23",color='g',marker='o',lw=1,ls='')
PlotObsMUVCount("bouwens",8,ms=5,capsize=3,label="Bouwens+22",color='b',marker='x',lw=1,ls='')
PlotObsMUVCount("bowler",8,True,ms=5,capsize=3,label="Bowler+20",color='m',marker='s',lw=1,ls='')



# ======
plt.legend()
plt.xlabel("Absolute Magnitude (AB)")
plt.ylabel("$Number/Mpc^{-3}/Mag$")
plt.title("Redshift z~"+str(8))
plt.grid(alpha=0.2)
plt.yscale('log')
# plt.show()
plt.savefig("/mnt/home/student/cranit/Repo/MPAnalysis/temp/plots_mar9/lum_fun.png",dpi=300)
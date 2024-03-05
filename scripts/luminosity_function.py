import numpy
import matplotlib.pyplot as plt

LUM_PATH = "/mnt/home/student/cranit/Work/RSGBank/TBSFR_Bank/luminosities.txt"
lum_flam = numpy.loadtxt(LUM_PATH) # erg s-1 cm-2 A-1

# === conversion
if True:
    c = 3e8 * 1e10 # A/s
    # print(c)
    # exit()
    lam = 1450 *(1+8) # A
    cf = (lam**2)/c

    lum_fnu = lum_flam/cf # per angstorm to per Hz conversion as Jy unit

    Jy = 1e-23 # erg s-1 cm-2 Hz-1
    ref = 3631*Jy

    # m_AB = -2.5*numpy.log10(lum_fnu/ref)
    m_AB = -2.5*numpy.log10(lum_fnu)-48.60+2
    

if False:
    # convert to si
    lum_flam_si = lum_flam * (1e-7) / (((1e-2)**2) * (1e-10)) # J s-1 m-2 m-1
    lam = 1450 *(1+8)* (1e-10)
    c=3e8
    lum_nu_si = lum_flam_si * (lam**2)/c  # J s-1 m-2 Hz-1
    lum_nu = lum_nu_si * (1e7) / (((1e2)**2))
    Jy = 1e-23 # erg s-1 cm-2 Hz-1
    ref = 3631*Jy
    m_AB = -2.5*numpy.log10(lum_nu)-48.60







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
plt.show()
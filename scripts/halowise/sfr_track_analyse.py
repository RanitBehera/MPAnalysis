import numpy,os
import matplotlib.pyplot as plt


SAVED_PATH = "/mnt/home/student/cranit/Work/RSGBank/TBSFR_Bank"

# PLOT
for offset in range(100):
    lbage,sfr = numpy.loadtxt(os.path.join(SAVED_PATH,"off_"+str(offset)+".txt")).T
    lbage /= 1e6
    plt.plot(lbage,sfr,'k',alpha=0.1)

# --- BEAUTIFY
# plt.xscale('log')
plt.yscale('log')
# plt.xlabel("Density (??)")
# plt.ylabel("Temperature (K)")
# plt.axhline(100,ls='--',lw=1,color='k')
# plt.axhline(10000,ls='--',lw=1,color='k')

# plt.title("L=50Mpc , N=$640^3$ , z=8 , $\\text{N}_{\\text{min}}^{\\text{halo}}=50$ , HID=" + str(TIHID) + " , $\\text{N}_{\\text{gas}}^{\\text{halo}}=$" + str(len(TEMP)),pad=10)


# --- SAVE
plt.show()
# plt.savefig(SAVE_PATH,dpi=200)
import numpy
import matplotlib.pyplot as plt
import os

# --- Config
DIR = "/mnt/home/student/cranit/Work/Merger_Tree_WSFR_Mod/RKSG_L50N640c"
REDSHIFT=8

# ---
SNAP_RED_DICT={"016":"12", "020":"11", "024":"10", "030":"9", "036":"8", "050":"6"}
RED_SNAP_DICT={"12":"016", "11":"020", "10":"024", "9":"030", "8":"036", "6":"050"}

FF_SNAP_NUM = RED_SNAP_DICT[str(REDSHIFT)] # Fixed Format
FILE_NAME = "halos_PART_" + FF_SNAP_NUM + ".0.particles"
FILE_PATH = DIR + os.sep + FILE_NAME



# --- data access
data = numpy.loadtxt(FILE_PATH)
m_vir= data[:,0]
sfr= data[:,5]

n_dm= data[:,1]
n_gas= data[:,2]
n_star= data[:,3]
n_bh= data[:,4]

mt_dm= 0.00311013
mt_gas= 0.000614086
mt_star=0.000153522
mt_bh=0.000153522

mu=10**10

m_dm = n_dm * mt_dm * mu 
m_gas = n_gas * mt_gas * mu
m_star = n_star * mt_star * mu
m_bh = n_bh * mt_bh * mu

# plt.plot(m_vir,sfr,'.',ms=1)

# plt.plot(m_dm,sfr,'.',ms=1)
# plt.axvline(mt_dm*mu,color='k',lw=1,ls='--')
# plt.plot(m_gas,sfr,'.',ms=1)
# plt.axvline(mt_gas*mu,color='k',lw=1,ls='--')
plt.plot(m_star,sfr,'.',ms=2)
plt.axvline(mt_star*mu,color='k',lw=1,ls='--')


plt.xscale('log')
plt.yscale('log')

plt.savefig("/mnt/home/student/cranit/Work/Merger_Tree_WSFR_Mod/Results/sfr_smass_z"+ str(REDSHIFT)+".png",dpi=200)
plt.savefig("/mnt/home/student/cranit/Work/Merger_Tree_WSFR_Mod/Results/sfr_smass_z"+ str(REDSHIFT) +".svg")
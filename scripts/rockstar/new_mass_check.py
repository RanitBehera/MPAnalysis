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
mvir= data[:,0]

n_dm= data[:,1]
n_gas= data[:,2]
n_star= data[:,3]
n_bh= data[:,4]

mt_dm= 0.00311013
mt_gas= 0.000614086
mt_star=0.000153522
mt_bh=0.000153522

m_dm = n_dm * mt_dm
m_gas = n_gas * mt_gas
m_star = n_star * mt_star
m_bh = n_bh * mt_bh

mu=10**10
m_total = m_dm + m_gas + m_star + m_bh
m_total*=mu

mass_mask=(mvir>=10**10)

frac=m_total/mvir

print(frac[mass_mask])
plt.hist(frac[mass_mask],bins=100)
plt.yscale('log')


plt.savefig("/mnt/home/student/cranit/Work/Merger_Tree_WSFR_Mod/Results/check_mass_calc_dist_z"+ str(REDSHIFT)+".png",dpi=200)
plt.savefig("/mnt/home/student/cranit/Work/Merger_Tree_WSFR_Mod/Results/check_mass_calc_dist_z"+ str(REDSHIFT) +".svg")
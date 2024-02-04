import os,numpy
import matplotlib.pyplot as plt


# --- Config
DIR = "/mnt/home/student/cranit/Work/Merger_Tree_WSFR_Mod/RKSG_L50N640c"
REDSHIFTS=[12,11,10,9,8,6]


# --- Derived Config
SNAP_RED_DICT={"016":"12", "020":"11", "024":"10", "030":"9", "036":"8", "050":"6"}
RED_SNAP_DICT={"12":"016", "11":"020", "10":"024", "9":"030", "8":"036", "6":"050"}


# --- Data Access

def get_nz_sfr_fraction(z,mass_bins):
    ff_snap_num = RED_SNAP_DICT[str(z)]
    file_name = "halos_PART_" + ff_snap_num + ".0.particles"
    file_path = DIR + os.sep + file_name

    data = numpy.loadtxt(file_path)
    sfr         =   data[:,5]                       # < ---- sfr column number may change in future
    halo_mass   =   data[:,0]

    def get_nz_sfr_for_mass_range(start,end):
        log10_mh = numpy.log10(halo_mass)
        mask_mass = ((log10_mh>=start) & (log10_mh<end))    

        selected_sfr    = sfr[mask_mass]        # length same as selected halos within mass range

        if not len(selected_sfr)==0:
            selected_nz_sfr = selected_sfr[selected_sfr!=0]
            nz_sfr_fraction = len(selected_nz_sfr)/len(selected_sfr)
            return nz_sfr_fraction
        else:
            return None
        
    # binned non-zero sfr fractions
    fracs = numpy.arange(len(mass_bins)-1,dtype=object)

    for i in range(len(mass_bins)-1):
        fracs[i]=get_nz_sfr_for_mass_range(mass_bins[i],mass_bins[i+1])

    return fracs



MASS_BINS = numpy.arange(7,13)
FRACTIONS = numpy.zeros((len(REDSHIFTS),len(MASS_BINS)-1))

for idx,red in enumerate(REDSHIFTS):
    FRACTIONS[idx]=get_nz_sfr_fraction(red,MASS_BINS)

FRACTIONS = FRACTIONS.T # Same mass bin in a column to in a row, easier to extract

# Plot
fig,ax1=plt.subplots()

for i in range(len(MASS_BINS)-1):
    tag = str(MASS_BINS[i]) + " - " + str(MASS_BINS[i+1])
    
    if i==3:
        ax1.plot(REDSHIFTS,FRACTIONS[i],'.-',label=tag,lw=2,ms=10)
    else:
        ax1.plot(REDSHIFTS,FRACTIONS[i],'.-',label=tag,lw=1,ms=8)

ax1.invert_xaxis()
ax1.set_xlabel("Redshift")
ax1.set_ylabel("Non-zero fraction")



# Second axis for look back time ---
from matplotlib.ticker import FormatStrFormatter
from astropy.cosmology import FlatLambdaCDM, z_at_value
import astropy.units as apu
cosmo = FlatLambdaCDM(H0=69.7, Om0=0.2814, Tcmb0=2.7255)      # <--- Hard Coded

def Z_2_LB(z):
    return cosmo.lookback_time(z).value  # In Gyr

def LB_2_Z(lb): # in Gyr
    # return float(z_at_value(cosmo.lookback_time,lb*apu.Gyr).value)
    # return lb**0.5
    return lb


ax2 = ax1.secondary_xaxis('top', functions=(Z_2_LB, LB_2_Z))
ax2.set_xlabel('Lookback Time (Gyr)', fontsize=10)
z_ticks = ax1.get_xticks()
lb_ticks = Z_2_LB(z_ticks)
ax2.set_xticks(lb_ticks)
ax2.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
ax2.xaxis.set_tick_params(labelsize=8)
# ----------------------------------


plt.legend(frameon=False,fontsize=8,ncols=5,loc="upper center",bbox_to_anchor=(0.5,1.35),
           title="Mass Bins : $\log_{10}\left(M_{\\text{halo}}\\right)$")
plt.subplots_adjust(top=0.7)
plt.title("Non-Zero SFR Fraction",pad=80)
plt.grid(alpha=0.3)

plt.savefig("/mnt/home/student/cranit/Work/Merger_Tree_WSFR_Mod/Results/binned_sfr_nz_frac.png",dpi=200)
plt.savefig("/mnt/home/student/cranit/Work/Merger_Tree_WSFR_Mod/Results/binned_sfr_nz_frac.svg")




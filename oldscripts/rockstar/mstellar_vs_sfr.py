import numpy
import matplotlib.pyplot as plt
import os

# --- Config
DIR = "/mnt/home/student/cranit/Work/Merger_Tree_WSFR_Mod/RKSG_L50N640c"
REDSHIFT=8
BOX_SIZE=50 #Mpc
NUM_PART=640


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



mass_cuts=numpy.logspace(numpy.log10(min(m_vir)),numpy.log10(max(m_vir)),100)

def PlotFrame(i):
    low_mass_cut=mass_cuts[i]
    mass_mask=(m_vir>=low_mass_cut)

    # plt.plot(m_vir,sfr,'.',ms=1)
    # plt.plot(m_dm,sfr,'.',ms=1)
    # plt.axvline(mt_dm*mu,color='k',lw=1,ls='--')
    # plt.plot(m_gas,sfr,'.',ms=1)
    # plt.axvline(mt_gas*mu,color='k',lw=1,ls='--')

    plt.plot(m_star[mass_mask],sfr[mass_mask],'.',ms=2)
    plt.axvline(mt_star*mu,color='k',lw=1,ls='--')


    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("Stellar Mass $(M_{\odot})$")
    plt.ylabel("SFR $(M_{\odot}/yr^{-1})$")
    plt.xlim([10**6,10**10])
    plt.ylim([10**-6,10**2])
    plt.subplots_adjust(left=0.12,right=0.80,bottom=0.12,top=0.85)

    plt.title("Stellar Mass vs SFR Distribution\n( L="+ str(BOX_SIZE) +"Mpc, N=$" + str(NUM_PART) + "^3, $ z="+str(REDSHIFT)+" )",pad=10 )


    # --- Halo Mass Cut Bar
    a2=plt.axes((0.81,0.12,0.05,0.85-0.12))
    a2.set_xticks([])
    a2.yaxis.tick_right()
    a2.yaxis.set_label_position("right")
    a2.set_ylabel("Halo Mass Range ($M_{\odot}$)",rotation=270,labelpad=20)
    a2.set_yscale("log")
    a2.set_xlim([0,1])
    a2.set_ylim([0.5*min(m_vir),max(m_vir)*2])
    a2.axhline(min(m_vir),color='k',ls='--',lw=1)
    a2.axhline(max(m_vir),color='k',ls='--',lw=1)
    a2.fill_between(a2.get_xlim(),y1=low_mass_cut*numpy.ones(2),y2=max(m_vir)*numpy.ones(2),alpha=0.5)



    plt.savefig("/mnt/home/student/cranit/Work/Merger_Tree_WSFR_Mod/Results/frames/sfr_stell_mass/sfr_smass_z"+ str(REDSHIFT)+ "_" + str(i)+".png",dpi=200)
    # plt.savefig("/mnt/home/student/cranit/Work/Merger_Tree_WSFR_Mod/Results/frames/sfr_stell_mass/sfr_smass_z"+ str(REDSHIFT) +".svg")

    plt.clf()

for i in range(len(mass_cuts)-1):
    PlotFrame(i)
    print("Frame",i,": Done")

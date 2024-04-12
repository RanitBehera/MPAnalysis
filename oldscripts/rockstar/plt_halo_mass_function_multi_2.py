from hmf import MassFunction
import matplotlib.pyplot as plt
import numpy,sys,os
from hmf import cosmology

sys.path.append("/home/ranitbehera/MyDrive/Repos/MPAnalysis/")
import galspecold as mp

# --- CONFIG PARAMETERS
GADGET_PATH             = "/home/ranitbehera/MyDrive/Data/MP-Gadget/L50N640/"
ROCKSTAR_PATH           = "/mnt/home/student/cranit/Work/RKSG_Benchmark/L50N640c/ZD_Prof/RKS"
ROCKSTAR_GALAXIES_PATH  = "/home/ranitbehera/MyDrive/Work/MF640_frm_mod_out/"
SNAP_NUMBER             = 36
REDSHIFT                = 8
# ROCKSTAR_HALO_FILENAME  = "halos_PART_"+'{:03}'.format(SNAP_NUMBER)+".hdf5.0.ascii"
ROCKSTAR_HALO_FILENAME  = "halos_PART_036.0.ascii"
INCLUDE_PIG             = True
BINDEXSTEP              = 0.5
SHOW_DEVIATION_PLOT     = False


# --- DERIVED PARAMETERS
HFILEPATH               = ROCKSTAR_PATH + os.sep + ROCKSTAR_HALO_FILENAME
HGFILEPATH              = ROCKSTAR_GALAXIES_PATH + os.sep + ROCKSTAR_HALO_FILENAME

cfg=mp.ConfigFile(ROCKSTAR_GALAXIES_PATH)
VOLUME          = cfg.BOX_SIZE**3
# REDSHIFT        = (1/cfg.SCALE_NOW)-1 
OMEGA_M         = cfg.Om
HUBBLE_H        = cfg.h0

# --- SIMULATION HALO MASS FUNCTION
def SimHMF(Mass,LogBinStep):
    # log10_Mass=numpy.log10(Mass)
    log10_Mass=numpy.log(Mass)

    log10_bin_start=numpy.floor(min(log10_Mass))
    log10_bin_end=numpy.ceil(max(log10_Mass))


    BinCount=numpy.zeros(int((log10_bin_end-log10_bin_start)/LogBinStep))

    for lm in log10_Mass:
        i=int((lm-log10_bin_start)/LogBinStep)
        BinCount[i]+=1

    # print(BinCount)

    log10_M=numpy.arange(log10_bin_start,log10_bin_end,LogBinStep)+(LogBinStep/2)
    dn_dlogM=BinCount/(VOLUME*LogBinStep)
    error=numpy.sqrt(BinCount)/(VOLUME*LogBinStep)

    return log10_M,dn_dlogM,error


# --- PLOTTING METHODS

def Plot_Model_HMF(axis_handle,model_name,**kwargs):
    mf = MassFunction(z = REDSHIFT,hmf_model=model_name,cosmo_params={"Om0":OMEGA_M,"H0":HUBBLE_H*100,"Tcmb0":2.7255})
    mf.Mmin=7
    mf.Mmax=12
    h=HUBBLE_H
    axis_handle.plot(mf.m,mf.dndlog10m*(h**3),**kwargs)

my_cosmo = {'flat': True, 'H0': 69.7, 'Om0': 0.2814, 'Ob0':0.0464, 'sigma8': 0.81, 'ns': 0.971}
from colossus.cosmology import cosmology
cosmology.setCosmology("my_cosmo",my_cosmo)
from colossus.lss import mass_function

def Plot_Colo_HMF(axis_handle,model_name,mdef="fof",**kwargs):
    z = REDSHIFT
    M = 10**numpy.arange(7.0, 14, 0.1)
    mfunc = mass_function.massFunction(M, z, mdef = mdef, model = model_name, q_out = 'dndlnM')
    mass_function.massFunction()
    axis_handle.plot(M,mfunc,**kwargs)
    
    
def Plot_Model_Deviation(axis_handle,model_name,dn_dlogM,error,**kwargs):
    # ----------- Make model hmf automatic
    # Low Res for Error
    h=HUBBLE_H
    mf_l=MassFunction(z=REDSHIFT,hmf_model=model_name,cosmo_params={"Om0":OMEGA_M,"H0":HUBBLE_H*100,"Tcmb0":2.7255},dlog10m=BINDEXSTEP)
    mf_l.Mmin=7.1
    mf_l.Mmax=11.9
    
    diff=mf_l.dndlog10m-dn_dlogM
    fact=mf_l.dndlog10m*(h**3)/dn_dlogM
    fi=0
    fe=-1
    axis_handle.plot(mf_l.m[fi:fe],fact[fi:fe],'.-',**kwargs)

    fact_p=mf_l.dndlog10m*(h**3)/(dn_dlogM-error)
    fact_n=mf_l.dndlog10m*(h**3)/(dn_dlogM+error)

    axis_handle.fill_between(mf_l.m[fi:fe],fact_p[fi:fe],fact_n[fi:fe],**kwargs)


def Plot_PIG_HMF(axis_handle,GADGET_PATH=GADGET_PATH,SNAP_NUMBER=SNAP_NUMBER,BINDEXSTEP=BINDEXSTEP,**kwargs):
    op=mp.BaseDirectory(GADGET_PATH)
    PIGMass=op.PIG(SNAP_NUMBER).FOFGroups.MassByType.ReadValues()*1e10
    cdm_mass=PIGMass[:,1]
    log10_M,dn_dlogM,error=SimHMF(cdm_mass,BINDEXSTEP)
    fi,fe=0,-1
    error=error/2
    # axis_handle.errorbar(10**log10_M[fi:fe],dn_dlogM[fi:fe],error[fi:fe],**kwargs)
    axis_handle.errorbar(numpy.e**log10_M[fi:fe],dn_dlogM[fi:fe],error[fi:fe],**kwargs)
    
    # ------ Get axis handle 2 and kwargs
    # Plot_Model_Deviation(ac,"ST",dn_dlogM,error,alpha=0.2,edgecolor=(0,0,0,0),color="m")


def Plot_RKS_HMF(axis_handle,HALOFILE_PATH=HFILEPATH,BINDEXSTEP=BINDEXSTEP,**kwargs):
    data=numpy.loadtxt(HALOFILE_PATH)
    m_vir=data[:,mp.ascii.mvir]
    mask=~(m_vir==0)
    m_vir=m_vir[mask]

    log10_M,dn_dlogM,error=SimHMF(m_vir,BINDEXSTEP)
    fi,fe=0,-1
    error=error/2
    # axis_handle.errorbar(10**log10_M[fi:fe],dn_dlogM[fi:fe],error[fi:fe],**kwargs)
    axis_handle.errorbar(numpy.e**log10_M[fi:fe],dn_dlogM[fi:fe],error[fi:fe],**kwargs)

def Plot_RKS_ONLY_HMF(axis_handle,PATH=HFILEPATH,BINDEXSTEP=BINDEXSTEP,**kwargs):
    Plot_RKS_HMF(axis_handle,HALOFILE_PATH=PATH,BINDEXSTEP=BINDEXSTEP,**kwargs)

def Plot_RKS_GAL_HMF(axis_handle,PATH=HGFILEPATH,BINDEXSTEP=BINDEXSTEP,**kwargs):
    Plot_RKS_HMF(axis_handle,HALOFILE_PATH=PATH,BINDEXSTEP=BINDEXSTEP,**kwargs)
    

def Plot_RKSG_BGC2_HMF(axis_handle,BGC2FILE_PATH,BINDEXSTEP=BINDEXSTEP,exclude_subhalo=True,**kwargs):
    data=numpy.loadtxt(BGC2FILE_PATH)
    m_vir=data[:,2]
    mask_roothalo=(data[:,14]==-1)

    if exclude_subhalo:
        m_vir=m_vir[mask_roothalo]

    log10_M,dn_dlogM,error=SimHMF(m_vir,BINDEXSTEP)
    fi,fe=0,-1
    error=error/2
    axis_handle.errorbar(10**log10_M[fi:fe],dn_dlogM[fi:fe],error[fi:fe],**kwargs)



def Plot_filtered(axis_handle,filter_file_path,BINDEXSTEP=BINDEXSTEP,**kwargs):
    data=numpy.loadtxt(filter_file_path)
    N_dm=data[:,1]
    N_gas=data[:,2]
    N_star=data[:,3]
    N_bh=data[:,4]


    mu=1e10
    mt_dm=0.00311013
    mt_gas=0.000614086
    mt_star= 0.000153522
    mt_bh= 0.000153522

    M_dm=N_dm*mt_dm*mu
    M_gas=N_gas*mt_gas*mu
    M_star=N_star*mt_star*mu
    M_bh=N_bh*mt_bh*mu

    M_tot=M_dm+M_gas+M_star+M_bh
    def DoForMass(mass,label,**kwargs):
        log10_M,dn_dlogM,error=SimHMF(mass,BINDEXSTEP)
        error=error/2
        axis_handle.errorbar(numpy.e**log10_M,dn_dlogM,error,label=label,**kwargs)
    


    DoForMass(M_dm[M_dm!=0],"RKSG (PFILE - Mod ,DM)",color="m")
    DoForMass(M_star[M_star!=0],"PFILE (PFILE - Mod, Star)",color="r")
    DoForMass(M_gas[M_gas!=0],"RKSG (PFILE - Mod, Gas)",color="y")
    DoForMass(M_bh[M_bh!=0],"RKSG (PFILE - Mod, BH)",color="c")
    DoForMass(M_tot[M_tot!=0],"RKSG (PFILE - Mod, Total)",color="g",lw=2)







# --- PLOTTING
if SHOW_DEVIATION_PLOT:
    f,(ac,ae)= plt.subplots(2,1,gridspec_kw={'height_ratios':[3,2]},figsize=(12,10))
    plt.subplots_adjust(hspace=0.0)
else:
    f,ac=plt.subplots(1,1,figsize=(12,10))

# Possible model HMF
# PS, ST, Behroozi, Angulo, Bhattacharya, Courtin, Crocce, Ishiyama, Jenkins, Manera, Peacock, Pillepich, Reed03, Reed07, Warren, Watson, Tinker08, Tinker10
# Plot_Model_HMF(ac,"PS",label="Press-Schechter",color='b')
# Plot_Model_HMF(ac,"ST",label="Seith-Tormen (hmf)",color='k')
# Plot_Model_HMF(ac,"Behroozi",label="Behroozi",color='m')

Plot_Colo_HMF(ac,'sheth99',ls="--",label="Sheth99 (colossus, fof)",color='k',lw=1)
# Plot_Colo_HMF(ac,'press74',ls="--",label="Press74 (colossus, fof)",color='m',lw=1)
Plot_Colo_HMF(ac,'comparat17',ls="-",label="Comparat17 (colossus, vir)",mdef='vir',color='k',lw=1)

if INCLUDE_PIG:
    Plot_PIG_HMF(ac,fmt='--',capsize=1,color='k',label="FoF (MP-Gadget)",lw=1)
    pass
# Plot_RKS_ONLY_HMF(ac,fmt='-',capsize=1,color='g',label="Rockstar",lw=1)
Plot_RKS_GAL_HMF(ac,fmt='-',capsize=1,color='k',label="RKSG (HFILE, mvir)",lw=1)

# Plot_filtered(ac,"/mnt/home/student/cranit/Work/RKSG_Benchmark/L50N640c/RKSG_S36LL20_WP/LengthByType2.txt")
Plot_filtered(ac,"/home/ranitbehera/MyDrive/Work/MF640_frm_mod_out/halos_PART_036.0.particles")



# Plot_RKS_ONLY_HMF(ac,"/mnt/home/student/cranit/Work/RKSG_Benchmark/L50N640c/LL_Prof/RKS/L18" +os.sep+"halos_PART_036.hdf5.0.ascii",fmt='.-',capsize=2,label="Rockstar (0.18)")
# Plot_RKS_ONLY_HMF(ac,"/mnt/home/student/cranit/Work/RKSG_Benchmark/L50N640c/LL_Prof/RKS/L20" +os.sep+"halos_PART_036.hdf5.0.ascii",fmt='.-',capsize=2,label="Rockstar (0.20)")
# Plot_RKS_ONLY_HMF(ac,"/mnt/home/student/cranit/Work/RKSG_Benchmark/L50N640c/LL_Prof/RKS/L22" +os.sep+"halos_PART_036.hdf5.0.ascii",fmt='.-',capsize=2,label="Rockstar (0.22)")
# Plot_RKS_ONLY_HMF(ac,"/mnt/home/student/cranit/Work/RKSG_Benchmark/L50N640c/LL_Prof/RKS/L24" +os.sep+"halos_PART_036.hdf5.0.ascii",fmt='.-',capsize=2,label="Rockstar (0.24)")
# Plot_RKS_ONLY_HMF(ac,"/mnt/home/student/cranit/Work/RKSG_Benchmark/L50N640c/LL_Prof/RKS/L26" +os.sep+"halos_PART_036.hdf5.0.ascii",fmt='.-',capsize=2,label="Rockstar (0.26)")
# Plot_RKS_ONLY_HMF(ac,"/mnt/home/student/cranit/Work/RKSG_Benchmark/L50N640c/LL_Prof/RKS/L28" +os.sep+"halos_PART_036.hdf5.0.ascii",fmt='.-',capsize=2,label="Rockstar (0.28)")
# Plot_RKS_ONLY_HMF(ac,"/mnt/home/student/cranit/Work/RKSG_Benchmark/L50N640c/LL_Prof/RKS/L30" +os.sep+"halos_PART_036.hdf5.0.ascii",fmt='.-',capsize=2,label="Rockstar (0.30)")

# Plot_RKS_ONLY_HMF(ac,"/mnt/home/student/cranit/Work/RKSG_Benchmark/L50N640c/LL_Prof/RKSG/L18" +os.sep+"halos_PART_036.hdf5.0.ascii",fmt='.-',capsize=2,label="Rockstar Galaxies (0.18)")
# Plot_RKS_ONLY_HMF(ac,"/mnt/home/student/cranit/Work/RKSG_Benchmark/L50N640c/LL_Prof/RKSG/L20" +os.sep+"halos_PART_036.hdf5.0.ascii",fmt='.-',capsize=2,label="Rockstar Galaxies (0.20)")
# Plot_RKS_ONLY_HMF(ac,"/mnt/home/student/cranit/Work/RKSG_Benchmark/L50N640c/LL_Prof/RKSG/L22" +os.sep+"halos_PART_036.hdf5.0.ascii",fmt='.-',capsize=2,label="Rockstar Galaxies (0.22)")
# Plot_RKS_ONLY_HMF(ac,"/mnt/home/student/cranit/Work/RKSG_Benchmark/L50N640c/LL_Prof/RKSG/L24" +os.sep+"halos_PART_036.hdf5.0.ascii",fmt='.-',capsize=2,label="Rockstar Galaxies (0.24)")
# Plot_RKS_ONLY_HMF(ac,"/mnt/home/student/cranit/Work/RKSG_Benchmark/L50N640c/LL_Prof/RKSG/L26" +os.sep+"halos_PART_036.hdf5.0.ascii",fmt='.-',capsize=2,label="Rockstar Galaxies (0.26)")
# Plot_RKS_ONLY_HMF(ac,"/mnt/home/student/cranit/Work/RKSG_Benchmark/L50N640c/LL_Prof/RKSG/L28" +os.sep+"halos_PART_036.hdf5.0.ascii",fmt='.-',capsize=2,label="Rockstar Galaxies (0.28)")
# Plot_RKS_ONLY_HMF(ac,"/mnt/home/student/cranit/Work/RKSG_Benchmark/L50N640c/LL_Prof/RKSG/L30" +os.sep+"halos_PART_036.hdf5.0.ascii",fmt='.-',capsize=2,label="Rockstar Galaxies (0.30)")







# Final Plot
ac.set_xscale('log')
ac.set_yscale('log')
ac.set_xlim([2e5,5e+12])
ac.set_ylim([1e-5,1e1])
ac.grid(alpha=0.5)
ac.legend()
# ac.set_xticks([])
# ac.set_ylabel("$dn/dlog_{10}(M/M_\odot)$",fontsize=12)
ac.set_ylabel("$dn/dln(M/M_\odot)$",fontsize=12)

if SHOW_DEVIATION_PLOT:
    ae.set_xscale('log')
    ae.set_yscale('log')
    ae.set_xlim([2e8,5e+11])
    ae.set_ylim([0.4,2.5])
    ae.grid(alpha=0.5)
    ae.yaxis.tick_right()
    ae.set_xlabel("Mass $log_{10}(M/M_\odot)$",fontsize=12)
    ae.set_ylabel("Deviation By Factor\nRelative to ROCKSTAR",fontsize=12)
    ae.axhline(1,color='k',ls='-',lw=1)

    tick_ref = [0.4,0.5,0.6,0.7,0.8,0.9,1,2,]
    tick_lable = ['','$\\times$ 0.5','','','','','$\\times$ 1','$\\times$ 2']

    ae.set_yticks([])
    ae.set_yticks(tick_ref)
    ae.set_yticklabels(tick_lable, minor=False)

if not SHOW_DEVIATION_PLOT:
    ac.set_xlabel("Mass $log_{10}(M/M_\odot)$",fontsize=12)

ac.set_title("Dark Matter Halo Mass Function Comparision (z="+str(numpy.round(REDSHIFT,2))+") : L = $" + str(cfg.BOX_SIZE) + "$ Mpc , N = $640^3$")
# plt.tight_layout()
# plt.show()
# plt.savefig("/mnt/home/student/cranit/Work/RKSG_Benchmark/results/MF_All_Part_640/ObO/snap" + '{:03}'.format(SNAP_NUMBER) + ".png",dpi=200)
plt.savefig("/home/ranitbehera/MyDrive/Meet/Result_17122023/5 MFP640 Mod/snap" + '{:03}'.format(SNAP_NUMBER) + ".svg")

